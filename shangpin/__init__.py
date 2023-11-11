from flask import Flask,session,flash






def get_real_name():
    #获取session中的用户名字,作为全局变量,给模版使用
    user_info = session.get("user_info")
    return user_info['real_name']





def create_app():
    app = Flask(__name__)

    #为cookie的session创建密钥
    app.secret_key = 'dhjkff3333565134qjklmx412ppoqjd13?87763*7'

    from .views import user
    from .views import order

    app.register_blueprint(user.ac)
    app.register_blueprint(order.ac)
    app.template_global()(get_real_name)

    return app