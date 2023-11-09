from flask import Blueprint,render_template,request,redirect,session
from ..sql import mysql


#蓝图对象-->登录业务
ac = Blueprint("user",__name__)


@ac.route('/login',methods=["GET","POST"])
def login():

    if request.method =="GET":

        return render_template("login.html",tixing="请输入用户名/密码")


    # 当到了提交时,走一下代码

    role = request.form.get("role")
    pwd = request.form.get("pwd")
    mobile = request.form.get("mobile")
    # real_name = request.form.get("mobile")

    # print(f'人员:{role};  手机号:{mobile};   密码:{pwd}')

    #*******************进入数据库查询*****************************
    result = mysql.users_find_login((role,pwd,mobile))
    if result:
        #"登录成功" --->跳转到其他页面
        # print(result)
        session["user_info"] = {"role":result['role'],"real_name":result['real_name'],"id":result['id']}

        return redirect('/order/list')

    #用户名密码错误-->提示
    return render_template("login.html",error="用户名/密码错误")


@ac.route('/users')
def users():
    return "用户列表"