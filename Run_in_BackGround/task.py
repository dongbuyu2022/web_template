import logging
import time
from shangpin.sql.redis_cache import work_pop_queue, find_order_in_redis, push_queue, pop_queue
from shangpin.sql.mysql import unexecuted_orders_for_work, update_task_final_in_sql

# 设置日志记录配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def find_in_sql_order_add_redis():
    try:
        data = unexecuted_orders_for_work()
    except Exception as e:
        logging.error(f"Error fetching unexecuted orders: {e}")
        return

    if not data:
        time.sleep(5)  # 调整为更合适的时间，根据实际情况
        return

    # 添加到Redis队列中
    push_queue(data)

    for task in pop_queue():
        try:
            print(f"id为:{task['id']}的订单--->已完成!!")  # 这里应该是调用实际处理函数，而不是打印
            time.sleep(1)  # 这里的休眠也可以根据处理任务的实际耗时调整
            update_task_final_in_sql(task)
        except Exception as e:
            logging.error(f"Error processing task {task['id']}: {e}")

def decode_redis():
    try:
        task = find_order_in_redis()
    except Exception as e:
        logging.error(f"Error finding order in Redis: {e}")
        return None

    if not task:
        return None

    # 运行订单
    try:
        data = work_pop_queue(task)
        return data
    except Exception as e:
        logging.error(f"Error popping work from queue: {e}")
        return None

def run():
    while True:
        order_id = decode_redis()
        if not order_id:
            deal = find_in_sql_order_add_redis()
            if not deal:
                print("目前已经没有订单了")
                time.sleep(2)  # 调整为更合适的时间，依据实际情况而定
            continue
        print('正在等待数据生成...')
        time.sleep(1)  # 也可以调整，或者改为更复杂的逻辑


if __name__ == '__main__':
    run()
