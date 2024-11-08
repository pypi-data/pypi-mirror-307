import importlib
from logging.handlers import TimedRotatingFileHandler

import redis
from flask import current_app
from flask_login import LoginManager
from flask_swagger_ui import get_swaggerui_blueprint

from lesscode_flask.db import db
from lesscode_flask.log.access_log_handler import AccessLogHandler
from lesscode_flask.model.user import AnonymousUser, User
from lesscode_flask.service.authentication_service import get_token_user, get_api_user
from lesscode_flask.utils.swagger.swagger_util import generate_openapi_spec


def setup_logging(app):
    """
    初始化日志配置
    1. 日志等级
        DEBUG : 10
        INFO：20
        WARN：30
        ERROR：40
        CRITICAL：50
    :return:
    """
    import logging
    import sys
    # 日志配置
    # 日志级别
    LOG_LEVEL = app.config.get("LESSCODE_LOG_LEVEL", "DEBUG")
    # 日志格式
    LOG_FORMAT = app.config.get("LESSCODE_LOG_FORMAT",
                                '[%(asctime)s] [%(levelname)s] [%(name)s:%(module)s:%(lineno)d] [%(message)s]')
    # 输出管道
    LOG_STDOUT = app.config.get("LESSCODE_LOG_STDOUT", True)
    # 日志文件备份数量
    LOG_FILE_BACKUPCOUNT = app.config.get("LESSCODE_LOG_FILE_BACKUPCOUNT", 7)
    # 日志文件分割周期
    LOG_FILE_WHEN = app.config.get("LESSCODE_LOG_LOG_FILE_WHEN", "D")
    # 日志文件存储路径
    LOG_FILE_PATH = app.config.get("LESSCODE_LOG_FILE_PATH", 'logs/lesscode.log')
    formatter = logging.Formatter(LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().setLevel(LOG_LEVEL.upper())
    # 控制台输出
    console_handler = logging.StreamHandler(sys.stdout if LOG_STDOUT else sys.stderr)
    console_handler.setFormatter(formatter)
    file_handler = logging.handlers.TimedRotatingFileHandler(LOG_FILE_PATH, when=LOG_FILE_WHEN,
                                                             backupCount=LOG_FILE_BACKUPCOUNT)

    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler)
    logging.getLogger().addHandler(file_handler)
    logging.addLevelName(100, 'ACCESS')

    LESSCODE_ACCESS_LOG_DB = app.config.get("LESSCODE_ACCESS_LOG_DB", 0)
    if LESSCODE_ACCESS_LOG_DB == 1:
        access_log_handler = AccessLogHandler()
        access_log_handler.level = 100
        logging.getLogger().addHandler(access_log_handler)


def setup_blueprint(app, path=None, pkg_name="handlers"):
    import os
    from flask import Blueprint
    import inspect
    """
    动态注册Handler模块
    遍历项目指定包内的Handler，将包内module引入。
    :param path: 项目内Handler的文件路径
    :param pkg_name: 引入模块前缀
    """
    if path is None:
        # 项目内Handler的文件路径，使用当前工作目录作为根
        path = os.path.join(os.getcwd(), pkg_name)
    # 首先获取当前目录所有文件及文件夹
    dynamic_handler_names = os.listdir(path)
    for handler_name in dynamic_handler_names:
        # 利用os.path.join()方法获取完整路径
        full_file = os.path.join(path, handler_name)
        # 循环判断每个元素是文件夹还是文件
        if os.path.isdir(full_file) and handler_name != "__pycache__":
            # 文件夹递归遍历
            setup_blueprint(app, os.path.join(path, handler_name), ".".join([pkg_name, handler_name]))
        elif os.path.isfile(full_file) and handler_name.lower().endswith("handler.py"):
            # 文件，并且为handler结尾，认为是请求处理器，完成动态装载
            module_path = "{}.{}".format(pkg_name, handler_name.replace(".py", ""))
            module = importlib.import_module(module_path)  # __import__(module_path)
            for name, obj in inspect.getmembers(module):
                # 找到Blueprint 的属性进行注册
                if isinstance(obj, Blueprint):
                    # 如果有配置统一前缀则作为蓝图路径的统一前缀
                    if hasattr(obj, "url_prefix") and app.config.get("ROUTE_PREFIX", ""):
                        obj.url_prefix = f'{app.config.get("ROUTE_PREFIX")}{obj.url_prefix}'
                    # 加载完成后 注册蓝图到应用
                    app.register_blueprint(obj)


def setup_query_runner():
    """
    注入数据查询执行器
    :return:
    """
    from redash.query_runner import import_query_runners
    from redash import settings as redash_settings
    import_query_runners(redash_settings.QUERY_RUNNERS)


def setup_sql_alchemy(app):
    """
    配置SQLAlchemy
    :param app:
    :return:
    """
    if app.config.get("SQLALCHEMY_BINDS"): # 确保配置SQLALCHEMY_BINDS才注册SQLAlchemy
        db.init_app(app)


def setup_login_manager(app):
    login_manager = LoginManager(app)
    setattr(app, "login_manager", login_manager)

    @login_manager.request_loader
    def request_loader(request):
        # # 使用token访问的用户
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if token:
            user = get_token_user(token)
            if user:
                return user
        apikey = request.headers.get("API-Key")
        if apikey:
            # 使用AK访问的接口用户
            user = get_api_user(apikey)
            if user:
                return user
        # 无任何用户信息返回 匿名用户
        return AnonymousUser()


def setup_swagger(app):
    """
    配置Swagger
    :param app:
    :return:
    """
    SWAGGER_URL = app.config.get("SWAGGER_URL", "")  # 访问 Swagger UI 的 URL
    # API_URL = 'http://127.0.0.1:5001/static/swagger.json'  # Swagger 规范的路径（本地 JSON 文件）
    API_URL = app.config.get("SWAGGER_API_URL", "")  # 接口
    # 创建 Swagger UI 蓝图
    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI 访问路径
        app.config.get("OUTSIDE_SCREEN_IP") + API_URL,  # Swagger 文件路径
        config={  # Swagger UI 配置参数
            'app_name': "Flask-Swagger-UI 示例"
        }
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    @app.route(API_URL, methods=['GET'])
    def swagger_spec():
        from lesscode_flask import __version__
        swag = generate_openapi_spec(app)
        swag['info']['title'] = app.config.get("SWAGGER_NAME", "")
        swag['info']['description'] = app.config.get("SWAGGER_DESCRIPTION", "")
        swag['info']['version'] = app.config.get("SWAGGER_VERSION", __version__)
        return swag


def setup_redis(app):
    redis_conn_list = app.config.get("DATA_SOURCE", [])

    for r in redis_conn_list:
        if r.get("type") == "redis":
            conn = redis.Redis(host=r.get("host"), port=r.get("port"), db=r.get("db"), password=r.get("password"),
                               decode_responses=True)
            if not hasattr(current_app, "redis_conn_dict"):
                current_app.redis_conn_dict = {}
            if getattr(current_app, "redis_conn_dict").get(r.get("conn_name")):
                raise Exception("Connection {} is repetitive".format(r.get("conn_name")))
            else:
                redis_conn_dict = getattr(current_app, "redis_conn_dict")
                redis_conn_dict.update({
                    r.get("conn_name"): conn
                })
                setattr(current_app, "redis_conn_dict", redis_conn_dict)
