from flask import Blueprint,session,redirect,render_template
from ..sql.mysql import order_findall
#蓝图对象
ac = Blueprint("order",__name__)


@ac.route('/order/list')
def login():
    #读取用户的cookie and 解密获取
    user_info = session.get("user_info")

    if not user_info:
        #验证cookie! 如果不行就跳转--->登录页面
        return redirect('/login')
    #进入到了订单页面

    data =order_findall(user_info['id'],user_info['role'])
    #状态码的转中文
    status_dict={
        1:'等待',
        2:"正在运行",
        3:"完成",
        4:"失败"
    }
    print(data[0]['user_name'])



    yemian = render_template("order_list.html",data_list = data, status_dict=status_dict)


    return yemian

@ac.route('/order/create')
def users():
    return "创建订单"