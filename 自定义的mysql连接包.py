import pymysql
from DBUtils.PooledDB import PooledDB
from loguru import logger


# 自定义连接mysql
class CustomMysql():
    def __init__(self, host, user, passwd, db_name, port, charset):

        self.db_pool = PooledDB(pymysql, 2, host=host, user=user,
                                passwd=passwd, db=db_name, port=port, charset=charset)
        conn = self.db_pool.connection()
        cursor = conn.cursor()

        conn.commit()

    def select_mysql(self, table_name, where_str):
        conn = self.db_pool.connection()
        cursor = conn.cursor()
        # now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        try:
            sql = "select * from {table_name} {where_str}".format(table_name=table_name, where_str=where_str)
            # print(sql)
            cursor.execute(sql)
            datas = cursor.fetchall()
            cursor.close()
            conn.close()
            return datas
        except Exception as e:
            logger.info(" msyql {}".format(e))
            return False

    """
        table_name: 查询表
        search_str: 查询内容
        where_str: 条件
    """

    def select_mysql_many(self, table_name, search_str, where_str):
        conn = self.db_pool.connection()
        cursor = conn.cursor()
        # now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        sql = "set sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';"
        cursor.execute(sql)
        try:
            sql = "select {search_str} from {table_name} {where_str}".format(search_str=search_str,
                                                                             table_name=table_name, where_str=where_str)
            # print(sql)
            cursor.execute(sql)
            datas = cursor.fetchall()
            cursor.close()
            conn.close()
            return datas
        except Exception as e:
            logger.info(" msyql {}".format(e))
            return False

    def select_mysql_count(self, table_name, where_str):
        conn = self.db_pool.connection()
        cursor = conn.cursor()
        # now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        try:
            sql = "select count(*) from {table_name} {where_str}".format(table_name=table_name, where_str=where_str)
            # print(sql)
            cursor.execute(sql)
            numbers = cursor.fetchone()
            cursor.close()
            conn.close()
            return numbers[0]
        except Exception as e:
            logger.info(" msyql {}".format(e))
            return False

    def insert_mysql(self, table_name, datas):

        conn = self.db_pool.connection()
        cursor = conn.cursor()
        nub = 0
        for data in datas:
            keys = ','.join(data.keys())
            values = ','.join(['%s'] * len(data))
            sql = 'insert ignore into {table_name} ({keys}) values({values})'.format(table_name=table_name, keys=keys,
                                                                                     values=values)
            # print(sql)
            try:
                nub_ = cursor.execute(sql, tuple(data.values()))
                conn.commit()
                nub += nub_
            except Exception as e:
                logger.info(" msyql {}".format(e))
                print(data)

        cursor.close()
        conn.close()
        return nub

    def update_mysql(self, sql):
        conn = self.db_pool.connection()
        cursor = conn.cursor()
        try:

            numbers = cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
            return numbers
        except Exception as e:
            logger.info(" msyql {}".format(e))
            return False

