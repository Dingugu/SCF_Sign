# -*- coding: utf8 -*-
import sys, time, re, base64
import rsa, requests



class ECloud_sign:
    '''
    天翼云盘签到、抽奖
    *签到获取空间
    '''
    def __init__(self, username, password):
        '''
        :param username: 账号
        :param password: 密码
        '''
        self.user = username
        self.pwd = password
        self.s = requests.session()


    def main(self):
        ret = self.login()
        if ret["status"]:
            surl = f'https://api.cloud.189.cn/mkt/userSign.action?rand={round(time.time()*1000)}&clientType=TELEANDROID&verself.sion=8.6.3&model=SM-G930K'
            url = [
                'https://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?taskId=TASK_SIGNIN&activityId=ACT_SIGNIN',
                'https://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?taskId=TASK_SIGNIN_PHOTOS&activityId=ACT_SIGNIN'
            ]
            headers = {
                'User-Agent':'Mozilla/5.0 (Linux; Android 5.1.1; SM-G930K Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Verself.sion/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 Ecloud/8.6.3 Android/22 clientId/355325117317828 clientModel/SM-G930K imsi/460071114317824 clientChannelId/qq proVerself.sion/1.0.6',
                "Referer" : "https://m.cloud.189.cn/zhuanti/2016/sign/index.jsp?albumBackupOpened=1",
                "Host" : "m.cloud.189.cn",
                "Accept-Encoding" : "gzip, deflate",
            }
            #签到
            res = self.s.get(surl, headers=headers)
            print("（ecloud）签到", res.json())
            netdiskBonus = res.json()['netdiskBonus']
            msg = f"签到：+{netdiskBonus}M空间\n"
            #第一次抽奖
            res = self.s.get(url[0], headers=headers)
            print("（ecloud）第一次抽奖", res.text)
            if res.json().get("errorCode"):
                msg += f"抽奖(1)：{res.json()['errorCode']}\n"
            else:
                netdiskBonus = re.search(r"\d+", res.json()['description'])
                msg += f"抽奖(1)：+{netdiskBonus}M空间\n"
            #第二次抽奖
            res = self.s.get(url[1], headers=headers)
            print("（ecloud）第二次抽奖", res.text)
            if res.json().get("errorCode"):
                msg += f"抽奖(2)：{res.json()['errorCode']}"
            else:
                netdiskBonus = re.search(r"\d+", res.json()['description'])
                msg += f"抽奖(2)：+{netdiskBonus}M空间\n"
        else:
            msg = ret["msg"]
        return msg


    def login(self):
        url = "https://cloud.189.cn/udb/udb_login.jsp?pageId=1&redirectURL=/main.action"
        res = self.s.get(url)
        captchaToken = re.findall(r"captchaToken' value='(.+?)'", res.text)[0]
        lt = re.findall(r'lt = "(.+?)"', res.text)[0]
        returnUrl = re.findall(r"returnUrl = '(.+?)'", res.text)[0]
        paramId = re.findall(r'paramId = "(.+?)"', res.text)[0]
        j_rsakey = re.findall(r'j_rsaKey" value="(\S+)"', res.text, re.M)[0]
        self.s.headers.update({"lt": lt})

        username = self.rsa_encode(j_rsakey, self.user)
        password = self.rsa_encode(j_rsakey, self.pwd)
        url = "https://open.e.189.cn/api/logbox/oauth2/loginSubmit.do"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/76.0',
            'Referer': 'https://open.e.189.cn/',
        }
        data = {
            "appKey": "cloud",
            "accountType": '01',
            "userName": f"{{RSA}}{username}",
            "password": f"{{RSA}}{password}",
            "validateCode": "",
            "captchaToken": captchaToken,
            "returnUrl": returnUrl,
            "mailSuffix": ":189.cn",
            "paramId": paramId
        }
        res = self.s.post(url, data=data, headers=headers, timeout=5)
        print("（ecloud）登录提示", res.json())
        if res.json()['result']:
            msg = f"签到失败：登录出错\n错误提示：\n{res.json()['msg']}"
            return {"status": False, "msg": msg}
        else:
            redirect_url = res.json()['toUrl']
            res = self.s.get(redirect_url)
            return {"status": True, "msg": "登录成功"}


    def int2char(self, a):
        BI_RM = list("0123456789abcdefghijklmnopqrstuvwxyz")
        return BI_RM[a]

    def b64tohex(self, a):
        b64map = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        d = ""
        e = 0
        c = 0
        for i in range(len(a)):
            if list(a)[i] != "=":
                v = b64map.index(list(a)[i])
                if 0 == e:
                    e = 1
                    d += self.int2char(v >> 2)
                    c = 3 & v
                elif 1 == e:
                    e = 2
                    d += self.int2char(c << 2 | v >> 4)
                    c = 15 & v
                elif 2 == e:
                    e = 3
                    d += self.int2char(c)
                    d += self.int2char(v >> 2)
                    c = 3 & v
                else:
                    e = 0
                    d += self.int2char(c << 2 | v >> 4)
                    d += self.int2char(15 & v)
        if e == 1:
            d += self.int2char(c << 2)
        return d


    def rsa_encode(self, j_rsakey, string):
        rsa_key = f"-----BEGIN PUBLIC KEY-----\n{j_rsakey}\n-----END PUBLIC KEY-----"
        pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(rsa_key.encode())
        result = self.b64tohex((base64.b64encode(rsa.encrypt(f'{string}'.encode(), pubkey))).decode())
        return result





if __name__ == '__main__':
    username = ""
    password = ""

    obj = ECloud_sign(username, password)
    msg = obj.main()
    print("【天翼云盘】", msg)
