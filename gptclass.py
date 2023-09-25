import requests
import random
import uuid

# request via proxy
proxies = {
    "http": "http://127.0.0.1:10809",
}


class GPT:
    def __init__(self):
        self.tokens = ""
        self.currenttoken = ""
        self.cookies = ""
        self.accesstoken = ""

    def _getaccounts(self):
        headers = {
            "sec-ch-ua": '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "referrer": "https://chat-shared2.zhile.io/shared.html",
            "referrerPolicy": "strict-origin-when-cross-origin",
        }
        url = "https://chat-shared2.zhile.io/api/loads?t=2050330140"
        response = requests.get(
            url,
            headers=headers,
            proxies=proxies,
        )
        # t = (response.text)  # 打印响应内容
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
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "sec-ch-ua": '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "referrer": "https://chat-shared2.zhile.io/shared.html",
            "referrerPolicy": "strict-origin-when-cross-origin",
        }
        url = "https://chat-shared2.zhile.io/auth/login"
        data = f"token_key={self.currenttoken.get('token_id')}&session_password=Wa204328SS."
        # data = "token_key=792fca33828ce595d4e2f0aff0a78acd&session_password=3wgrsgfga6767AA"
        response = requests.post(
            url,
            headers=headers,
            data=data,
            proxies=proxies,
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
            "referrer": "https://chat-shared2.zhile.io/?v=2",
            "referrerPolicy": "strict-origin-when-cross-origin",
        }
        url = "https://chat-shared2.zhile.io/api/auth/session"
        response = requests.get(
            url,
            headers=headers,
            cookies=self.cookies,
            proxies=proxies,
        )
        ##print(response.text)  # 打印响应内容
        json = response.json()  # 将响应转换为JSON格式
        # print(json)
        accesstoken = json.get("accessToken")
        # print(accesstoken)
        self.accesstoken = accesstoken
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
            "referrer": "https://chat-shared2.zhile.io/?v=2",
            "referrerPolicy": "strict-origin-when-cross-origin",
        }
        url = "https://chat-shared2.zhile.io/api/models?history_and_training_disabled=false"
        response = requests.get(
            url, headers=headers, cookies=self.cookies, proxies=proxies
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
            "referrer": "https://chat-shared2.zhile.io/?model=text-davinci-002-render-sha",
            "referrerPolicy": "strict-origin-when-cross-origin",
        }
        url = f"https://chat-shared2.zhile.io/api/conversations?offset=0&limit={limit}&order=updated"
        response = requests.get(url, headers=headers, cookies=self.cookies)
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
            "referrer": f"https://chat-shared2.zhile.io/c/{convid}",
            "referrerPolicy": "strict-origin-when-cross-origin",
        }
        url = f"https://chat-shared2.zhile.io/api/conversation/{convid}"
        response = requests.get(url, headers=headers, cookies=True)
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

    def _askconv_next(self, convid, question):
        convid = "aaa198ba-1d3b-4905-986d-18deec839daf"
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
        #get rand uuid
        uuidstr = str(uuid.uuid4())
        uuidstr2 = str(uuid.uuid4())
        body = '{"action":"variant","messages":[{"id":"aaa2ed78-c6d0-4082-bf24-8f4ccff3c96f","author":{"role":"user"},"content":{"content_type":"text","parts":["hello"]},"metadata":{}}],"parent_message_id":"aaa1f07f-796d-4261-b0ee-92235f3305e5","model":"text-davinci-002-render-sha","timezone_offset_min":-480,"variant_purpose":"comparison_implicit","history_and_training_disabled":false,"arkose_token":null}'
        response = requests.post(
            "https://chat-shared2.zhile.io/api/conversation", headers=headers, data=body
        )
        #print code
        print(response.status_code)
        print(response.text)


if __name__ == "__main__":
    g = GPT()
    print(g.Getaccesstoken())
    print(g._getmodels())
    print(g._getconvs())
    g._askconv_next("aaa198ba-1d3b-4905-986d-18deec839daf", "你好")

##todo --> g._askconv(convid,question)
## --> _getrecv(convid)
