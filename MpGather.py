'''
@Description: mp投放微信数据采集类
@Version: 1.0
@Autor: Demoon
@Date: 1970-01-01 08:00:00
@LastEditors: Demoon
@LastEditTime: 2020-07-01 11:36:41
'''
import json
import requests
import utils as mytools


class MpGather:
    def __init__(self, cookie: dict, token: str, data_ary: tuple):
        self.data_ary = data_ary
        self.colloctConf = [
            {
                # 0     小游戏数据
                'url': 'https://mp.weixin.qq.com/promotion/as_rock',
                'data': {
                            'action': 'get_campaign_data',
                            'token': token,
                            'appid': '',
                            'spid': '',
                            '_': '',
                            'args': '',
                        }
            }
        ]
        #   配置requests session
        sess = requests.session()  # 新建session
        c = requests.cookies.RequestsCookieJar()        # 添加cookies到CookieJar
        for i in cookie:
            c.set(i["name"], i['value'])
        sess.cookies.update(c)  # 更新session里cookies
        self.req = sess
        #   设置一个请求头
        self.req.headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'referer': 'https://mp.weixin.qq.com/promotion/readtemplate?t=campaign/manage&lang=zh_CN&token='+str(token)+'&type=4',
            'sec-ch-ua': '"\\Not\"A;Brand";v="99", "Chromium";v="84", "Google Chrome";v="84"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.21 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }

    #   _get 方法
    def _get(self, url, para):
        res = self._subGet(url, para)
        while (res.get('ret') != 0):
            mytools.randomSleep()
            res = self._subGet(url, para)
        return res

    #   _get子方法
    def _subGet(self, url, para):
        res = {}
        try:
            r = self.req.get(url, params=para)
            res = r.json()
        except BaseException as e:
            print(str(e))
        return res

    #   统计信息采集
    def runCollect(self):
        #   广告联盟
        url = self.colloctConf[0]['url']
        params = self.colloctConf[0]['data']
        details_list = self.getPages(url, params)
        return details_list

    #   多页数据处理
    def getPages(self, url, data):
        #   请求参数
        args = {
            "op_type": 1,
            "where": {

            },
            "page": 1,
            "page_size": 20,
            "pos_type": 995,
            "advanced": True,
            "create_time_range": {
                "start_time": 1597593643
            },
            "query_index": "[\"cname\",\"material_preview\",\"status\",\"budget\",\"paid\",\"exp_pv\",\"clk_pv\",\"ctr\",\"clk_uv\",\"cpc\",\"conv_index_cvr\",\"conv_index_cpa\",\"bid\",\"ecpm\",\"expand_targeting_switch\",\"exposure_score\",\"minigame_realization_roi_amount\",\"minigame_realization_roi\",\"begin_time\",\"end_time\",\"auto_compensate_money\"]",
            "time_range": {
                "start_time": 1605456000,
                "last_time": 1605542399
            }
        }
        data['args'] = json.dumps(args)
        #   发起请求
        res = []
        onepage = self._get(url, data)
        while len(onepage.get('list', [])) > 0:
            res += self._dealData(onepage['list'])
            args['page'] = onepage['conf']['page'] + 1
            data['args'] = json.dumps(args)
            onepage = self._get(url, data)
        return res

    #   数据处理
    def _dealData(self, data_list: list):
        return list(map(lambda x: {
            'cname': x.get('campaign_info', {}).get('cname'),
            'appid': x.get('campaign_info', {}).get('product_id'),
            'paid': x.get('campaign3_index', {}).get('paid'),   # 花费
            'exp_pv': x.get('campaign3_index', {}).get('exp_pv'),   # 曝光次数
            'clk_pv': x.get('campaign3_index', {}).get('clk_pv'),   # 点击次数
            'ctr': x.get('campaign3_index', {}).get('ctr'),  # 点击率 0.0035
            'clk_uv': x.get('campaign3_index', {}).get('clk_uv'),   # 点击人数
            'cpc': x.get('campaign3_index', {}).get('cpc'),   # 点击均价
            }, data_list))