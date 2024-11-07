import os
import re
import logging
from datetime import datetime
from tempfile import NamedTemporaryFile
from typing import Union
from zipfile import ZipFile

import pandas as pd
from pandas import DataFrame
from requests.auth import HTTPBasicAuth

from k2magic.dialect import k2a_requests
from sqlalchemy import make_url, literal, URL, and_, MetaData, Table, String, Integer, Column, Float, \
    BinaryExpression
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.visitors import traverse

from k2magic.dataframe_db import DataFrameDB
from k2magic.dataframe_db_exception import DataFrameDBException


class K2DataFrameDB(DataFrameDB):
    """
    扩展DataFrameDB，提供访问K2Assets Repo数据的能力（原生方式，非REST方式）
    :param repo_url: 数据库连接 URL
    :param db_port: 底层数据库对外暴露的端口号
    :param debug: 调试模式可输出更多日志信息
    """

    def __init__(self, repo_url: Union[str, URL], schema=None, db_port: int = None,
                 debug: bool = False, rest: bool = False):
        self.repo_url_obj = make_url(repo_url)
        self.behind_repo = (self.repo_url_obj.drivername == 'k2assets+repo')
        self.repo_meta = self._fetch_repo_meta()
        self.repo_name = self.repo_url_obj.database
        self.db_port = db_port
        self.rest = rest
        self.debug = debug

        # 日志配置（与父类初始化可能存在重复，但问题不大）
        self.logger = logging.getLogger(self.__class__.__name__)
        if self.debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        # rest情况不需要解析底层数据库连接
        if self.rest:
            return

        # tsf情况不需要sqlalchemy支持
        if self.repo_meta['storage'] == 'tsf':
            return

        self.db_url_obj = self._disclose_db_url()

        self.logger.debug(f"Disclosed url: {str(self.db_url_obj)}")

        super().__init__(self.db_url_obj, schema, debug)

        self.metadata = self._build_engine_meta()

    def get_repo_data(self, start_time: Union[str, int, datetime], end_time: Union[str, int, datetime],
                      devices: list = None,
                      columns: list = None, limit: int = None, desc: bool = None) -> DataFrame:
        """
        查询Repo数据，参数说明可参考K2Assets在线文档的开发者手册的GET repo-data接口，参数值为逗号分隔形式的改为字符串数组形式。
        :param repo_name:
        :param start_time:
        :param end_time:
        :param devices:
        :param columns:
        :param limit:
        :param desc:
        :return:
        """
        repo_name = self.repo_name

        # 统一时间参数类型
        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        elif isinstance(start_time, int):
            start_time = datetime.fromtimestamp(start_time / 1000)
        if isinstance(end_time, str):
            end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        elif isinstance(end_time, int):
            end_time = datetime.fromtimestamp(end_time / 1000)

        # rest和非rest分别处理
        if self.rest:
            result = self._get_repo_data_by_rest(start_time=start_time, end_time=end_time, columns=columns,
                                                 devices=devices,
                                                 limit=limit, desc=desc)
        else:
            # columns参数里暂时不支持表达式（例如 ${col1+col2}）
            if any("${" in s for s in columns):
                raise DataFrameDBException(f"Aviator expression as column is not supported in SDK")

            # 若没有指定schema前缀则添加self.schema前缀
            if (self.schema is not None) and ('.' not in repo_name):
                repo_name = f"{self.schema}.{repo_name}"

            if repo_name in self.metadata.tables:
                table: Table = self.metadata.tables[repo_name]
            else:
                raise DataFrameDBException(f"Table '{repo_name}' does not exist")

            try:
                with self.engine.connect() as conn:
                    query = table.select()
                    if columns:
                        # 检查是否有非法数据列
                        missing_columns = [col for col in columns if col not in table.columns]
                        if missing_columns:
                            raise DataFrameDBException(f"Columns not exist in table: {', '.join(missing_columns)}")
                        # 构造查询列
                        query = query.with_only_columns(*(table.c[col] for col in columns))

                    # 时间过滤条件
                    query = query.where(and_(table.c.k_ts >= int(start_time.timestamp() * 1000),
                                             table.c.k_ts < int(end_time.timestamp() * 1000)))

                    # 设备过滤条件
                    if '*' not in devices:
                        query = query.where(table.c.k_device.in_(devices))

                    # if group_by:
                    #     query = query.group_by(*[text(col) for col in group_by])
                    if desc is not None:
                        if desc:
                            query = query.order_by(table.c.k_ts.desc())
                        else:
                            query = query.order_by(table.c.k_ts.asc())
                    if limit:
                        query = query.limit(limit)

                    if self.behind_repo:
                        # 处理表名和列名小写问题
                        query = traverse(obj=query, opts={},
                                         visitors={"binary": _stmt_lower_case, "textclause": _stmt_lower_case,
                                                   "column": _stmt_lower_case, "table": _stmt_lower_case})

                        if self.engine.name == "postgresql":
                            # 处理原始表里的纳秒，转换为毫秒返回给用户
                            query = traverse(obj=query, opts={},
                                             visitors={"textclause": _pg_modify_timestamp,
                                                       "column": _pg_modify_timestamp,
                                                       "binary": _pg_modify_timestamp})
                            query = query.with_only_columns(*((table.c[col] / literal(1000000)).label('k_ts')
                                                              if col == 'k_ts' else table.c[col] for col in columns))
                        elif self.engine.name == "taos":
                            pass
                        elif self.engine.name == "tsf":
                            pass
                        else:
                            raise DataFrameDBException(f"Unsupported storage: {self.engine.name}")

                    # 执行查询
                    # taospy不处理params（bug? taos\cursor.py line 121），因此这里要预先将params转换到sql里
                    compiled_query = query.compile(compile_kwargs={"literal_binds": True})
                    cursor_result = conn.execute(compiled_query)

                    result = pd.DataFrame(cursor_result.fetchall(), columns=cursor_result.keys())

                    # 恢复列名中的大小写（以repo数据结构中的大小写为准）
                    repo_column_names = [item["name"] for item in self.repo_meta['columns']]
                    rename_dict = {}
                    for repo_col in repo_column_names:
                        if repo_col.lower() in result.columns:
                            rename_dict[repo_col.lower()] = repo_col
                    result.rename(columns=rename_dict, inplace=True)

            except SQLAlchemyError as e:
                raise DataFrameDBException(
                    "Failed to query records due to a database error.",
                    original_exception=e
                )

        # 将k_ts列转为datetime类型 （原始查询结果里是str，原因待查）
        # 手工加毫秒数处理时区问题（pg里是0时区毫秒值），以便得到datetime64类型而非numpy的Timestamp类型
        if not result['k_ts'].dtype.name.startswith('datetime'):
            result['k_ts'] = result['k_ts'].astype(float)
            result['k_ts'] += 8 * 3600 * 1000
            result['k_ts'] = pd.to_datetime(result['k_ts'], unit='ms')

        return result

    def get_repo_file(self, dest_path: str, start_time: Union[str, int, datetime],
                      end_time: Union[str, int, datetime],
                      devices: list = None, limit: int = None, desc: bool = None):
        """
        获取指定repo下的文件，参数说明可参考K2Assets在线文档的开发者手册的GET repo-data接口，参数值为逗号分隔形式的改为字符串数组形式。
        此方法适用于tsf、parquet等文件存储类型的repo，
        :param self:
        :param dest_path: 下载后数据文件的存放路径
        :param start_time:
        :param end_time:
        :param devices:
        :param limit:
        :param desc:
        :return:
        """
        # if self.rest == False:
        #     raise DataFrameDBException("TSF data without REST is not supported yet.")

        # 统一时间参数类型
        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        elif isinstance(start_time, int):
            start_time = datetime.fromtimestamp(start_time / 1000)
        if isinstance(end_time, str):
            end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        elif isinstance(end_time, int):
            end_time = datetime.fromtimestamp(end_time / 1000)

        protocol = self.repo_url_obj.query.get('protocol', 'https')  # k2assets http protocol
        auth = HTTPBasicAuth(self.repo_url_obj.username, self.repo_url_obj.password)
        tenant = self.repo_url_obj.query.get('tenant', None)

        api_base = (f"{protocol}://{self.repo_url_obj.host}{':' if self.repo_url_obj.port else ''}"
                    f"{self.repo_url_obj.port if self.repo_url_obj.port else ''}")
        api_url = (
            f"{api_base}/api/v2/repo-data/{self.repo_url_obj.database}/download"
            f"?deviceIds={','.join(devices)}"
            f"&beginTime={int(start_time.timestamp() * 1000)}&endTime={int(end_time.timestamp() * 1000)}")
        if limit:
            api_url += f'&limit={limit}'
        if desc is not None:
            api_url += f'&desc={"true" if desc else "false"}'
        self.logger.debug(api_url)
        with NamedTemporaryFile() as tmp_zip_file:
            response = k2a_requests.get_stream(api_url, auth=auth, tenant=tenant)
            # 将zip流写入临时文件以避免内存溢出
            for chunk in response.iter_content(chunk_size=8192):
                tmp_zip_file.write(chunk)
            # 解压ZIP文件
            with ZipFile(tmp_zip_file, 'r') as zip_file:
                zip_file.extractall(dest_path)
            # 删除临时zip文件
            os.remove(tmp_zip_file.name)

    def _get_repo_data_by_rest(self, start_time: Union[str, int, datetime], end_time: Union[str, int, datetime],
                               devices: list = None, columns: list = None,
                               limit: int = 100, aggr_function: str = None, aggr_interval: int = None,
                               filter: str = None, value_filter: str = None, desc: bool = None):
        """
        此方法的功能是通过rest api获取指定repo的时序数据，api文档：https://dev.kstonedata.k2/docs/developer-guide/index.html#/api/get-repo-data
        代码内容来自 https://gitlab.kstonedata.k2/data_analysis/k2assets_operators/blob/develop/package_util/k2_magic/handler/RepoHandler.py
        并在原有代码基础上做了重构和增加功能。
        """

        # 统一时间参数类型
        # if isinstance(start_time, str):
        #     start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        # elif isinstance(start_time, int):
        #     start_time = datetime.fromtimestamp(start_time / 1000)
        # if isinstance(end_time, str):
        #     end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        # elif isinstance(end_time, int):
        #     end_time = datetime.fromtimestamp(end_time / 1000)

        columns_str = ','.join(columns)
        device_str = ','.join(devices)

        params = f'columns={columns_str}&deviceIds={device_str}&beginTime={int(start_time.timestamp() * 1000)}&endTime={int(end_time.timestamp() * 1000)}'

        if limit:
            params += f'&limit={limit}'

        if aggr_function:
            params += f'&aggrFunction={aggr_function}'

        if aggr_interval:
            params += f'&aggrInterval={aggr_interval}'

        if value_filter:
            params += f'&valueFilter={value_filter}'

        if filter:
            params += f'&filter={filter}'

        if desc:
            params += '&desc=true'

        params += '&tsFormat=unix'  # 确保返回整数值，以便后面在df里统一转换为datetime类型

        params += '&keepNull=true'  # 表头里保留全空列

        url = self.repo_url_obj
        protocol = url.query.get('protocol', 'https')  # k2assets http protocol
        auth = HTTPBasicAuth(url.username, url.password)
        tenant = url.query.get('tenant', None)
        api_base = f"{protocol}://{url.host}{':' if url.port else ''}{url.port if url.port else ''}"
        api_url = f"{api_base}/api/v2/repo-data/{url.database}?{params}"

        resp = k2a_requests.get(api_url, auth=auth, tenant=tenant)

        ### 将数据从json转换成dataframe
        data_list = []
        for rdata_dict in resp['body']['items']:
            rdata = pd.Series(rdata_dict).to_frame().T
            data_list.append(rdata)

        if not len(data_list):
            df = pd.DataFrame(columns=columns)
        else:
            df = pd.concat(data_list)
            df.index = range(len(df))
        return df

    def _disclose_db_url(self) -> URL:
        """
        将 k2assets+repo:// 开头的 conn_url 转换为底层数据库的 conn_url
        实现方式是先从repo获取元信息，然后让SQLAlchemy直接访问底层数据
        :param repo_db_url: 使用URL类型避免密码明文泄露
        :return:
        """
        if self.repo_url_obj.drivername != 'k2assets+repo':
            raise DataFrameDBException("Not a valid url (k2assets+repo://) to disclose")
        storage = self.repo_meta['storage']
        if storage == 'postgresql':
            jdbc_url = self.repo_meta[
                'jdbc_url']  # e.g. jdbc:postgresql://192.168.132.167:5432/repos?currentSchema=public
            if jdbc_url.startswith('jdbc:'):
                jdbc_url = jdbc_url[5:]
            jdbc_url_obj = make_url(jdbc_url)
            jdbc_url_obj = jdbc_url_obj.set(drivername='postgresql+psycopg2', username=self.repo_meta['jdbc_user'],
                                            password=self.repo_meta['jdbc_password'])
            jdbc_url_obj = jdbc_url_obj.set(query={})  # 否则psycopgs2报错ProgrammingError

            # 解决内部docker服务名称作为host时，在外部无法使用的问题
            # 3.8.1时是postgresql，3.9之后是k2a-postgresql
            # 这里按默认的情况解析host和port，但如果现场情况与默认不相同，则需要现场修改k2a-k2box-service里的环境变量K2BOX_POSTGRESQL_URL
            if jdbc_url_obj.host == 'postgresql' or jdbc_url_obj.host == 'k2a-postgresql' or jdbc_url_obj.host == 'k2a-repos':
                jdbc_url_obj = jdbc_url_obj.set(host=self.repo_url_obj.host, port=15432)

        elif storage == 'TDengine_3':
            jdbc_url = self.repo_meta['jdbc_url']  # e.g. jdbc:TAOS://192.168.132.167:6030/repos
            if jdbc_url.startswith('jdbc:'):
                jdbc_url = jdbc_url[5:]
            jdbc_url_obj = make_url(jdbc_url)
            jdbc_url_obj = jdbc_url_obj.set(drivername='taos', username=self.repo_meta['jdbc_user'],
                                            password=self.repo_meta['jdbc_password'],
                                            database=self.repo_url_obj.database.lower())
            # 解决内部docker服务名称作为host时，在外部无法使用的问题
            if jdbc_url_obj.host == 'tdengine' or jdbc_url_obj.host == 'k2a-tdengine':
                jdbc_url_obj = jdbc_url_obj.set(host=self.repo_url_obj.host)

        elif storage == 'tsf':
            jdbc_url_obj = self.db_url_obj
        else:
            raise DataFrameDBException(f"Unsupported storage: {storage}")

        # 解决docker容器映射到外部端口号变化问题
        if self.db_port:
            jdbc_url_obj = jdbc_url_obj.set(port=self.db_port)

        return jdbc_url_obj

    def _fetch_repo_meta(self) -> dict:
        """
        获取Repo底层数据库的配置信息，如数据库类型、ip地址、用户名等。

        返回结果举例：
        {
          'storage': 'postgresql',
            'jdbc_url': 'jdbc:postgresql://k2a-postgresql:5432/repos?currentSchema=public',
            'jdbc_user': 'k2data',
            'jdbc_password': 'K2data1234',
            'jdbc_conn_pool_size': '20',
            'batch_insert_size': '500',
            'batch_insert_pool_size': '1',
            'key_varchar_len': '256',
            'varchar_len': '1024',
            'completeness_stats_cache': 'true',
            'latest_data_cache': 'true'
        }
        :param url:
        :return:
        """
        url = self.repo_url_obj

        if url.drivername != 'k2assets+repo':
            raise DataFrameDBException("Not a valid url (k2assets+repo://) to fetch")

        result = {}
        protocol = url.query.get('protocol', 'https')  # k2assets http protocol
        auth = HTTPBasicAuth(url.username, url.password)
        tenant = url.query.get('tenant', None)

        api_base = f"{protocol}://{url.host}{':' if url.port else ''}{url.port if url.port else ''}"

        # 获取repo的storage类型，一并放在返回的dict里（key为"storage")
        api_url = f"{api_base}/api/v2/repos/{url.database}"
        data = k2a_requests.get(api_url, auth=auth, tenant=tenant)
        result['storage'] = data.get('body').get('storageInfo').get('name')

        # 获取repo的meta-settings
        api_url = f"{api_base}/api/v2/repos/{url.database}/meta-settings"
        data = k2a_requests.get(api_url, auth=auth, tenant=tenant)
        settings = data.get('body').get('items')

        # 将json里的items转为dict类型
        for item in settings:
            name = item['name']
            pref_value = item['prefValue']
            if pref_value is None:
                pref_value = item['defaultValue']

            # 顺便翻译${}包裹的环境变量，例如${K2BOX_POSTGRESQL_URL}
            pattern = r'\$\{([a-zA-Z0-9_]+)\}'

            def replace(match):
                param_name = match.group(1)
                env_url = f"{api_base}/api/env/{param_name}"
                response2 = k2a_requests.get(env_url, auth=auth, tenant=tenant)
                return response2.get('body').get('values').get(param_name)

            pref_value = re.sub(pattern, replace, pref_value)

            result[name] = pref_value

        # 获取repo的数据结构
        api_url = f"{api_base}/api/v2/repos/{url.database}/columns?from=schema"
        data = k2a_requests.get(api_url, auth=auth, tenant=tenant)
        columns = data.get('body').get('all')
        result['columns'] = columns

        return result

    def _build_engine_meta(self) -> MetaData:
        """
        用Repo里定义的数据结构，构造sqlalchemy engine的metadata对象。实现当Repo与底层数据库不一致时，以Repo数据结构为准的效果。
        例如pg repo里底层数据库是全小写的列名，而用户使用的是repo数据结构的列名可以有大写。
        :param repo_meta:
        :return:
        """
        metadata = MetaData()

        # 在metadata里添加表
        table = Table(self.repo_name, metadata)

        # 遍历json列表中的每个字典
        for column_info in self.repo_meta['columns']:

            # 根据类型创建Column对象
            if column_info['type'] == 'string':
                column = Column(column_info['name'], String)
            elif column_info['type'] == 'long':
                column = Column(column_info['name'], Integer)
            elif column_info['type'] == 'double':
                column = Column(column_info['name'], Float)
            else:
                self.logger.debug(f"Ignored unknown type column {column_info['name']}")

            # 将Column对象添加到对应的Table对象中
            table.append_column(column)
        return metadata


def _pg_modify_timestamp(element):
    """
    将查询里的时间条件转为纳秒（仅pg需要）
    :param element:
    :return:
    """
    # if isinstance(element, Column):
    #     if element.key == 'k_ts':
    #         element.key = 'k_ts/1000000'
    #         element.name = 'k_ts/1000000'
    # 处理where语句里的k_ts过滤条件，非TextClaused的情况
    if isinstance(element, BinaryExpression):
        if element.left.key == 'k_ts':
            element.right = element.right * 1000000
    # 处理where语句里的k_ts过滤条件，TextClaused的情况
    # 对于TextClause类型的过滤条件，只能用正则来识别毫秒时间戳（12~13位数字），添加6个零以后变成纳秒单位
    # if isinstance(element, TextClause):
    #     def add_zeros(match):
    #         number = match.group(0)
    #         return number + '000000'
    #     pattern = r'\b\d{12,13}\b'
    #     element.text = re.sub(pattern, add_zeros, element.text)


def _stmt_lower_case(element):
    """
    将查询里的表名和列名转为小写
    :param element: SQLAlchemy里的sql语法树中的节点
    :return:
    """
    if isinstance(element, Table):
        element.name = element.name.lower()
    if isinstance(element, Column):
        element.name = element.name.lower()
    # if isinstance(element, TextClause):
    #     element.text = element.text.lower()
