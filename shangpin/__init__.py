from flask import Flask, session, flash

import os

import configparser


def get_real_name():
    # 获取session中的用户名字,作为全局变量,给模版使用
    user_info = session.get("user_info")
    return user_info['real_name']


def create_app():
    app = Flask(__name__)
    # region   读取配置文件ini里面的数据,定义config_dict={}
    # 读取config.ini文件并将配置存储在app.config中
    config = configparser.ConfigParser()
    # 假定config.ini位于与此__init__.py同级的目录中
    config_path = os.path.join( os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.ini')
    config.read(config_path, encoding='utf-8')

    config_dict = {
        "mysql": {},
        "redis": {},
        "secret": {}
    }
    for section in config.sections():
        for key, value in config.items(section):
            config_dict[section][key] = value

    # 将配置直接存入 app.config，这样在应用中就可以全局访问了



    # endregion

    from .sql.mysql import init_db
    from .sql.redis_cache import init_redis_db

    init_db(config_dict["mysql"])  # 初始化mysql数据库连接池
    init_redis_db(config_dict["redis"])  # 初始redis化数据库连接池

    # 为cookie的session创建密钥
    app.secret_key = config_dict['secret']

    from .views import user
    from .views import order

    app.register_blueprint(user.ac)
    app.register_blueprint(order.ac)





    app.template_global()(get_real_name)

    return app
