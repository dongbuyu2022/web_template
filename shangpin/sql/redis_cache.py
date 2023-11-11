import redis
import json

# 创建连接池
# 参数说明:
# host: Redis服务器的地址，默认为localhost
# port: Redis服务器的端口，默认为6379
# db: 要访问的数据库号，默认为0
# max_connections: 连接池允许的最大连接数，超过这个数就会等待，而不是立即得到一个连接，默认没有限制
pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    db=0,
    max_connections=10,
    encoding='utf-8',
    decode_responses=True
)
def push_queue(value):
    # 创建Redis连接对象，使用的时候会从连接池中获取连接
    r = redis.Redis(connection_pool=pool)
    #json.dumps(value)--->对value进行编码,怕他格式有问题
    r.lpush('que',json.dumps(value))

def pushed_value():
    # 创建Redis连接对象，使用的时候会从连接池中获取连接
    r = redis.Redis(connection_pool=pool)
    # 从队列中获取最新的元素
    last_value = r.lindex('que', 0)
    # 打印最新的元素
    if last_value is not None:
        # 假设存储的是JSON字符串，需要解码成Python对象
        value_obj = json.loads(last_value)
        print(value_obj)
    else:
        print("队列为空")




