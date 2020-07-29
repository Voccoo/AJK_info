import requests
from parsel import Selector


class GetCity:
    def __init__(self):
        pass

    def run(self):
        headers = {
            'authority': 'www.anjuke.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://xuzhou.anjuke.com/',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cookie': 'sessid=CB9A3C5F-D9A9-035B-7A47-7CC88E1884AA; aQQ_ajkguid=ABF9B0F6-B0BF-57FC-8D66-F0C9BF99EE0B; lps=http%3A%2F%2Fwww.anjuke.com%2F%7Chttps%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DvvMyyPrYLE_8yjJHgKXBBkpw0_WlMDqf8tap2myswAazJcUPKwY3yUS7Ub0V_8bs%26wd%3D%26eqid%3D944677fb00052a3c000000045f058b02; twe=2; id58=e87rkF8Fiwav1kQ7BiBTAg==; _gid=GA1.2.731607766.1594198792; _ga=GA1.2.931641422.1594198792; 58tj_uuid=9dc7ce16-7d65-45ae-9fff-3f8962245bd7; als=0; ajk_member_captcha=3e54a5aa069a420c3cf5ba3d4b506d65; wmda_uuid=dececd079974425d0f5b73facdb2cb09; wmda_new_uuid=1; wmda_visited_projects=%3B6289197098934; propertys=2cy1q26-qd6kdb_2ctqivy-qd6jv8_2ceva5n-qd6jsj_2cqumgk-qd6jqp_2bx2c06-qd6jep_xutm59-qd57nx_; init_refer=https%253A%252F%252Fwww.baidu.com%252Flink%253Furl%253DIjcf35JcjNmwwLUOdOsvw_u6Yn7sF27IL6HjPnz-IAcy8_oBIDhE_QBQbv_R20Dy%2526wd%253D%2526eqid%253Dc80932ae001ab717000000045f06b166; new_uv=4; new_session=0; wmda_session_id_6289197098934=1594274185379-175e3e05-315d-0799; ctid=107; xxzl_cid=c371f576d26741068bd782dfeea7afd8; xzuid=6af2fc8b-71db-48b9-bce6-acbb3beb0385',
        }

        response = requests.get('https://www.anjuke.com/sy-city.html', headers=headers)
        html = Selector(text=response.text)
        url_list = html.css("div.letter_city > ul > li > div.city_list > a::attr(href)").extract()
        print(url_list)
        print(len(url_list))

if __name__ == '__main__':
    gt = GetCity()
    gt.run()
