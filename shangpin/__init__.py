from flask import Flask

def create_app():
    app = Flask(__name__)

    #为cookie的session创建密钥
    app.secret_key = 'dhjkff3333565134qjklmx412ppoqjd13?87763*7'

    from .views import user
    from .views import order

    app.register_blueprint(user.ac)
    app.register_blueprint(order.ac)

    return app