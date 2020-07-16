# -*- coding: utf8 -*-
import time
import json
import requests

from func.iqiyi import IQY_sign
from func.tx import TX_sign
from func.mgtv import MG_sign
from func.wyy import WYY_sign
from func.ecloud import ECloud_sign
from func.wapj import PJ_sign
from func.ley import LY_sign
from func.bbs import JY_sign


def sendMsg(key, content):
    '''
    通过Cool Push向QQ发送信息
    :param key: 酷腿密钥
    :param c: 发送内容
    '''
    url = f"https://push.xuthus.cc/send/{key}"
    params = {
        "c": content
    }
    requests.get(url, params=params)


def iqy(P00001):
    '''爱奇艺引用'''
    # 签到
    obj = IQY_sign(P00001)
    msg1 = obj.sign()
    # 抽奖
    msg2 = []
    for i in range(3, 0, -1):
        ret = obj.draw(i)
        if ret["status"]:
            msg2.append(ret["msg"])
        else:
            break
    # 日常任务
    obj.queryTask().joinTask()
    msg3 = obj.queryTask().getReward()

    msg = f"{msg1}\n抽奖：{msg2}\n任务：{msg3}"
    return msg


def tx(cookies, params):
    '''腾讯视频引用'''
    obj = TX_sign(cookies, params)
    obj.auth_refresh()
    msg = f"用户：{obj.nickName}\n签到(1)：{obj.sign_once()}\n签到(2)：{obj.sign_twice()}"
    return msg


def mg(params):
    '''芒果tv引用'''
    obj = MG_sign(params)
    msg = obj.sign()
    return msg


def wyy(uin, pwd):
    '''网易云音乐引用'''
    obj = WYY_sign(uin, pwd)
    if obj.isLogin:
        msg = f'用户：{obj.nickname}\n签到：{obj.sign()}\n打卡：{obj.daka()}'
    else:
        msg = "登录失败，密码错误"
    return msg


def ecloud(user, pwd):
    '''天翼云盘引用'''
    obj = ECloud_sign(user, pwd)
    msg = obj.main()
    return msg

def pj(cookies):
    '''吾爱破解论坛引用'''
    obj = PJ_sign(cookies)
    msg = obj.sign()
    return msg

def ly(cookies):
    '''乐易论坛引用'''
    obj = LY_sign(cookies)
    msg = obj.sign()
    return msg


def jy(cookies):
    '''精易论坛引用'''
    obj = JY_sign(cookies)
    msg = obj.sign()
    return msg




def main_handler(event, context):
    with open("config.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())

    key = data["SKey"]
    # 爱奇艺
    msg_iqy = ""
    for d in data["IQIYI"]:
        msg_iqy += iqy(d["P00001"])

    # 腾讯视频
    msg_tx = ""
    for d in data["TX"]:
        params = dict([p.split("=") for p in d["params"].split("&")])
        cookies = dict([c.split("=") for c in d["cookies"].split("; ")])
        msg_tx += tx(cookies, params)

    # 芒果tv
    msg_mg = ""
    for d in data["MGO"]:
        params = dict([p.split("=") for p in d["params"].split("&")])
        msg_mg += mg(params)

    # 天翼云盘
    msg_ec = ""
    for d in data["ECLOUD"]:
        msg_ec += ecloud(d["user"], d["pwd"])

    # 吾爱论坛
    msg_52 = ""
    for d in data["52PJ"]:
        cookies = dict([c.split("=") for c in d["cookies"].split("; ")])
        msg_52 += pj(cookies)

    # 乐易论坛
    msg_ly = ""
    for d in data["LEY"]:
        cookies = dict([c.split("=") for c in d["cookies"].split("; ")])
        msg_ly += ly(cookies)

    # 精易论坛
    msg_jy = ""
    for d in data["BBS"]:
        cookies = dict([c.split("=") for c in d["cookies"].split("; ")])
        msg_jy += jy(cookies)

    # 网易云音乐
    msg_wyy = ""
    for d in data["WYY"]:
        msg_wyy += wyy(d["uin"], d["pwd"])

    # 发送信息
    msg = f"【爱奇艺】\n{msg_iqy}\n\
【腾讯视频】\n{msg_tx}\n\
【芒果tv】\n{msg_mg}\n\
【天翼云盘】\n{msg_ec}\n\
【吾爱破解论坛】\n{msg_52}\n\
【乐易论坛】\n{msg_ly}\n\
【精易论坛】\n{msg_jy}\n\
【网易云】\n{msg_wyy}"
    sendMsg(key, msg)
