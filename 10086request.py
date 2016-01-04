# -*- coding:UTF-8 -*-
import captcha
import requests
import RSA
import re
import json


class WhiteList(object):
    # 初始化
    def __init__(self):
        self.__session = requests.session()
        self.__username = ""
        self.__password = ""
        self.__loginstatus = 0
        self.__mobilephone = ""

    # 设置用户名
    def setusername(self, username):
        self.__username = username

    # 设置密码
    def setpassword(self, password):
        self.__password = password

    # 添加需要加入白名单的手机
    def addmobile(self, mobilephones):
        # 判断是否为列表
        if isinstance(mobilephones, list):
            self.__mobilephone = mobilephones
        else:
            self.__mobilephone = [mobilephones]

    @property
    def __AttemptLogin__(self):
        # 登录并保持初始cookie
        logininitpage = self.__session.get("http://bmd.sh.10086.cn/login.jsp")
        cookie = logininitpage.cookies
        # 使用登录页面的cookie获取验证码图片
        r = self.__session.get("http://bmd.sh.10086.cn/captcha.jpg", stream=True, cookies=cookie)
        # 获取生产public key用的modulus和exponent
        public_modulus_hex_re = re.compile("RSAUtils\.getKeyPair(.*)")
        public_modulus_hex = public_modulus_hex_re.findall(logininitpage.content)
        keypairs = public_modulus_hex[0].replace("\"", "").replace("(", "").replace(")", "").replace(";", "").split(",")
        encryptionexponent = keypairs[0].strip()
        modulus = keypairs[2].strip()
        with open('verifycode.jpg', 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
            f.close()
        # 获取验证码图片中的字符
        vcode = captcha.deCAPTCHA('verifycode.jpg')
        # 获取登录提交用的密码
        encryptedpw = RSA.encrypt(self.__password, modulus, encryptionexponent)
        payload = {"lg": self.__username,
                   "password": encryptedpw,
                   "mc": vcode}
        loginpage = self.__session.post("http://bmd.sh.10086.cn/login.wsp", data=payload, cookies=cookie)
        return loginpage

    def __login__(self):
        if self.__username == "" or self.__password == "":
            print("username or password missing")
            exit()
        else:
            page = self.__AttemptLogin__
            if page.content.decode('utf-8').find('账户被锁定'.decode('utf-8')) > 0:
                self.__loginstatus = 3  # 账户被锁定
            else:
                # 如果验证码错误则反复尝试，直到正确为止
                while page.content.decode('utf-8').find('验证码错误'.decode('utf-8')) > 0 or page.content.decode(
                        'utf-8').find('用户名或密码错误'.decode('utf-8')) > 0:
                    if page.content.decode('utf-8').find('用户名或密码错误'.decode('utf-8')) > 0:
                        print('uername or password is incorrect')
                        self.__loginstatus = 2  # 密码错误
                        exit()
                    else:
                        page = self.__AttemptLogin__
                self.__loginstatus = 1  # 成功

    def __savemobile__(self, mobile):
        # 提交单个手机号码到白名单
        pl = {"whiteMobile.oprCode": "01",
              "businessTypeName": "白名单业务",
              "whiteMobile.serviceCode": "10657109018606",
              "whiteMobile.serviceId": "QSH0010500",
              "whiteMobile.serviceType": "01",
              "whiteMobile.mobile": mobile}
        msg = self.__session.post("http://bmd.sh.10086.cn/wsp/saveWhiteMobile.wsp", data=pl).content
        msg = json.loads(msg, encoding='utf-8')
        return msg

    def savemobile(self):
        self.__login__()
        # 只有登录成功才会提交白名单
        if self.__loginstatus == 1:
            response = []
            # 遍历手机号码列表中的所有手机，并提交为白名单
            for m in self.__mobilephone:
                newmsg = self.__savemobile__(m)
                # 将服务器返回的记录写入字典
                msg = {"msg": newmsg[u'message'],
                       "success": newmsg[u"success"]}
                response.append(msg)
            return response
        else:
            # 登录失败，返回登录错误消息
            response = [{"msg": 'login failure',
                         "success": False}]
            return response

    def getloginstatus(self):
        # 返回登录状态
        if self.__loginstatus == 0:
            return {"StatusMsg": u"尚未登录",
                    "StatusCode": 0}
        if self.__loginstatus == 1:
            return {"StatusMsg": u"登录成功",
                    "StatusCode": 1}
        if self.__loginstatus == 2:
            return {"StatusMsg": u"登录失败，密码错误",
                    "StatusCode": 2}
        if self.__loginstatus == 3:
            return {"StatusMsg": u"登录失败，账户被锁定",
                    "StatusCode": 3}

    def close(self):
        # 关闭会话,所有变量设为控制
        self.__loginstatus = 0
        self.__mobilephone = ""
        self.__password = ""
        self.__username = ""
        self.__session.close()
