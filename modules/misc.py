import json, os, pickle, locale
from datetime import datetime

DEBUG = False



def date_getter():
    locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
    
    now = datetime.now()
    day = now.day
    month = now.strftime("%B")
    year = now.year

    date_list = [day, month, year]
    return date_list




def token_loader():
    global gpt_token, deep_token
    with open("tokens.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                if data.get("model") == "GPT":
                    gpt_token = data.get("token")
                elif data.get("model") == "DEEP":
                    deep_token = data.get("token")
            except json.JSONDecodeError:
                continue
            



async def cookies(page):
    if "cookies.pkl" in os.listdir():

        cookies = pickle.load(open("cookies.pkl", "rb"))
        await page.context.clear_cookies()
        for i in cookies:

            cookie_dict = {
                "domain": i["domain"],
                "httponly": i["httponly"],
                "name": i["name"],
                "path": i["path"],
                "samesite": i["samesite"],
                "secure": i["secure"],
                "value": i["value"]
            }

            await page.context.add_cookies([cookie_dict])

        await page.reload()






# def parser():  Adapt it to playwright too