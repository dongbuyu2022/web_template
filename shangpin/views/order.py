from flask import Blueprint,session,redirect,render_template,request,flash,jsonify
from ..sql.mysql import order_findall,order_insert
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
        4: {"sta":"失败","col":"danger"},
        5: {"sta":"未知","col":"default"}
    }


    yemian = render_template("order_list.html", data_list=data, status_dict=status_dict)



    return yemian







@ac.route('/order/create',methods = ["GET","POST"])
def create_order():
    user_info = session.get("user_info")
    if not user_info:
        # 验证cookie! 如果不行就跳转--->登录页面
        return redirect('/login')

    if request.method=="GET":
     # 进入到了订单页面
        return render_template('create_order.html')

    #当在得到post提交的表单的时候,
    url = request.form.get("url")
    count = request.form.get("count")

    order_id = order_insert(user_info['id'],user_info['real_name'],url,count,status=1)
    #当订单提交成功,则跳转到订单列表中
    if order_id:

        return redirect('/order/list')
    else:
        flash('后台程序有误!请重新输入订单')  # 发送一次性警告消息
        return redirect('/order/create')  # 重定向回创建订单页面