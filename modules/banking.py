if __name__ == '__main__':
    from misc import cookies, date_getter
else:
    from modules.misc import cookies, date_getter

from pydoc import html
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
import os, csv, asyncio, pandas as pd






async def bank_scrapping(headless: bool = True):
    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch(
            headless=headless,
            args=[
                '--log-level=3',
                '--disable-gpu',
                '--disable_notifications',
                '--disable-search-engine-choice-screen',
                '--disable-blink-features=AutomationControlled'
            ],
        )
        
        page = await browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/134.0.0.0 Safari/537.36",
            locale="en-US",
            timezone_id="America/Argentina/Buenos_Aires",
                    
        )
        
        if "cookies.pkl" in os.listdir():
            await cookies(page)
            await page.goto("https://www.mercadopago.com.ar/home")
        else:
            print("No cookies")
            
        
            
        # Acc Balance
        bal = page.locator("//html/body/div[2]/main/section/div/div/div[1]/div[1]/div/div/div[1]/div/div[2]/div/span/span[2]")
        await bal.wait_for()
        bal = await bal.text_content()
        bal = bal.replace(".", "")

        # Acc Savings
        sav = page.locator("//html/body/div[2]/main/section/div/div/div[1]/section[1]/div[2]/div/div/div[1]/a/div/div[2]/span/span[2]")
        sav = await sav.text_content()
        sav = sav.replace(".", "")

        await page.goto("https://www.mercadopago.com.ar/activities#from-section=menu")
        
        
        
        dt_data = {"Name": [], "Amount": []}
        dt_dates = []
        already = set()
        
        try:
            with open("trans.csv", "r", encoding="utf-8") as f:
                csv_readed = f.read()
                for line in csv_readed.splitlines():
                    already.add(line.strip())
        except FileNotFoundError:
            csv_readed = None

        pages = True
        pages_counter = 1
        
        
        
        while pages == True:
            try:
                page_button = page.locator(f'.andes-pagination__link[href="/activities/{pages_counter}"][aria-label="Ir a la página {pages_counter}"]')
            
                await page_button.click()
                await page.wait_for_selector("ul.mp3-list.activities-list section.activity-feed", timeout=2000)
                
                trans_list = page.locator("ul.mp3-list.activities-list section.activity-feed")
                trans_days = await trans_list.count()
                #print(trans_days)
            except:
                pages= False
                continue
            
            try:
                html = await page.content()
                #print("activities-list" in html)
                await page.wait_for_timeout(2000)
            except:
                pages = False
                continue


            for day in range(trans_days):
                current = trans_list.nth(day)
                
                feeds = current.locator(".ui-rowfeed-container")
                day = await current.locator(".activity-feed__title").text_content()
                
                date_data = date_getter()
                
                if day == "Hoy":
                    day = f"{date_data[0]} de {date_data[1]} de {date_data[2]}"
                else:
                    day = f"{day} de {date_data[2]}"
                    

                feeds_count = await feeds.count()

                for transaction in range(feeds_count):
                    current_feed = feeds.nth(transaction)

                    trans_name = await current_feed.locator(".ui-rowfeed-title").text_content() #Who sends/receives transaction

                    trans_amount = await current_feed.locator(".andes-money-amount__fraction").text_content()           # ----
                    trans_amount = trans_amount.replace(".", "")                                                        #     |
                    trans_cents = await current_feed.locator(".andes-money-amount__cents").text_content()               #     |---> Getting Integer + Cents and converting to float
                    trans_amount = float(trans_amount + "." + trans_cents)                                              # ----

                    min_symbol = current_feed.locator(".andes-money-amount__negative-symbol")

                    if await min_symbol.count() != 0:
                        minus = True
                    else:
                        minus = False

                    if minus:
                        trans_amount = float("-" + str(trans_amount))


                    if f"{day},{trans_name}" in already:
                        continue
                    else:
                        dt_data["Name"].append(trans_name)
                        dt_data["Amount"].append(trans_amount)
                        dt_dates.append(day)
                    
            pages_counter += 1
    
    
    
    # Adding the data to the CSV file
    df = pd.DataFrame(dt_data, index=dt_dates)
    df.to_csv("trans.csv", index=True, mode='a', header=True if csv_readed is None else False)
    
    bal_and_sav = [float(bal), float(sav)]

    return bal_and_sav

if __name__ == '__main__':
    asyncio.run(bank_scrapping(False))