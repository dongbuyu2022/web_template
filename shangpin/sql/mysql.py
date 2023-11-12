from dbutils.pooled_db import PooledDB
import pymysql
from pymysql import cursors
import logging

'''
**********************************需要修改的地方*********************************************
'''

host = 'localhost'  # 数据库主机地址
port = 3306  # 数据库的端口号
user = 'root'  # 数据库登录用户名
password = '123456'  # 对应的登录密码
database = 'flask'  # 需要连接的数据库名称
charset = 'utf8'  # 数据库字符集（编码）

'''
**********************************需要修改的地方*****************************************
'''







# 定义一个数据库连接池。
pool = PooledDB(
    creator=pymysql,  # 设置数据库模块名称，这里是pymysql
    maxconnections=6,  # 设置连接池中的最大连接数量，值为0或None表示无限制
    mincached=2,  # 设置初始化时，连接池内空闲连接的最少数量，值为0表示不创建任何连接
    maxcached=5,  # 设置连接池空闲的最多连接数量，值为0或None表示无限制
    maxshared=3,  # 设置连接池中的最大共享连接数量，值为0或None表示全部都是共享的
    blocking=True,  # 当连接池中没有可用连接时，是否阻塞等待，值为False则报错
    maxusage=None,  # 设置一个连接最多可以被重复使用（复用）的次数，值为None表示无限制
    setsession=[],  # 设置开始会话前执行的命令列表
    ping=0,  # 设置ping服务器端的选项，作用是检查是否服务器端可用
    host=host, port=port, user=user, password=password, database=database, charset=charset

)


# 示例改进：使用with语句来自动处理连接关闭
def users_find_login(values):
    #登录页面的用户查询
    try:
        with pool.connection() as conn:
            with conn.cursor(cursors.DictCursor) as cursor:
                query = "SELECT * FROM users WHERE role=%s AND password=%s AND mobile=%s"
                cursor.execute(query, values)
                result = cursor.fetchone()
                return result
    except Exception as e:
        logging.error(f"Database error during user login fetch: {e}")
        return None


def order_findall(id,role):
    #根据用户信息,对商品页面的查询,id为用户的id,role为用户属性
    conn = pool.connection()
    # cursor = conn.cursor()
    cursor = conn.cursor(cursors.DictCursor)  # 让他返回一个字典 而不是列表
    #当role=2的时候,表示管理员,就全部返回
    result=[]
    if role==2:

        query = f"select * from orders"
        cursor.execute(query, [])
        result = cursor.fetchall()

    else:
        query = "select * from orders where user_id=%s"
        cursor.execute(query, id)
        result = cursor.fetchall()

    # conn.commit()  #不是增删改,不需要提交事务
    cursor.close()
    conn.close()

    return result

def order_insert(user_id,user_name,url,count,status):
    #根据用户信息,对商品页面的查询,id为用户的id,role为用户属性
    conn = pool.connection()
    cursor = conn.cursor()
    query = f"insert into orders(`user_id`,`user_name`,`url`,`count`,`status`) values(%s,%s,%s,%s,%s)"

    values=[user_id,user_name,url,count,status]
    cursor.execute(query, values)
    conn.commit()  # 不是增删改,不需要提交事务
    cursor.close()
    conn.close()
    AutoAdd_id = cursor.lastrowid     #拿到插入的这个自增id
    return str(AutoAdd_id)  #返回这个自增id


def unexecuted_orders_for_work():
    # 返回status<=2的数据
    # 根据用户信息,对商品页面的查询,id为用户的id,role为用户属性
    conn = pool.connection()
    # cursor = conn.cursor()
    cursor = conn.cursor(cursors.DictCursor)  # 让他返回一个字典 而不是列表
    # 当role=2的时候,表示管理员,就全部返回
    result = []

    query = "select * from orders where status <= %s"
    cursor.execute(query, 2)
    result = cursor.fetchall()


    # conn.commit()  #不是增删改,不需要提交事务
    cursor.close()
    conn.close()

    return result


def update_task_final_in_sql(task):
    conn = pool.connection()  # 假设 `pool` 已经定义为连接池
    cursor = conn.cursor()
    update_query = "UPDATE orders SET status = %s WHERE id = %s"

    try:
        cursor.execute(update_query, (3, task['id']))  # 更新任务status为3
        conn.commit()  # 提交事务
        # print(f"任务ID {task['id']} 的状态已更新为3")
    except Exception as e:
        print("数据库操作出错:", e)
        conn.rollback()  # 出错时回滚
    finally:
        cursor.close()
        conn.close()

