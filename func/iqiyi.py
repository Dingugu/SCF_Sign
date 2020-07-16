# -*- coding: utf8 -*-
import requests

class IQY_sign:
    '''
    爱奇艺签到、抽奖
    *奖励：签7天奖1天，14天奖2天，28天奖7天；日常任务；随机成长值
    '''
    def __init__(self, P00001):
        '''
        :param P00001: cookies中必要参数
        '''
        self.P00001 = P00001
        self.taskList = []
        self.growthTask = 0

    def sign(self):
        '''
        签到
        '''
        url = "https://tc.vip.iqiyi.com/taskCenter/task/queryUserTask"
        params = {
             "deviceId": "891BA95ECB858923B61E235940927Be3",
             "appname": "memberTask",
             "messageId": "memberTask_sRbBsBRlR6hYpDuJGSC5h838eCCr6GKc",
             "version": "2.0",
             "invokeType": "outer_http",
             "lang": "zh_cn",
             "P00001": self.P00001,
             "belong": "GOLD_TASK",
             "autoSign": "yes",
             "platform": "bb136ff4276771f3",
             "fv": "8810d5688ee1a7a6",
             "appVersion": "11.6.5"
        }
        res = requests.get(url, params=params)
        if res.json()["code"] == "A00000":
            growth = res.json()["data"]["signInfo"]["data"]["rewardMap"]["growth"]
            continueSignDaysSum = res.json()["data"]["signInfo"]["data"]["continueSignDaysSum"]
            vipStatus = res.json()["data"]["userInfo"]["vipStatus"]
            rewardDay = 7 if continueSignDaysSum<=7 else (14 if continueSignDaysSum<=14 else 28)
            msg = f"VIP等级：{vipStatus}\n签到：+{growth}成长值\n已签到：{continueSignDaysSum}天/{rewardDay}天"
            
            self.hot_taskCode = res.json()["data"]["tasks"]["daily"][1]["taskCode"]
        else:
            print("（iqy）签到错误", res.content.decode())
            msg = f'错误代码：{res.json()["code"]}\n信息：{res.json()["msg"]}'
        return msg


    def draw(self, i):
        '''
        抽奖
        :param i: 签到次数
        '''
        url = "https://cards.iqiyi.com/views_category/3.0/vip_home"
        params1 = {
            "bi_params": "{%22vipService%22: %22new%22,%22vip_huanfu%22: null}",
            "from_subtype": 1,
            "from_type": 56,
            "block": "504091_vip_1",
            "page_st": "suggest",
            "card_v": "3.0",
            "phone_operator": 2,
            "phoneOperator": 2,
            "cellphoneModel": "TAS-AN00",
            "ip": "10.0.2.15",
            "longitude": 116.404188,
            "latitude": 39.914466,
            "cinema_show_ds": "1",
            "layout_v": 70.103,
            "app_k": "e8f644bf99f68d71df79fe80c0a72d64",
            "device_type": 0,
            "dev_os": "5.1.1",
            "secure_p": "GPhone",
            "secure_v": 1,
            "psp_status": 3,
            "app_lm": "cn",
            "api_v": 11.4,
            "imei": "ce700690cd1447933749cc753dd93773",
            "net_sts": 1,
            "lang": "zh_CN",
            "qyid": "f185cea041dfcbec15c66b7155041ba91101",
            "psp_cki": "2445cb3a367b6915c204a3f3ec55e0c4c9212fe8bcb470459bc1570b28357e48",
            "psp_sub_uid": 1626879399,
            "scrn_scale": 1,
            "mac": "a6: 1e: fd: 31: 30: de",
            "cupid_v": "3.47.008",
            "profile": "%7B%22group%22%3A%221%2C2%22%2C%22counter%22%3A1%2C%22hy_id%22%3A%22%22%2C%22recall_firstdate%22%3A%22-1%22%2C%22first_time%22%3A%2220200713%22%2C%22recall_time%22%3A%22%22%7D",
            "upd": 1,
            "app_v": "11.6.5",
            "psp_uid": 1626879300,
            "platform_id": 10,
            "core": 1,
            "dev_ua": "TAS-AN00",
            "aid": "31216ecca8b6eb12",
            "cupid_uid": 860242417064453,
            "app_gv": "",
            "gps": "%2C",
            "bdgps": "116.404188%2C39.91446",
            "youth_model": 0,
            "no_rec": 0,
            "xas": 1,
            "pkg_t": 1,
            "dev_t": 1,
            "net_level": 3,
            "req_times": 0,
            "req_sn": 1594637758659
        }
        headers = {
            "t": 490079643,
            "sign": "087cfe72a655408f11a9083de5d869dd"
        }
        res = requests.get(url, params=params1, headers=headers)
        # 提取抽奖url前缀
        for i, card in enumerate(res.json()["cards"]):
            for j, block in enumerate(card["blocks"]):
                url = block.get("actions", {}).get("click_event", {}).get("data", {}).get("url")
                if url and url.startswith("http://iface2.iqiyi.com/"):
                    # 抽奖    
                    params2 ={
                        "lottery_num": i,
                        "app_k": "e8f644bf99f68d71df79fe80c0a72d64",
                        "app_v": "11.6.5",
                        "app_gv": "",
                        "app_t": 0,
                        "platform_id": 10,
                        "dev_os": "5.1.1",
                        "dev_ua": "TAS-AN00",
                        "net_sts": 1,
                        "qyid": "f185cea041dfcbec15c66b7155041ba91101",
                        "imei": "ce700690cd1447933749cc753dd93773",
                        "aid": "31216ecca8b6eb12",
                        "mac": "a6: 1e: fd: 31: 30: de",
                        "scrn_scale": 1,
                        "lang": "zh_CN",
                        "app_lm": "cn",
                        "oaid": "",
                        "psp_uid": 1626879300,
                        "psp_sub_uid": 1626879300,
                        "psp_cki": "2445cb3a367b6915c204a3f3ec55e0c4c9212fe8bcb470459bc1570b28357e48",
                        "psp_status": 3,
                        "secure_v": 1,
                        "secure_p": "GPhone",
                        "cupid_id": 860242417065354,
                        "cupid_v": "3.47.008",
                        "core": "1",
                        "profile": "%7B%22group%22%3A%221%2C2%22%2C%22counter%22%3A1%2C%22hy_id%22%3A%22%22%2C%22recall_firstdate%22%3A%22-1%22%2C%22first_time%22%3A%2220200713%22%2C%22recall_time%22%3A%22%22%7D",
                        "unlog_sub": "0",
                        "cust_count": "",
                        "dev_hw": "%7B%22cpu%22%3A2400000%2C%22gpu%22%3A%22%22%2C%22mem%22%3A%22171.2MB%22%7D",
                        "net_ip": "%7B%22country%22%3A%22%E4%B8%AD%E5%9B%BD%22%2C%22province%22%3A%22%E5%8C%97%E4%BA%AC%22%2C%22city%22%3A%22%E5%8C%97%E4%BA%AC%22%2C%22cc%22%3A%22%E7%A7%BB%E5%8A%A8%22%2C%22area%22%3A%22%E5%8D%8E%E4%B8%AD%22%2C%22timeout%22%3A0%2C%22respcode%22%3A0%7D",
                        "scrn_sts": "1",
                        "scrn_res": "360,640",
                        "scrn_dpi": 160,
                        "psp_vip": 1,
                        "client_ip": "%7B%22country%22%3A%22%E4%B8%AD%E5%9B%BD%22%2C%22province%22%3A%22%E5%8C%97%E4%BA%AC%22%2C%22city%22%3A%22%E5%8C%97%E4%BA%AC%22%2C%22cc%22%3A%22%E7%A7%BB%E5%8A%A8%22%2C%22area%22%3A%22%E5%8D%8E%E4%B8%AD%22%2C%22timeout%22%3A0%2C%22respcode%22%3A0%7D",
                        "province_id": 2008,
                        "upd": "1",
                        "youth_model": 0,
                        "no_rec": 0,
                        "xas": 1,
                        "bi_params": "%7B%22bi_recommend_reason%22%3A%22recreason%22%2C%22vipService%22%3A%22new%22%2C%22viptab%22%3A%22cid_order_list_1%22%2C%22people_id%22%3A%220%22%2C%22vertical_order%22%3A%22colomn%22%2C%22paperplane%22%3A%22yes%22%2C%22game_liveroom%22%3A%221%22%2C%22ad_focus_time%22%3A%225%22%2C%22recommend%22%3A%221%22%2C%22ct%22%3A%2220200713%22%2C%22qyhome%22%3A%22newui%22%2C%22wdym_hd%22%3A%220%22%2C%22smallvideo%22%3A%221%22%2C%22baike_p2v%22%3A%22bucket_a%22%2C%22order%22%3A%22huati%2Cdati%2Cbaoxiang%2Cwenda%22%2C%22hotply_recommend_num%22%3A%22twentytwo%22%2C%22ad_third%22%3A%22yes%22%2C%22moviereason%22%3A%22new%22%2C%22is_poster%22%3A%22bi%22%2C%22design%22%3A%221%22%7D",
                        "pkg_t": 1,
                        "dev_t": 1,
                        "aqyid": "860242417065353_31216ecca8b6eb11_0",
                        "pps": 0,
                        "pu": 1626879300,
                        "cupid_uid": 860242417065353,
                        "api_v": "11.4",
                        "gps": "%2C",
                        "bdgps": "121.497859%2C31.24768",
                        "net_level": 2,
                        "req_times": 0,
                        "req_sn": 1594640282763
                    }
                    res = requests.get(url, params=dict(params1, **params2), headers=headers)
                    break
        if not res.json().get('code'):
            msg = res.json()["awardName"]
            return {"status": True, "msg": msg}
        else:
            msg = res.json()["kv"]["msg"]
            return {"status": False, "msg": msg}


    def queryTask(self):
        '''
        获取日常任务 和 taskCode
        '''
        url = "https://tc.vip.iqiyi.com/taskCenter/task/queryUserTask"
        params = {
            "deviceId": "891BA95ECB858923B61E235940927BE3",
            "appname": "memberTask",
            "messageId": "memberTask_KnfCA0s791iyMa0RLUaTHFSrYYeMOPO2",
            "version": 2.0,
            "invokeType": "outer_http",
            "lang": "zh_cn",
            "P00001": self.P00001,
            "belong": "GOLD_TASK",
            "autoSign": "yes",
            "platform": "bb136ff4276771f3",
            "fv": "8810d5688ee1a7a6",
            "appVersion": "11.6.5"
        }
        res = requests.get(url, params=params)
        if res.json()["code"] == "A00000":
            for item in res.json()["data"]["tasks"]["daily"]:
                self.taskList.append({
                    "name": item["name"],
                    "taskCode": item["taskCode"],
                    "status": item["status"],
                    "taskReward": item["taskReward"]["task_reward_growth"]
                    })
        else:
            print("（iqy）获取任务失败")
        return self


    def joinTask(self):
        """
        遍历完成任务
        """
        url = "https://tc.vip.iqiyi.com/taskCenter/task/joinTask"
        params = {
            "P00001": self.P00001,
            "taskCode": "",
            "platform": "bb136ff4276771f3",
            "lang": "zh_CN",
            "app_lm": "cn"
        }
        # 遍历任务，仅做一次
        for item in self.taskList:
            if item["status"] == 2:
                params["taskCode"] = item["taskCode"]
                res = requests.get(url, params=params)


    def getReward(self):
        """
        获取任务奖励
        :return: 返回信息
        """
        url = "https://tc.vip.iqiyi.com/taskCenter/task/getTaskRewards"
        params = {
            "P00001": self.P00001,
            "taskCode": "",
            "platform": "bb136ff4276771f3",
            "lang": "zh_CN",
            "app_lm": "cn",
            "deviceID": "891BA95ECB858923B61E235940927BE3",
            "dfp": "14870f1cce322d4109ae303a70bfe7cd35d9d92fe037bfd1d8f79d8747e00d82bc",
            "fv": "8810d5688ee1a7a6"
        }
        # 遍历任务，领取奖励
        for item in self.taskList:
            if item["status"] == 0:
                params["taskCode"] = item["taskCode"]
                res = requests.get(url, params=params)
                if res.json()["code"] == "A00000":
                    self.growthTask += item["taskReward"]
        msg = f"+{self.growthTask}成长值"
        return msg




if __name__ == '__main__':
    P00001 = ""
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
    print("【爱奇艺签到】", msg)
