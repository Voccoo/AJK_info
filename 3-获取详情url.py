from OwnTools.ip import local_redis_ip
from OwnTools.mysql import OperationMysql
from OwnTools.rediss import OperationRedis
from loguru import logger
from parsel import Selector
import requests
import time
from OwnTools.UserAgent import VocUserAgent
import threadpool


class GetInfoUrl:
    def __init__(self):
        self.mysql = OperationMysql(db_name="wph", type=2)
        self.redis = OperationRedis(redis_db=7)
        self.ip = local_redis_ip()
        self.ua = VocUserAgent()
        self.limit_count = 1

    def search_db(self, search_id):
        table_name = "AJK_basics_url"
        search_str = "id,city_name,area_name,basics_name,basics_url"
        where_str = " where id={}".format(search_id)
        datas = self.mysql.select_mysql_many(table_name, search_str, where_str)
        return datas

    def get_html(self, url, referer):
        while 1:
            try:
                proxies = self.ip.ip_https_and_http()
                headers = {
                    'authority': 'www.anjuke.com',
                    'cache-control': 'max-age=0',
                    'upgrade-insecure-requests': '1',
                    'user-agent': self.ua.pc(),
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-user': '?1',
                    'sec-fetch-dest': 'document',
                    'referer': referer,
                    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
                }
                response = requests.get(url, headers=headers,
                                        proxies=proxies,
                                        allow_redirects=False,
                                        timeout=10)
                if response.status_code == 200:
                    # print(response.text)
                    # time.sleep(1000)
                    return Selector(text=response.text)
                else:
                    print(response.text)
                    time.sleep(60)
            except Exception as e:
                # logger.warning(e)
                pass

    def run2(self, search_id):
        # da = self.mysql.select_mysql("AJK_basics_url"," where id={}".format(search_id))
        da = self.search_db(search_id)[0]
        id = da[0]
        city_name = da[1]
        area_name = da[2]
        basics_name = da[3]
        basics_url = da[4] + "o5/"
        page = 1
        # print(basics_url)
        while 1:
            # print(basics_url)
            html = self.get_html(basics_url, da[4])
            details_url_list = html.css("ul.m-house-list > li > a::attr(href)").extract()
            if len(details_url_list) == 0:
                details_url_list = html.css("ul#houselist-mod-new >li a::attr(href)").extract()

            basics_url = html.css("a.aNxt::attr(href)").extract_first()
            item_list = []
            for dul in details_url_list:
                item_list.append({
                    "city_name": city_name,
                    "area_name": area_name,
                    "basics_name": basics_name,
                    "details_url": dul.split("?")[0],
                })

            if basics_url is not None:
                in_result = self.mysql.insert_mysql("AJK_details_url", item_list)
                logger.info(
                    "获取ID【{}】，城市【{}】，区域【{}】，基本名【{}】，第【{}】页，共【{}/{}】条数据--【下一页】".format(id,
                                                                                      city_name, area_name,
                                                                                      basics_name, page,
                                                                                      in_result,
                                                                                      len(details_url_list)))
                page += 1
            else:
                logger.info(
                    "获取ID【{}】，城市【{}】，区域【{}】，基本名【{}】，第【{}】页，共【{}】条数据--【结束】".format(id, city_name, area_name,
                                                                                  basics_name, page,
                                                                                  len(details_url_list)))
                break
        up_sql = "update AJK_basics_url set status=1 where id={}".format(id)
        up_result = self.mysql.update_mysql(up_sql)
        logger.info("ID是【{}】，城市【{}】，区域【{}】，基本【{}】，修改结果【{}】".format(id, city_name, area_name, basics_name, up_result))

    def run(self):
        datas = self.mysql.select_mysql_many("AJK_basics_url", "id", " where status = 0")
        task_param_list = []
        count_ = int(input('请输入要开启的线程数量：'))
        # count_ = 1
        for i in datas:
            task_param_list.append(i[0])
        pool = threadpool.ThreadPool(count_)
        reqs = threadpool.makeRequests(self.run2, task_param_list)
        for req in reqs:
            pool.putRequest(req)
        pool.wait()


if __name__ == '__main__':
    giu = GetInfoUrl()
    giu.run()
