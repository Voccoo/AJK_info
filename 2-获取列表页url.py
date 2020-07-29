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

    def deal_str(self, str_where):
        if str_where is None:
            return str_where
        else:
            return str_where.replace("\t", "").replace("\n", "").replace(" ", "")

    def run2(self, s_url):
        url_1 = "{}/sale/".format(s_url)
        html_area = self.get_html(url_1, s_url)
        # "#switch_apf_id_7 > span.city"
        city_name = html_area.css("div.cur_citynew >div:nth-child(1) > span.city::text").extract_first()
        # "#switch_apf_id_7 > span.city"
        # print(city_name)
        if city_name is None or city_name == "":
            # print("1111111111111")
            city_name = html_area.css("div#switch_apf_id_5::text").extract_first()
        print("{}---{}".format(city_name, s_url))
        area_url_list = html_area.css("div.div-border.items-list>div:nth-child(1)>span>a")
        # if len(area_url_list) == 0:
        #     area_url_list = html_area.css("")
        item_list = []

        for aul in area_url_list:
            area_name = aul.css("::text").extract_first()
            quart_url = aul.css("::attr(href)").extract_first()
            # print(quart_url)
            # print(area_name)
            html_quart = self.get_html(quart_url, url_1)
            basics_el = html_quart.css("div.sub-items>a")
            for bel in basics_el:
                basics_url = bel.css("::attr(href)").extract_first()
                basics_name = bel.css("::text").extract_first()
                # print(basics_url)
                # print(basics_name)

                item_list.append({
                    "city_name": self.deal_str(city_name),
                    "area_name": self.deal_str(area_name),
                    "basics_name": self.deal_str(basics_name),
                    "basics_url": self.deal_str(basics_url),
                })
        if len(item_list) > 0:
            in_result = self.mysql.insert_mysql("AJK_basics_url", item_list)
            logger.info("城市【{}】，增加基础URL【{}】条".format(city_name, in_result))
        else:
            with open("获取数据异常.txt", "a", encoding="utf-8") as f:
                f.write("{} \n".format(s_url))

    def run(self):
        start_url = [
            'https://anshan.anjuke.com','https://chifeng.anjuke.com',
            'https://anyang.anjuke.com', 'https://anqing.anjuke.com',
            'https://ankang.anjuke.com',
            'https://anshun.anjuke.com', 'https://aba.anjuke.com','https://akesu.anjuke.com',
            'https://ali.anjuke.com', 'https://alaer.anjuke.com',
            'https://alashanmeng.anjuke.com', 'https://aomen.anjuke.com', 'https://anqiu.anjuke.com',
            'https://anning.anjuke.com', 'https://beijing.anjuke.com', 'https://baoding.anjuke.com',
            'https://baotou.anjuke.com', 'https://binzhou.anjuke.com', 'https://baoji.anjuke.com',
            'https://bengbu.anjuke.com', 'https://benxi.anjuke.com', 'https://beihai.anjuke.com','https://bayinguoleng.anjuke.com',
             'https://bazhong.anjuke.com', 'https://bayannaoer.anjuke.com',
            'https://bozhou.anjuke.com', 'https://baiyin.anjuke.com', 'https://baicheng.anjuke.com',
            'https://baise.anjuke.com', 'https://baishan.anjuke.com', 'https://boertala.anjuke.com',
            'https://bijie.anjuke.com', 'https://baoshan.anjuke.com', 'https://bazh.anjuke.com',
            'https://beipiao.anjuke.com', 'https://beiliu.anjuke.com', 'https://chengdu.anjuke.com',
            'https://chongqing.anjuke.com', 'https://cs.anjuke.com', 'https://cz.anjuke.com',
            'https://cc.anjuke.com', 'https://cangzhou.anjuke.com', 'https://changji.anjuke.com',
            'https://changde.anjuke.com', 'https://chenzhou.anjuke.com',
            'https://chengde.anjuke.com', 'https://changzhi.anjuke.com',
            'https://chizhou.anjuke.com',
            'https://chuzhou.anjuke.com', 'https://chaoyang.anjuke.com', 'https://chaozhou.anjuke.com',
            'https://chuxiong.anjuke.com', 'https://chaohu.anjuke.com', 'https://changdu.anjuke.com',
            'https://changge.anjuke.com', 'https://chongzuo.anjuke.com', 'https://changshushi.anjuke.com',
            'https://chibi.anjuke.com', 'https://cengxi.anjuke.com', 'https://cixi.anjuke.com',
            'https://chongzhou.anjuke.com', 'https://dalian.anjuke.com', 'https://dg.anjuke.com',
            'https://deyang.anjuke.com', 'https://dali.anjuke.com', 'https://dezhou.anjuke.com',
            'https://dongying.anjuke.com', 'https://daqing.anjuke.com', 'https://dandong.anjuke.com',
            'https://datong.anjuke.com', 'https://dazhou.anjuke.com', 'https://dafeng.anjuke.com',
            'https://dehong.anjuke.com', 'https://dingzhou.anjuke.com', 'https://diqing.anjuke.com',
            'https://dingxi.anjuke.com', 'https://dxanling.anjuke.com', 'https://dongtai.anjuke.com',
            'https://dengzhou.anjuke.com', 'https://dongfang.anjuke.com', 'https://danzhou.anjuke.com',
            'https://danyang.anjuke.com', 'https://dengta.anjuke.com', 'https://dunhuang.anjuke.com',
            'https://daye.anjuke.com', 'https://duyun.anjuke.com', 'https://dongyang.anjuke.com',
            'https://dujiangyan.anjuke.com', 'https://eerduosi.anjuke.com', 'https://enshi.anjuke.com',
            'https://ezhou.anjuke.com', 'https://enping.anjuke.com', 'https://emeishan.anjuke.com',
            'https://foshan.anjuke.com', 'https://fz.anjuke.com', 'https://fuyang.anjuke.com',
            'https://fushun.anjuke.com', 'https://fuxin.anjuke.com', 'https://fuzhoushi.anjuke.com',
            'https://fangchenggang.anjuke.com', 'https://feichengshi.anjuke.com',
            'https://fengchengshi.anjuke.com', 'https://fuqing.anjuke.com', 'https://fuan.anjuke.com',
            'https://fuding.anjuke.com', 'https://guangzhou.anjuke.com', 'https://gy.anjuke.com',
            'https://guilin.anjuke.com', 'https://ganzhou.anjuke.com', 'https://guangan.anjuke.com',
            'https://guigang.anjuke.com', 'https://guangyuan.anjuke.com', 'https://ganzi.anjuke.com',
            'https://gannan.anjuke.com', 'https://guantao.anjuke.com', 'https://guoluo.anjuke.com',
            'https://guyuan.anjuke.com', 'https://gongzhulingshi.anjuke.com', 'https://gaoyou.anjuke.com',
            'https://gaomishi.anjuke.com', 'https://geermu.anjuke.com', 'https://guanghan.anjuke.com',
            'https://guiping.anjuke.com', 'https://gaoanshi.anjuke.com', 'https://gaobeidian.anjuke.com',
            'https://hangzhou.anjuke.com', 'https://hf.anjuke.com', 'https://heb.anjuke.com',
            'https://haikou.anjuke.com', 'https://huizhou.anjuke.com', 'https://handan.anjuke.com',
            'https://huhehaote.anjuke.com', 'https://huanggang.anjuke.com', 'https://huainan.anjuke.com',
            'https://huangshan.anjuke.com', 'https://hebi.anjuke.com', 'https://hengyang.anjuke.com',
            'https://huzhou.anjuke.com', 'https://hengshui.anjuke.com', 'https://hanzhong.anjuke.com',
            'https://huaian.anjuke.com', 'https://huangshi.anjuke.com', 'https://heze.anjuke.com',
            'https://huaihua.anjuke.com', 'https://huaibei.anjuke.com', 'https://huludao.anjuke.com',
            'https://heyuan.anjuke.com', 'https://honghe.anjuke.com', 'https://hami.anjuke.com',
            'https://hegang.anjuke.com', 'https://hulunbeier.anjuke.com', 'https://haibei.anjuke.com',
            'https://haidong.anjuke.com', 'https://hainan.anjuke.com', 'https://hechi.anjuke.com',
            'https://heihe.anjuke.com', 'https://hexian.anjuke.com', 'https://hezhou.anjuke.com',
            'https://hailaer.anjuke.com', 'https://huoqiu.anjuke.com', 'https://hetian.anjuke.com',
            'https://huangnan.anjuke.com', 'https://hexi.anjuke.com', 'https://heshan.anjuke.com',
            'https://haicheng.anjuke.com', 'https://huanghua.anjuke.com', 'https://hejian.anjuke.com',
            'https://hancheng.anjuke.com', 'https://hanchuanshi.anjuke.com', 'https://haimen.anjuke.com',
            'https://haining.anjuke.com', 'https://haiyang.anjuke.com', 'https://jinan.anjuke.com',
            'https://jx.anjuke.com', 'https://jilin.anjuke.com', 'https://jiangmen.anjuke.com',
            'https://jingmen.anjuke.com', 'https://jinzhou.anjuke.com', 'https://jingdezhen.anjuke.com',
            'https://jian.anjuke.com', 'https://jining.anjuke.com', 'https://jinhua.anjuke.com',
            'https://jieyang.anjuke.com', 'https://jinzhong.anjuke.com', 'https://jiujiang.anjuke.com',
            'https://jiaozuo.anjuke.com', 'https://jincheng.anjuke.com', 'https://jingzhou.anjuke.com',
            'https://jiamusi.anjuke.com', 'https://jiuquan.anjuke.com', 'https://jixi.anjuke.com',
            'https://jiyuan.anjuke.com', 'https://jinchang.anjuke.com', 'https://jiayuguan.anjuke.com',
            'https://jiangyin.anjuke.com', 'https://jingjiang.anjuke.com', 'https://jianyangshi.anjuke.com',
            'https://jintan.anjuke.com', 'https://jishou.anjuke.com', 'https://jinghong.anjuke.com',
            'https://jinjiangshi.anjuke.com', 'https://jianou.anjuke.com', 'https://jiaozhoux.anjuke.com',
            'https://jurong.anjuke.com', 'https://jiangyoushi.anjuke.com', 'https://km.anjuke.com',
            'https://ks.anjuke.com', 'https://kaifeng.anjuke.com', 'https://kashi.anjuke.com',
            'https://kelamayi.anjuke.com', 'https://kenli.anjuke.com', 'https://lezilesu.anjuke.com',
            'https://kuerle.anjuke.com', 'https://kaili.anjuke.com', 'https://kaiping.anjuke.com',
            'https://lanzhou.anjuke.com', 'https://langfang.anjuke.com', 'https://luoyang.anjuke.com',
            'https://liuzhou.anjuke.com', 'https://laiwu.anjuke.com', 'https://luan.anjuke.com',
            'https://luzhou.anjuke.com', 'https://lijiang.anjuke.com',
            'https://linyi.anjuke.com',
            'https://liaocheng.anjuke.com', 'https://lianyungang.anjuke.com', 'https://lishui.anjuke.com',
            'https://loudi.anjuke.com', 'https://leshan.anjuke.com', 'https://liaoyang.anjuke.com',
            'https://lasa.anjuke.com', 'https://linfen.anjuke.com', 'https://longyan.anjuke.com',
            'https://luohe.anjuke.com', 'https://liangshan.anjuke.com', 'https://liupanshui.anjuke.com',
            'https://liaoyuan.anjuke.com', 'https://laibin.anjuke.com', 'https://lingcang.anjuke.com',
            'https://linxia.anjuke.com', 'https://linyishi.anjuke.com', 'https://linzhi.anjuke.com',
            'https://longnan.anjuke.com', 'https://lvliang.anjuke.com', 'https://linhaishi.anjuke.com',
            'https://longhaishi.anjuke.com', 'https://lilingshi.anjuke.com', 'https://linqing.anjuke.com',
            'https://longkou.anjuke.com', 'https://laiyang.anjuke.com', 'https://leiyang.anjuke.com',
            'https://liyang.anjuke.com', 'https://lingyuan.anjuke.com', 'https://lingbaoshi.anjuke.com',
            'https://lengshuijiang.anjuke.com', 'https://lianyuan.anjuke.com', 'https://lufengshi.anjuke.com',
            'https://luoding.anjuke.com', 'https://lepingshi.anjuke.com', 'https://laizhoushi.anjuke.com',
            'https://laixi.anjuke.com', 'https://mianyang.anjuke.com', 'https://maoming.anjuke.com',
            'https://maanshan.anjuke.com', 'https://mudanjiang.anjuke.com', 'https://meishan.anjuke.com',
            'https://meizhou.anjuke.com', 'https://minggang.anjuke.com', 'https://meihekou.anjuke.com',
            'https://nanjing.anjuke.com', 'https://nb.anjuke.com', 'https://nc.anjuke.com',
            'https://nanning.anjuke.com', 'https://nantong.anjuke.com', 'https://nanchong.anjuke.com',
            'https://nanyang.anjuke.com', 'https://ningde.anjuke.com', 'https://neijiang.anjuke.com',
            'https://nanping.anjuke.com', 'https://naqu.anjuke.com', 'https://nujiang.anjuke.com',
            'https://nananshi.anjuke.com', 'https://ningguo.anjuke.com', 'https://panzhihua.anjuke.com',
            'https://pingdingsha.anjuke.com', 'https://panjin.anjuke.com', 'https://pingxiang.anjuke.com',
            'https://puyang.anjuke.com', 'https://putian.anjuke.com', 'https://puer.anjuke.com',
            'https://pingliang.anjuke.com', 'https://puning.anjuke.com', 'https://pizhou.anjuke.com',
            'https://penglaishi.anjuke.com', 'https://pinghu.anjuke.com', 'https://pingdu.anjuke.com',
            'https://pengzhou.anjuke.com', 'https://qd.anjuke.com', 'https://qinhuangdao.anjuke.com',
            'https://quanzhou.anjuke.com', 'https://qujing.anjuke.com', 'https://qiqihaer.anjuke.com',
            'https://quzhou.anjuke.com', 'https://qingyuan.anjuke.com', 'https://qinzhou.anjuke.com',
            'https://qingyang.anjuke.com', 'https://qiandongnan.anjuke.com', 'https://qianjiang.anjuke.com',
            'https://qingxu.anjuke.com', 'https://qiannan.anjuke.com', 'https://qitaihe.anjuke.com',
            'https://qianxinan.anjuke.com', 'https://qiananshi.anjuke.com', 'https://qingzhoushi.anjuke.com',
            'https://qingzhen.anjuke.com', 'https://qionghai.anjuke.com', 'https://qinyangshi.anjuke.com',
            'https://qufu.anjuke.com', 'https://qidong.anjuke.com', 'https://rizhao.anjuke.com',
            'https://rikeze.anjuke.com', 'https://ruian.anjuke.com', 'https://ruzhoushi.anjuke.com',
            'https://renqiushi.anjuke.com', 'https://ruijin.anjuke.com', 'https://rushanshi.anjuke.com',
            'https://renhuai.anjuke.com', 'https://ruili.anjuke.com', 'https://rugao.anjuke.com',
            'https://rongchengshi.anjuke.com', 'https://shanghai.anjuke.com', 'https://shenzhen.anjuke.com',
            'https://suzhou.anjuke.com', 'https://sjz.anjuke.com', 'https://sy.anjuke.com',
            'https://sanya.anjuke.com', 'https://shaoxing.anjuke.com', 'https://shantou.anjuke.com',
            'https://shiyan.anjuke.com', 'https://sanmenxia.anjuke.com', 'https://sanming.anjuke.com',
            'https://shaoguan.anjuke.com', 'https://shangqiu.anjuke.com', 'https://suqian.anjuke.com',
            'https://suihua.anjuke.com', 'https://shaoyang.anjuke.com', 'https://suining.anjuke.com',
            'https://shangrao.anjuke.com', 'https://siping.anjuke.com', 'https://shihezi.anjuke.com',
            'https://shunde.anjuke.com', 'https://suzhoushi.anjuke.com', 'https://songyuan.anjuke.com',
            'https://shuyang.anjuke.com', 'https://shizuishan.anjuke.com', 'https://suizhou.anjuke.com',
            'https://shuozhou.anjuke.com', 'https://shanwei.anjuke.com', 'https://sansha.anjuke.com',
            'https://shangluo.anjuke.com', 'https://shannan.anjuke.com', 'https://shennongjia.anjuke.com',
            'https://shuangyashan.anjuke.com', 'https://shishi.anjuke.com', 'https://sanheshi.anjuke.com',
            'https://shouguang.anjuke.com', 'https://shengzhou.anjuke.com', 'https://sihui.anjuke.com',
            'https://shaowu.anjuke.com', 'https://songzi.anjuke.com', 'https://tianjin.anjuke.com',
            'https://ty.anjuke.com', 'https://taizhou.anjuke.com', 'https://tangshan.anjuke.com',
            'https://taian.anjuke.com', 'https://taiz.anjuke.com', 'https://tieling.anjuke.com',
            'https://tongliao.anjuke.com', 'https://tongling.anjuke.com', 'https://tianshui.anjuke.com',
            'https://tonghua.anjuke.com', 'https://taishan.anjuke.com', 'https://tongchuan.anjuke.com',
            'https://tulufan.anjuke.com', 'https://tianmen.anjuke.com', 'https://tumushuke.anjuke.com',
            'https://tongcheng.anjuke.com', 'https://tongren.anjuke.com', 'https://taiwan.anjuke.com',
            'https://taicang.anjuke.com', 'https://taixing.anjuke.com', 'https://tengzhoushi.anjuke.com',
            'https://tongxiang.anjuke.com', 'https://tianchang.anjuke.com', 'https://wuhan.anjuke.com',
            'https://wuxi.anjuke.com', 'https://weihai.anjuke.com', 'https://weifang.anjuke.com',
            'https://wulumuqi.anjuke.com', 'https://wenzhou.anjuke.com', 'https://wuhu.anjuke.com',
            'https://wuzhou.anjuke.com', 'https://weinan.anjuke.com', 'https://wuhai.anjuke.com',
            'https://wenshan.anjuke.com', 'https://wuwei.anjuke.com', 'https://wulanchabu.anjuke.com',
            'https://wafangdian.anjuke.com', 'https://wujiaqu.anjuke.com', 'https://wuyishan.anjuke.com',
            'https://wuzhong.anjuke.com', 'https://wuzhishan.anjuke.com', 'https://wnelingshi.anjuke.com',
            'https://wuanshi.anjuke.com', 'https://wenchang.anjuke.com', 'https://wulanhaote.anjuke.com',
            'https://wuxue.anjuke.com', 'https://wanning.anjuke.com', 'https://xa.anjuke.com',
            'https://xm.anjuke.com', 'https://xuzhou.anjuke.com', 'https://xiangtan.anjuke.com',
            'https://xiangyang.anjuke.com', 'https://xinxiang.anjuke.com', 'https://xinyang.anjuke.com',
            'https://xianyang.anjuke.com', 'https://xingtai.anjuke.com', 'https://xiaogan.anjuke.com',
            'https://xining.anjuke.com', 'https://xuchang.anjuke.com', 'https://xinzhou.anjuke.com',
            'https://xuancheng.anjuke.com', 'https://xianning.anjuke.com', 'https://xinganmeng.anjuke.com',
            'https://xinyu.anjuke.com', 'https://bannan.anjuke.com', 'https://xianggang.anjuke.com',
            'https://xiangxi.anjuke.com', 'https://xiantao.anjuke.com', 'https://xilinguole.anjuke.com',
            'https://xintaishi.anjuke.com', 'https://xiangxiang.anjuke.com', 'https://xinghuashi.anjuke.com',
            'https://xingyi.anjuke.com', 'https://xuanwei.anjuke.com', 'https://xiangchengshi.anjuke.com',
            'https://xingcheng.anjuke.com', 'https://xinyishi.anjuke.com', 'https://xingyang.anjuke.com',
            'https://xinmi.anjuke.com', 'https://yt.anjuke.com', 'https://yangzhou.anjuke.com',
            'https://yichang.anjuke.com', 'https://yinchuan.anjuke.com', 'https://yangjiang.anjuke.com',
            'https://yongzhou.anjuke.com', 'https://yulinshi.anjuke.com', 'https://yancheng.anjuke.com',
            'https://yueyang.anjuke.com', 'https://yuncheng.anjuke.com', 'https://yichun.anjuke.com',
            'https://yingkou.anjuke.com', 'https://yulin.anjuke.com', 'https://yibin.anjuke.com',
            'https://yiyang.anjuke.com', 'https://yiwu.anjuke.com', 'https://yuxi.anjuke.com',
            'https://yili.anjuke.com', 'https://yangquan.anjuke.com', 'https://yanan.anjuke.com',
            'https://yingtan.anjuke.com', 'https://yanbian.anjuke.com', 'https://yufu.anjuke.com',
            'https://yaan.anjuke.com', 'https://yangchun.anjuke.com', 'https://yanling.anjuke.com',
            'https://yichunshi.anjuke.com', 'https://yushu.anjuke.com', 'https://yueqing.anjuke.com',
            'https://yuzhou.anjuke.com', 'https://yongxin.anjuke.com', 'https://yongkangshi.anjuke.com',
            'https://yidou.anjuke.com', 'https://yizheng.anjuke.com', 'https://yanji.anjuke.com',
            'https://yangzhong.anjuke.com', 'https://yining.anjuke.com', 'https://yingde.anjuke.com',
            'https://yuyao.anjuke.com', 'https://yanshishi.anjuke.com', 'https://yixing.anjuke.com',
            'https://zhengzhou.anjuke.com', 'https://zh.anjuke.com', 'https://zs.anjuke.com',
            'https://zhenjiang.anjuke.com', 'https://zibo.anjuke.com', 'https://zhangjiakou.anjuke.com',
            'https://zhuzhou.anjuke.com', 'https://zhangzhou.anjuke.com', 'https://zhanjiang.anjuke.com',
            'https://zhaoqing.anjuke.com', 'https://zaozhuang.anjuke.com', 'https://zhoushan.anjuke.com',
            'https://zunyi.anjuke.com', 'https://zhumadian.anjuke.com', 'https://zigong.anjuke.com',
            'https://ziyang.anjuke.com', 'https://zhoukou.anjuke.com', 'https://zhangqiu.anjuke.com',
            'https://zhangjiajie.anjuke.com', 'https://zhucheng.anjuke.com', 'https://zhuanghe.anjuke.com',
            'https://zhengding.anjuke.com', 'https://zhangbei.anjuke.com', 'https://zhangye.anjuke.com',
            'https://zhaotong.anjuke.com', 'https://weizhong.anjuke.com', 'https://zhaoxian.anjuke.com',
            'https://zouchengshi.anjuke.com', 'https://zunhua.anjuke.com', 'https://zhangjiagang.anjuke.com',
            'https://zhijiang.anjuke.com', 'https://zhaoyuanshi.anjuke.com', 'https://zixing.anjuke.com',
            'https://zhangshu.anjuke.com', 'https://zhuji.anjuke.com', 'https://zhuozhoushi.anjuke.com',
            'https://zaoyangshi.anjuke.com', 'https://chengdu.anjuke.com', 'https://chengdu.anjuke.com',
            'https://chengdu.anjuke.com', 'https://nanjing.anjuke.com', 'https://hangzhou.anjuke.com',
            'https://hangzhou.anjuke.com', 'https://hangzhou.anjuke.com', 'https://hangzhou.anjuke.com',
            'https://chongqing.anjuke.com', 'https://chongqing.anjuke.com', 'https://chongqing.anjuke.com',
            'https://chongqing.anjuke.com', 'https://chongqing.anjuke.com', 'https://chongqing.anjuke.com',
            'https://chongqing.anjuke.com', 'https://chongqing.anjuke.com', 'https://chongqing.anjuke.com',
            'https://chongqing.anjuke.com', 'https://chongqing.anjuke.com', 'https://dalian.anjuke.com',
            'https://jinan.anjuke.com', 'https://jinan.anjuke.com', 'https://jinan.anjuke.com',
            'https://zhengzhou.anjuke.com', 'https://zhengzhou.anjuke.com', 'https://cs.anjuke.com',
            'https://sjz.anjuke.com', 'https://sjz.anjuke.com', 'https://sjz.anjuke.com',
            'https://qd.anjuke.com', 'https://qd.anjuke.com', 'https://xa.anjuke.com', 'https://xa.anjuke.com',
            'https://xa.anjuke.com', 'https://nb.anjuke.com', 'https://nb.anjuke.com', 'https://hf.anjuke.com',
            'https://hf.anjuke.com', 'https://hf.anjuke.com', 'https://hf.anjuke.com', 'https://fz.anjuke.com',
            'https://fz.anjuke.com', 'https://fz.anjuke.com', 'https://km.anjuke.com', 'https://km.anjuke.com',
            'https://gy.anjuke.com', 'https://sy.anjuke.com', 'https://sy.anjuke.com', 'https://nc.anjuke.com',
            'https://nc.anjuke.com', 'https://cz.anjuke.com', 'https://jx.anjuke.com', 'https://yt.anjuke.com',
            'https://yt.anjuke.com', 'https://yt.anjuke.com', 'https://haikou.anjuke.com',
            'https://cc.anjuke.com', 'https://sanya.anjuke.com', 'https://sanya.anjuke.com',
            'https://sanya.anjuke.com', 'https://sanya.anjuke.com', 'https://huizhou.anjuke.com',
            'https://huizhou.anjuke.com', 'https://huizhou.anjuke.com', 'https://jilin.anjuke.com',
            'https://lanzhou.anjuke.com', 'https://langfang.anjuke.com',
            'https://luoyang.anjuke.com', 'https://nanning.anjuke.com',
            'https://nanning.anjuke.com', 'https://nantong.anjuke.com',  'https://quanzhou.anjuke.com',
            'https://shaoxing.anjuke.com',
            'https://taizhou.anjuke.com',  'https://tangshan.anjuke.com',

            'https://weifang.anjuke.com',  'https://xuzhou.anjuke.com',
            'https://yangzhou.anjuke.com',
            'https://yangzhou.anjuke.com',
            'https://yichang.anjuke.com', 'https://yichang.anjuke.com', 'https://yichang.anjuke.com',
            'https://zhenjiang.anjuke.com', 'https://zhenjiang.anjuke.com', 'https://binzhou.anjuke.com',
            'https://dongying.anjuke.com', 'https://taiz.anjuke.com', 'https://daqing.anjuke.com',
            'https://lianyungang.anjuke.com', 'https://huzhou.anjuke.com', 'https://huzhou.anjuke.com',
            'https://yancheng.anjuke.com', 'https://maanshan.anjuke.com', 'https://xuancheng.anjuke.com',
            'https://bazhong.anjuke.com'
        ]
        task_param_list = []
        count_ = int(input('请输入要开启的线程数量：'))
        # count_ = 1
        start_url = list(set(start_url))
        for i in start_url:
            task_param_list.append(i)
        pool = threadpool.ThreadPool(count_)
        reqs = threadpool.makeRequests(self.run2, task_param_list)
        for req in reqs:
            pool.putRequest(req)

        pool.wait()


if __name__ == '__main__':
    gt = GetInfoUrl()
    gt.run()
