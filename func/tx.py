import re
import time
import requests


class TX_sign:
    """
    腾讯视频签到
    *VIP签到两次
    """
    def __init__(self, cookies, params):
        '''
        初始化
        :param cookies: 
        :param params: 请求access.video.qq.com/user/auth_refresh?后的字符串
        '''
        self.params = params
        self.s = requests.session()
        # 设置cookies
        self.s.cookies = requests.utils.cookiejar_from_dict(cookies, cookiejar=None, overwrite=True)
        self.nickName = ""



    def auth_refresh(self):
        '''
        刷新信息
        '''
        url = "https://access.video.qq.com/user/auth_refresh"
        headers = {"referer": "https://v.qq.com/"}
        res = self.s.get(url, params=self.params, headers=headers)
        self.nickName = re.search('nick":"(.*?)"', res.content.decode()).group(1)
        print("（tx）刷新信息", res.text)



    def sign_once(self):
        '''
        一次签到
        '''
        url = "http://v.qq.com/x/bu/mobile_checkin"
        params = {
            "isDarkMode": 0,
            "uiType": "REGULAR"
        }
        res = self.s.get(url, params=params)
        match = re.search(r'isMultiple" />\s+(.*?)\s+<', res.text)
        if match:
            value = match.group(1)
            msg = f"成长值{value}"
        else:
            msg = "签到失败(可能已签到)"
        print("（tx）一次签到", msg)
        return msg


    def sign_twice(self):
        '''
        二次签到
        '''
        url = f"https://vip.video.qq.com/fcgi-bin/comm_cgi"
        params = {
            "name": "hierarchical_task_system",
            "cmd": 2,
            "_": round(time.time() * 1000),
            "callback": f"Zepto{round(time.time() * 1000 + 9)}"
        }
        res = self.s.get(url, params=params)
        ret = re.search('ret": (.*?),|}', res.text).group(1)
        if ret == "0":
            value = re.search('checkin_score": (.*?),', res.text).group(1)
            msg = f"成长值x{value}"
        else:
            msg = res.text
        print("（tx）二次签到", msg)
        return msg







if __name__ == '__main__':
    cookies = {
        'vqq_access_token': '',
        'vqq_openid': '',
        'vqq_refresh_token': '',
        'main_login': 'qq',
        'vqq_vuserid': '',
        'vqq_vusession': ''
    }
    params = {
        'vappid': '', 
        'vsecret': '', 
        'type': 'qq', 
        'g_tk': '', 
        'g_vstk': '', 
        'g_actk': '', 
        'callback': 'jQuery19108549813835942517_1594629802068', 
        '_': 1594629802069
    }

    obj = TX_sign(cookies, params)
    obj.auth_refresh()
    msg = f"用户：{obj.nickName}\n签到(1)：{obj.sign_once()}\n签到(2)：{obj.sign_twice()}"
    print("【腾讯视频签到】", msg)
