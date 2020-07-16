# -*- coding: utf8 -*-
import time
import json
import requests



class MG_sign:
    '''
    芒果签到
    *奖励：连签21天，得15天体验会员；对应积分
    '''
    def __init__(self, params):
        '''
        初始化
        :param params: url关键字credits.bz.mgtv.com/user/creditsTake的?后所有参数
        '''
        self.params = params
        self.params["timestamp"] = round(time.time())


    def sign(self):
        '''
        签到
        :return: 返回信息
        '''
        url = "https://credits.bz.mgtv.com/user/creditsTake"
        res = requests.get(url, params=self.params)
        res_json = json.loads(res.content.decode().replace("__jp5(", "").replace(");", ""))
        print("（mgtv）签到信息", res.content.decode())
        if res_json["code"] == 200:
            curDay = res_json["data"]["curDay"]
            credits = res_json["data"]["credits"]
            msg = f"签到：+{credits}积分\n已签到：{curDay}天/21天"
        else:
            msg = "签到失败"
        return msg




if __name__ == '__main__':
    params = {
        "uuid": "",
        "uid": "",
        "ticket": "",
        "token": "",
        "device": "MI 10 PRO",
        "did": "",
        "deviceId": "",
        "appVersion": "6.6.4",
        "osType": "android",
        "platform": "android",
        "abroad": 0,
        "aid": 635,
        "nonce": "",
        "timestamp": 1594818023,
        "appid": "credits_vd8S2VNu",
        "type": 1,
        "sign": "",
        "callback": "__jp5"
    }
    obj = MG_sign(params)
    msg = obj.sign()
    print("【芒果tv签到】", msg)
