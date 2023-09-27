# Description: This is a simple chatgpt tool.
# Author: Wu Yixuan
# Date: 2023-9-26
# Version: 1.0.4
# Repository: https://git.5i.gs/Cutieu/Python-Gpt-Free
# Website: https://5i.gs

import requests
import random
import uuid
import json

__version__ = "1.0.4"
# 选择是否使用代理
__proxy__ = {
    "http": "http://127.0.0.1:10809",
}
# __proxy__ = None


class GPT:
    def __init__(self, sessfile="sess.txt"):
        # load sess
        self.sessfile = sessfile
        try:
            with open(sessfile, "r") as f:
                siss = json.loads(f.read())
                self.accesstoken = siss.get("accesstoken")
                # self.tokens = siss.get("tokens")
        except:
            self.accesstoken = ""

        self.tokens = ""
        self.currenttoken = ""
        self.cookies = ""

        self.proxies = __proxy__

        self.urlbase = "chat-shared2.zhile.io"
        try:
            rconf = json.loads(
                requests.get(
                    "https://git.5i.gs/Cutieu/Python-Gpt-Free/raw/branch/main/update.txt?"
                    + str(random.random())
                ).text
            )
            if rconf.get("version") != __version__:
                print(f"检测到新版本，即将下载{rconf.get('version')}版本,到{__file__}")
                if input("是否下载？(n取消)").lower() == "n":
                    exit(0)
                with open(__file__, "w") as f:
                    f.write(
                        requests.get(
                            "https://git.5i.gs/Cutieu/Python-Gpt-Free/raw/branch/main/pyfreegpt.py?"
                            + str(random.random())
                        ).text
                    )
                print("下载完成，正在重启")
                import os

                os.system("python " + __file__)
                exit()
            self.urlbase = rconf.get("urlbase")
        except Exception as e:
            print(f"检测更新失败{e},使用本地配置.")

    def _savesiss(self):
        with open(self.sessfile, "w") as f:
            f.write(
                json.dumps(
                    {
                        "accesstoken": self.accesstoken,
                        # "tokens": self.tokens,
                    }
                )
            )

    def _getaccounts(self):
        headers = {
            "sec-ch-ua": '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "referrer": f"https://{self.urlbase}/shared.html",
            "referrerPolicy": "strict-origin-when-cross-origin",
        }
        url = f"https://{self.urlbase}/api/loads?t=2050330140"
        response = requests.get(
            url,
            headers=headers,
            proxies=self.proxies,
        )
        if "Just a moment..." in (response.text):
            print("cloudflare检测到你是机器人，请切换代理或手动修改源码添加cookie")
            exit(0)
        json = response.json()  # 将响应转换为JSON格式
        # #print(json)
        tokendic = json.get("loads")
        self.tokens = tokendic
        return tokendic

    def _chooseaccount(self):
        self.currenttoken = random.choice(self.tokens)
        # print (self.currenttoken)
        return self.currenttoken

    def _login(self):
        _session_password = "Wa204328SS."
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "sec-ch-ua": '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "referrer": f"https://{self.urlbase}/shared.html",
            "referrerPolicy": "strict-origin-when-cross-origin",
        }
        url = f"https://{self.urlbase}/auth/login"
        data = f"token_key={self.currenttoken.get('token_id')}&session_password={_session_password}"
        # data = "token_key=792fca33828ce595d4e2f0aff0a78acd&session_password=3wgrsgfga6767AA"
        response = requests.post(
            url,
            headers=headers,
            data=data,
            proxies=self.proxies,
        )
        # save cookies
        self.cookies = response.cookies
        # #print cookies
        # print(response.cookies)
        # #print raw response
        # print(response.text)  # 打印响应内容
        # #print(response.status_code)  # 打印响应状态码
        # #print headers
        # print(response.headers)
        if "400" in response.text:
            return 400
        else:
            return 200

    def _getaccesstoken(self):
        headers = {
            "sec-ch-ua": '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "referrer": f"https://{self.urlbase}/?v=2",
            "referrerPolicy": "strict-origin-when-cross-origin",
        }
        url = f"https://{self.urlbase}/api/auth/session"
        response = requests.get(
            url,
            headers=headers,
            cookies=self.cookies,
            proxies=self.proxies,
        )
        ##print(response.text)  # 打印响应内容
        json = response.json()  # 将响应转换为JSON格式
        # print(json)
        accesstoken = json.get("accessToken")
        # print(accesstoken)
        self.accesstoken = accesstoken
        self._savesiss()
        return accesstoken

    def Getaccesstoken(self):
        if not self.tokens:
            self._getaccounts()
        self._chooseaccount()
        if self._login() == 200:
            return self._getaccesstoken()
        else:
            return self.Getaccesstoken()

    def _getmodels(self):
        headers = {
            "authorization": f"Bearer {self.accesstoken}",
            "content-type": "application/json",
            "sec-ch-ua": '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "referrer": f"https://{self.urlbase}/?v=2",
            "referrerPolicy": "strict-origin-when-cross-origin",
        }
        url = f"https://{self.urlbase}/api/models?history_and_training_disabled=false"
        response = requests.get(
            url, headers=headers, cookies=self.cookies, proxies=self.proxies
        )
        # print (response.text)
        json = response.json()
        models = []
        for j in json.get("models"):
            models.append(j.get("slug"))
        self.models = models
        return models

    def _getconvs(self, limit=28):
        headers = {
            "authorization": f"Bearer {self.accesstoken}",
            "content-type": "application/json",
            "sec-ch-ua": '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "referrer": f"https://{self.urlbase}/?model=text-davinci-002-render-sha",
            "referrerPolicy": "strict-origin-when-cross-origin",
        }
        url = f"https://{self.urlbase}/api/conversations?offset=0&limit={limit}&order=updated"
        response = requests.get(
            url, headers=headers, cookies=self.cookies, proxies=self.proxies
        )
        print(response.text)  # 打印响应内容
        json = response.json()  # 将响应转换为JSON格式
        c = json.get("items")
        self.convs = c
        return c

    def _convgetcontent(self, convid):
        headers = {
            "authorization": f"Bearer {self.accesstoken}",
            "content-type": "application/json",
            "sec-ch-ua": '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "referrer": f"https://{self.urlbase}/c/{convid}",
            "referrerPolicy": "strict-origin-when-cross-origin",
        }
        url = f"https://{self.urlbase}/api/conversation/{convid}"
        response = requests.get(
            url, headers=headers, proxies=self.proxies, cookies=self.cookies
        )
        print(response.text)  # 打印响应内容
        """json = response.json()  # 将响应转换为JSON格式
        title = json.get("title")
        # ResourceWarning
        result = []
        for key, value in json["mapping"].items():
            # 判断value中的message键对应的值中的author键对应的值中的role键对应的值是否为"user"
            if value["message"]["author"]["role"] == "user":
                # 如果是"user"，则将value中的message键对应的值中的content键对应的值中的parts键对应的值（一个列表）中的第一个元素（一个字符串）赋给text变量
                text = value["message"]["content"]["parts"][0]
                # 将{"rule":"user","text":"..."}这样的字典添加到结果列表中，其中"text"键对应的值为text变量
                result.append({"rule": "user", "text": text})
        pass"""

    def _askconv_next_simple(self, question, callback=lambda x: print(x)):
        url = f"https://{self.urlbase}/api/conversation"
        headers = {
            "accept": "text/event-stream",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "authorization": f"Bearer {self.accesstoken}",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "pragma": "no-cache",
            "sec-ch-ua": '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
        }
        data = {
            "action": "next",
            "messages": [
                {
                    "id": str(uuid.uuid4()),  # ,"aaa22022-158d-4f90-8394-cce1a33e84cb"
                    "author": {"role": "user"},
                    "content": {"content_type": "text", "parts": [question]},
                    "metadata": {},
                }
            ],
            "parent_message_id": str(
                uuid.uuid4()
            ),  # ,"aaa16cbf-5f20-400b-8eb3-0ac293093164"
            "model": "text-davinci-002-render-sha",
            "timezone_offset_min": -480,
            "suggestions": [
                "What are 5 creative things I could do with my kids' art? I don't want to throw them away, but it's also so much clutter.",
                "Can you come up with some names for a mocktail (non-alcoholic cocktail) with Coke and pomegranate syrup?",
                "'Come up with 5 sophisticated names for my coffee shop that becomes a bar at night – like \"The Page Turner\". Include a short sentence explaining what it means!'",
                "Design a database schema for an online merch store.",
            ],
            "history_and_training_disabled": False,
            "arkose_token": None,
        }
        response = requests.post(
            url,
            headers=headers,
            json=data,
            cookies=self.cookies,
            proxies=self.proxies,
            stream=True,
        )
        cs = ""
        flag = False
        for chunk in response.iter_content(chunk_size=10240):
            cs += chunk.decode("utf-8") + "\n"
            while "\n" in cs:
                i, cs = cs.split("\n", 1)
                if "data: [DONE]" in i:
                    break
                if i.startswith("data:"):
                    try:
                        j = json.loads(i.replace("data: ", ""))
                        rep = j.get("message").get("content").get("parts")[0]
                        callback(rep)
                        flag = True
                    except:
                        ...
        if not flag:
            return "error"
        return rep

    def Ask(self, question, callback=None):
        globles = {"cnt": 0}

        def tcallback(rep):
            repl = "正在生成中：" + rep.replace("\n", "").replace(" ", "").replace("\r", "")
            print(repl[globles["cnt"] :], end="", flush=True)
            globles["cnt"] = len(repl)

        if callback:
            tcallback = callback

        x = self._askconv_next_simple(question, tcallback)
        if x == "error":
            self.Getaccesstoken()
            return self.Ask(question)
        return x


def Ask(question, callback=None):
    g = GPT()
    return g.Ask(question, callback=callback)


"""if __name__ == "__main__":
    g = GPT()
    # print(g.Getaccesstoken())
    # print(g._getmodels())
    # print(g._getconvs())
    # print(g._askconv_next_simple("你可以帮我写代码吗？"))
    for i in range(100):
        print("\n"*5,f"For .{i}",g.Ask("你可以帮我写代码吗？,使用python编写一个关于{}的程序".format(i)))


##todo --> g._askconv(convid,question)
## --> _getrecv(convid)
# generite uuid
# uuid.uuid4()
"""
if __name__ == "__main__":
    print(Ask("你是谁"))
