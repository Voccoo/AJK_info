# from OwnTools.time import Time
import redis
import json



class OperationRedis():
    def __init__(self, redis_db):
        # self.debug = 'Yes'
        self.debug = 'No'
        # self.ti = Time()
        # ++++++++++Redis配置参数++++++++++++
        redis_host = 'localhost'
        redis_password = 'Cs123456.'
        redis_port = 6379
        self.redis_conn = redis.ConnectionPool(host=redis_host,
                                               password=redis_password,
                                               port=redis_port,
                                               db=redis_db
                                               )

    def insert_redis(self, redis_key, datas):
        """
                传入的datas为（tuple）,根据内容循环获取里面详细的内容，
                组成一个新的dict变量，并通过redis的rpush函数，插入到指定key下
                :param datas:
                :return:
                """
        r_insert_ = redis.Redis(connection_pool=self.redis_conn)
        # r_insert_ = redis.StrictRedis(host='localhost', password='Cs123456.', port=6379, db=2)

        try:
            for data in datas:
                # 需要生动配置每一个需要插入的数据对应的dict数据key和value
                r_insert_.rpush(redis_key, json.dumps(data))
            # result = '--{}--插入成功--{}--条--'.format(self.ti.now_time(), len(datas))
            r_insert_.connection_pool.disconnect()
            return len(datas)
        except Exception as e:
            if self.debug == 'Yes':
                print(e)
            return '--Error：数据添加方法[insert_redis]出现错误--{}--'.format(e)

    def count_redis(self, redis_key):
        try:
            r = redis.Redis(connection_pool=self.redis_conn)
            # 另外一种连接方式
            # r = redis.StrictRedis(host='localhost', password='Cs123456.', port=6379, db=2)
            count_nub = r.llen(redis_key)
            r.connection_pool.disconnect()
            return count_nub
        except Exception as e:
            if self.debug == 'Yes':
                print(e)

            return '--Error：数据添加方法[count_redis]出现错误--{}--'.format(e)

    def insert_redis_lpush(self, redis_key, datas):
        """
                传入的datas为（tuple）,根据内容循环获取里面详细的内容，
                组成一个新的dict变量，并通过redis的rpush函数，插入到指定key下
                :param datas:
                :return:
                """
        r_insert_ = redis.Redis(connection_pool=self.redis_conn)
        # r_insert_ = redis.StrictRedis(host='localhost', password='Cs123456.', port=6379, db=2)

        try:
            for data in datas:
                # 需要生动配置每一个需要插入的数据对应的dict数据key和value
                r_insert_.lpush(redis_key, json.dumps(data))
            result = '--{}--插入成功--{}--条--'.format(self.ti.now_time(), len(datas))
            r_insert_.connection_pool.disconnect()
            return result
        except Exception as e:
            if self.debug == 'Yes':
                print(e)
            return '--Error：数据添加方法[insert_redis]出现错误--{}--'.format(e)

    def get_info(self, redis_key):
        try:
            r = redis.Redis(connection_pool=self.redis_conn)
            redis_info = json.loads(r.blpop(redis_key)[1].decode('UTF-8').replace(' ', ''))
            return redis_info
        except Exception as e:
            if self.debug == 'Yes':
                print(e)

            return '--Error：数据添加方法[get_info]出现错误--{}--'.format(e)