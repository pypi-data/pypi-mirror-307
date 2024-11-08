import os
import sys

from flask import current_app

from lesscode_flask.utils.helpers import get_start_port


class BaseConfig:
    # 应用名称
    APPLICATION_NAME: str = ""
    # 应用id
    CLIENT_ID: str = ""
    # 项目名称
    PROJECT_NAME: str = ""
    # 统一路由前缀
    ROUTE_PREFIX = ""
    # 项目端口号
    PORT = 5002

    # 数据源
    DATA_SOURCE = []
    # SQLALCHEMY数据库连接
    SQLALCHEMY_BINDS = {
        # 'users': 'mysqldb://localhost/users',
        # 'appmeta': 'sqlite:////path/to/appmeta.db'
    }

    # 日志级别
    LESSCODE_LOG_LEVEL = os.environ.get("LESSCODE_LOG_LEVEL", "INFO")
    # 日志格式
    LESSCODE_LOG_FORMAT = os.environ.get("LESSCODE_LOG_FORMAT",
                                         '[%(asctime)s] [%(levelname)s] [%(name)s:%(module)s:%(lineno)d] [%(message)s]')
    # 输出管道
    LESSCODE_LOG_STDOUT = os.environ.get("LESSCODE_LOG_STDOUT", True)
    # 日志文件备份数量
    LESSCODE_LOG_FILE_BACKUPCOUNT = os.environ.get("LESSCODE_LOG_FILE_BACKUPCOUNT", 7)
    # 日志文件分割周期
    LESSCODE_LOG_LOG_FILE_WHEN = os.environ.get("LESSCODE_LOG_LOG_FILE_WHEN", "D")
    # 日志文件存储路径
    LESSCODE_LOG_FILE_PATH = os.environ.get("LESSCODE_LOG_FILE_PATH", 'logs/lesscode.log')
    # 访问日志是否DB存储
    LESSCODE_ACCESS_LOG_DB = os.environ.get("LESSCODE_ACCESS_LOG_DB", 0)
    # 未配置权限的资源 默认权限  1：需要登录 0：游客'
    AUTH_DEFAULT_ACCESS = 0

    # 外网地址
    OUTSIDE_SCREEN_IP: str = "http://127.0.0.1:{}".format(get_start_port())
    SWAGGER_URL = '{}/swagger-ui'.format(ROUTE_PREFIX)
    SWAGGER_API_URL = '{}/swagger'.format(ROUTE_PREFIX)
    NOT_RESPONSE_RESULT = [SWAGGER_URL, SWAGGER_API_URL]
    # # 项目端口号
    # PORT: int = 8080
    #
    # 应用运行根路径
    # APPLICATION_PATH: str = f"{os.path.abspath(os.path.dirname(sys.argv[0]))}"
    # # 静态资源目录
    STATIC_PATH: str = f"{os.path.abspath(os.path.dirname(sys.argv[0]))}"
    #
    # # 是否启动资源注册
    # RMS_REGISTER_ENABLE: bool = False
    # # 注册地址
    # RMS_REGISTER_SERVER: str = "http://127.0.0.1:8918"
    #
    SECRET_KEY = "423ad5ef841bbd073b415e4ba4136d7c94cac3f5e9bfeec1a21da35cd9ea6b46"
    # redis缓存开关
    CACHE_ENABLE: bool = False
    REDIS_CACHE_KEY = "redis"
    REDIS_OAUTH_KEY = "redis"
    AUTHORIZATION_ENABLE: bool = False
    #
    # # 外网地址
    # OUTSIDE_SCREEN_IP: str = ""
    # # 内网ip
    # INSTANCE_IP: str = ""
    #
    # 数据服务
    CAPABILITY_PLATFORM_SERVER: str = "http://127.0.0.1:8976"
    # # 权限服务地址
    # OAUTH_SERVER: str = ""
    # # 后端管理地址
    # UPMS_SERVER: str = ""
    # # 报告服务地址
    # REPORT_SERVER: str = ""
    #
    # # aes加密key
    # AES_KEY: str = 'haohaoxuexi'
    # ks3连接配置
    # host ks3的地址; access_key_id ks3的key; access_key_secret ks3的密钥 is_secure 是否使用https协议
    KS3_CONNECT_CONFIG: dict = {"bucket_name": "", "host": "", "access_key_id": "", "access_key_secret": "",
                                "is_secure": False}
    # request请求的参数
    CONNECT_CONFIG: dict = {
        # "pool_connections": 10,
        # "pool_maxsize": 100,
        # "max_retries": 1,
        # "pool_block": False
    }
    #
    # # mysql ip地址
    # MYSQL_IP: str = ""
    # # mysql 端口号
    # MYSQL_PORT: str = ""
    # # mysql 用户名
    # MYSQL_USERNAME: str = ""
    # # mysql 用户密码
    # MYSQL_PASSWORD: str = ""
    #
    # # clickhouse ip地址
    # CK_IP: str = ""
    # # clickhouse 端口号
    # CK_PORT: str = ""
    # # clickhouse 用户名
    # CK_USERNAME: str = ""
    # # clickhouse 密码
    # CK_PASSWORD: str = ""

    # swagger 的名称
    SWAGGER_NAME = "API"
    # swagger 的版本
    SWAGGER_VERSION = "1.0.0"
    # swagger 的描述
    SWAGGER_DESCRIPTION = "项目接口说明文档"
