from flask import Blueprint,session,redirect,render_template
from ..sql.mysql import order_findall
#蓝图对象
ac = Blueprint("order",__name__)


@ac.route('/order/list')
def order_list():
    #读取用户的cookie and 解密获取
    user_info = session.get("user_info")

    if not user_info:
        #验证cookie! 如果不行就跳转--->登录页面
        return redirect('/login')
    #进入到了订单页面

    data =order_findall(user_info['id'],user_info['role'])
    #状态码的转中文/颜色
    status_dict={
        1: {"sta":'等待',"col":"warning"},
        2: {"sta":"正在运行","col":"info"},
        3: {"sta":"完成","col":"success"},
        4: {"sta":"失败","col":"danger"}
    }
    print(data[0]['user_name'])



    yemian = render_template("order_list.html",data_list = data, status_dict=status_dict)


    return yemian

@ac.route('/order/create')
def create_order():
    # 读取用户的cookie and 解密获取
    user_info = session.get("user_info")

    if not user_info:
        # 验证cookie! 如果不行就跳转--->登录页面
        return redirect('/login')
    # 进入到了订单页面

    data = order_findall(user_info['id'], user_info['role'])

    return render_template('create_order.html',data_list = data)