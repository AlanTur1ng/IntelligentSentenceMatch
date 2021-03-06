# -*- coding:utf-8 -*-
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
import requests
import os 
import sys

class UNIT:
    def __init__(self, api_key, api_secret):
        self.access_token = None
        self.url = None

        self.set_access_token(api_key, api_secret)

    def set_access_token(self, api_key, api_secret):
        host = 'https://aip.baidubce.com/oauth/2.0/token?' \
               'grant_type=client_credentials&' \
               'client_id={0}&' \
               'client_secret={1}'.format(api_key, api_secret)
        response = requests.post(host)
        if response:
            self.access_token = response.json()['access_token']
            print("access_token successe")
        else:
            print("access_token failed")

    def query(self, bot_session, query_text, app_id):
        self.url = 'https://aip.baidubce.com/rpc/2.0/unit/bot/chat?access_token=' + self.access_token
        post_data = """{   
                    "bot_session": "%s",
                    "log_id": "7758521",
                    "service_id": "%s",	
                    "request": {
                        "bernard_level": 1,
                        "client_session": "{\\\"client_results\\\":\\\"\\\", \\\"candidate_options\\\": []}",
                        "query": "%s",	
                        "query_info": {
                            "asr_candidates": [],
                            "source": "KEYBOARD",
                            "type": "TEXT"
                        },
                        "updates": "",
                        "user_id": "4a0b77ceeb674b0e829a622038d8d842"
                    },
                    "bot_id":"1086918",
                    "version": "2.0"
                }""" % (bot_session, app_id, query_text)
        post_data = post_data.encode('utf-8')
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(self.url, data=post_data, headers=headers)
        if response:
            return response.json()#['result']['response']['action_list'][0]['say']

if __name__ == "__main__":
    print("chating mode loading...")
    app_id = "1086918"
    inputs = sys.argv[0]
    api_key = "SVy07kGrs4h7zCtkVrPOB6wZ"
    api_secret = "TpFxIA0hmLcDqlYNuXjZfBqGi9HxaVvk"
    session_id = ""
    step = 1
    chatBot = UNIT(api_key, api_secret)
    while True:
        print("round %d" % step)
        inputs = input("your question: ")
        #print("step %d: with %s, %s, %s" % (step,session_id, inputs, app_id))
        response = chatBot.query(session_id, inputs, app_id)
        session_id = response['result']['bot_session'].split(",")[-1].split(":")[1].split("}")[0].split("\"")[1]#['session_id']
        session_id = "{\\\"session_id\\\":\\\"%s\\\"}" % session_id
        print("bot_session:", session_id)
        print("respons: \n ", response['result']['response']['action_list'][0]['say'])

        step += 1