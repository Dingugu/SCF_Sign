# -*- coding: utf8 -*-
import re
import requests


class LY_sign:
    def __init__(self, cookies):
        """
        初始化设置参数
        :param cookies: 含必要参数的cookies
        """
        self.cookies = cookies
        self.url = "https://www.leybc.com/plugin.php"
        self.formhash = ""

        self.load()


    def _requests(self, method, params, data=None):
        '''
        重写requests请求
        :param method: 请求方法
        :param params: url表单值
        :param data: post请求数据
        :return: utf8编码后的response对象
        '''
        if method.upper() == "GET":
            res = requests.get(self.url, params=params, cookies=self.cookies)
        elif method.upper() == "POST":
            res = requests.post(self.url, params=params, data=data, cookies=self.cookies)
        res.encoding = "utf-8"
        return res


    def load(self):
        '''
        加载网页获取formhash值
        '''
        params = {"id": "dsu_paulsign:sign"}
        res = self._requests("GET", params=params)
        self.fromhash = re.search('formhash=(.*?)"', res.text).group(1)
        print(f"{'-'*10}乐易formhash值：{self.fromhash}{'-'*10}")


    def sign(self):
        '''
        签到
        '''
        params = {
            "id": "it618_credits:ajax",
            "formhash": self.fromhash,
            "ac": "qd"
        }
        res = self._requests("GET", params=params)
        print(f"{'-'*10}乐易签到：{res.content.decode('gbk')}{'-'*10}")
        msg = res.content.decode('gbk')
        if "奖励积分" in msg:
            credits = re.search("：(.*?) 易币").group(1)
            coins = re.search("易币 (.*?) 金钱").group(1)
            msg = f"签到：+{credits}易币;+{coins}金钱"
        return msg





if __name__ == '__main__':
    cookies = {
        "2vlT_96d0_saltkey": "",
        "2vlT_96d0_auth": ""
    }

    obj = LY_sign(cookies)
    msg = obj.sign()
    print("【乐易论坛】", msg)