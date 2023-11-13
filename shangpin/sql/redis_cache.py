import redis
import json
from redis.exceptions import ResponseError
import logging

# 创建连接池
# 参数说明:
# host: Redis服务器的地址，默认为localhost
# port: Redis服务器的端口，默认为6379
# db: 要访问的数据库号，默认为0
# max_connections: 连接池允许的最大连接数，超过这个数就会等待，而不是立即得到一个连接，默认没有限制


pool=None


import redis

def init_redis_db(config):
    # 初始化连接redis池

    global pool

    # 使用字典解包的方式传递配置参数
    pool_kwargs = {
        'host': config['host'],
        'port': int(config['port']),
        'db': 0,
        'max_connections': 10,
        'decode_responses': True
    }

    # 如果有密码就添加密码,没有就不添加
    if 'password' in config and config['password']:
        pool_kwargs['password'] = config['password']



    pool = redis.ConnectionPool(**pool_kwargs)


# push_queue 函数，把列表中的每个订单单独推入Redis队列：
def push_queue(value):
    # 创建Redis连接对象，使用的时候会从连接池中获取连接
    r = redis.Redis(connection_pool=pool)
    for item in value:  # 迭代传入的列表
        item_de = json.dumps(item)  # 对单个订单进行编码
        r.lpush('work', item_de)  # 将编码后的单个订单推入队列


# 示例改进：异常处理和日志记录
def pop_queue():
    r = redis.Redis(connection_pool=pool)
    while True:
        try:
            task_json = r.rpop('work')
            if task_json:
                yield json.loads(task_json)
            else:
                logging.info("队列为空，等待/生成新任务.")
                break
        except Exception as e:
            logging.error(f"redis提取页面`pop_queue`出现问题: {e}")
            continue  # 继续尝试下一个工作，而不是退出循环








def work_pop_queue(task):
    # 为Run_in_BackGround提取任务
    r = redis.Redis(connection_pool=pool)
    result = r.brpop(task, timeout=10)

    if result:
        # result可能是(key, value)格式的元组，这里我们只需要第二个元素
        _, data = result  # 使用"_"来忽略不需要的第一个元素（队列的名称）

        # 确保数据是字符串，之后再加载，如果需要可以增加额外的错误处理
        if isinstance(data, bytes):
            data = data.decode('utf-8')  # 或使用你知道用于编码的具体编码

        # data现在应该是一个JSON格式的字符串，可以被loads
        value_obj = json.loads(data)
        return value_obj
    else:
        # 如果没有数据返回，可以选择返回None或者其他值或者抛出异常
        return None



def find_order_in_redis():
    r = redis.Redis(connection_pool=pool)

    keys = r.keys('*')

    for key in keys:
        try:
            # 检查该key是否有值，不管它的类型是什么
            if r.exists(key):

                return key
        except ResponseError as e:
            # 在这里处理异常情况或记录日志
            logging.error(f"redis查询订单`find_order_in_redis`出现问题: {e}")
            continue
    return None





