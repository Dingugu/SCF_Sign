# -*- coding: utf8 -*-
import hashlib
import random
import requests



class WYY_sign:
    '''
    网易云音乐签到、打卡
    接用第三方api：http://gzw.bylds.cn/music/
    '''
    def __init__(self, uin, pwd):
        '''
        初始化
        :param uin: 网易云账号
        :param pwd: 网易云密码
        '''
        self.uin = uin
        self.pwd = hashlib.md5(pwd.encode()).hexdigest()
        self.session = requests.session()
        self.host = "http://gzw.bylds.cn/music/api.php"
        self.nickname = ""
        self.isLogin = False

        self.login()


    def _requests(self, method, params, data=None):
        '''
        重写请求
        :param method: 请求方法
        :param params: url表单参数
        :param data: post提交数据
        :return: response对象
        '''
        if method.upper() == "GET":
            res = self.session.get(self.host, params=params, timeout=1000)
        elif method.upper() == "POST":
            res = self.session.post(self.host, params=params, data=data, timeout=1000)
        res.encoding = "utf-8"
        return res


    def login(self):
        '''
        登录
        '''
        params = {"do": "login"}
        data = {
            "uin": self.uin,
            "pwd": self.pwd,
            "r": random.random()
        }
        res = self._requests("POST", params, data)
        if not res.json().get("msg"):
            msg = "登录成功"
            self.nickname = res.json()["profile"]["nickname"]
            self.isLogin = True
            return [True, msg]
        else:
            msg = res.json()["msg"]
            self.isLogin = False
            return [False, msg]


    def sign(self):
        '''
        签到
        '''
        params = {"do": "sign"}
        data = {"r": random.random()}
        res = self._requests("POST", params, data)
        print("（wyy）签到数据", res.json())
        if res.json()["code"] == 200:
            msg = f"经验＋{res.json()['point']}"
        else:
            msg = res.json()["msg"]
        return msg


    def daka(self):
        '''
        300首歌打卡
        '''
        params = {"do": "daka"}
        data = {"r": random.random()}
        res = self._requests("POST", params, data)
        print("（wyy）打卡数据", res.content.decode())
        if res.status_code == 200:
            msg = f"听歌＋{res.json().get('count')}"
        else:
            try:
                msg = res.json()["msg"]
            except Exception as e:
                if res.status_code == 502:
                    self.daka()
                else:
                    msg = e
        return msg



if __name__ == '__main__':
    uin = "18736300609"
    pwd = "a787125293"

    obj = WYY_sign(uin, pwd)
    if obj.isLogin:
        msg = f'用户：{obj.nickname}\n签到：{obj.sign()}\n打卡：{obj.daka()}'
    else:
        msg = "登录失败，密码错误"
    print("【网易云签到】", msg)
