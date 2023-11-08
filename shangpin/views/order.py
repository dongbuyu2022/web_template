from flask import Blueprint,session,redirect

#蓝图对象
ac = Blueprint("order",__name__)


@ac.route('/order/list')
def login():
    #读取用户的cookie and 解密获取
    user_info = session.get("user_info")
    if not user_info:
        #验证cookie! 如果不行就跳转--->登录页面
        return redirect('/login')
    return "订单列表"

@ac.route('/order/create')
def users():
    return "创建订单"