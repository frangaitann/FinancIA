from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from serpapi import GoogleSearch
from PIL import Image
import pymupdf, requests, asyncio, base64





# MUST ADAPT THIS CODE TO SEND THE IMAGES IN A SEPARATE WAY EACH ONE




def encode64(picture):
    with open(picture, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')




async def run_web(text, debug: bool):

    params = {
    "api_key": "7b6b3b5ba83e563c828b62fc9eb77bae1118ed47da82d2a8fcc9885a7982896f",
    "engine": "google_light_fast",
    "google_domain": "google.com",
    "q": text,
    "hl": "es",
    "gl": "ar",
    "uule": "w+CAIQICIjQXJnZW50aW5h"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    urls = []
    for i in results["organic_results"]:
        title = i["title"]
        index = i["position"]
        url = i["link"]
        
        urls.append(url)
        print(f'\n{index}\n{title}\n{url}\n\n')
    
    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch(
            headless=debug,
            args=[
                '--log-level=3',
                '--disable-gpu',
                '--disable_notifications',
                '--disable-search-engine-choice-screen',
                '--disable-blink-features=AutomationControlled'
            ],
        )
        
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/134.0.0.0 Safari/537.36",
            locale="en-US",
            timezone_id="America/Argentina/Buenos_Aires",
                    
        )
        
        pics= []
        page_quantity= 0
        for i, link in enumerate(urls):    
            await page.goto(link, wait_until='domcontentloaded')
            
            if ".pdf" in link:
                raw_doc= requests.get(link)
                raw_doc.raise_for_status()
                data_doc= raw_doc.content
                doc= pymupdf.open(stream=data_doc)
                
                for page_obj in range(doc.page_count):
                    page_n= doc.load_page(page_obj)
                    
                    pix= page_n.get_pixmap()
                    pagefile= f"page-{page_quantity}.png"
                    pix.save(pagefile)
                    pics.append(Image.open(pagefile))
                    page_quantity += 1
                    
                doc.close()
            else:
                await asyncio.sleep(2.5)
                screen_png= f"screen{i}.png"
                await page.screenshot(path=screen_png, full_page=True)
                pics.append(Image.open(screen_png))
            
        
        await browser.close()
        
        
        
        
        
        
if __name__ == '__main__':
    asyncio.run(run_web("IPC INDEC 2025", False))