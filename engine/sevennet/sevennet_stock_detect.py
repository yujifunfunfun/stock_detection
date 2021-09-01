import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

import requests
from dotenv import load_dotenv
from common.logger import set_logger
from common.google_spreadsheet import *
from twitter.twitter_tweet import *
from discord.discord_post import *

logger = set_logger(__name__)


def start_chrome():
    global option
    option = Options()                         
    # option.add_argument('--headless') 
    # option.add_argument('--lang=ja-JP')
    # option.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # option.add_argument('--ignore-certificate-errors')
    # option.add_argument('--ignore-ssl-errors')
    # option.add_argument('--incognito') 
    option.add_argument("window-size=1500,1000")
    #ここで、バージョンなどのチェックをする
    global driver
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=option)   


def check_stock():
    jan_list = download_target_jan('セブンネット')
    

    for jan in jan_list:
        # 商品ページへ遷移
        driver.get(f"https://7net.omni7.jp/search/?keyword={jan}")
        logger.info('商品ページへ遷移しました')
        time.sleep(3)

        # 在庫確認
        logger.info('在庫確認中')

        if driver.find_elements_by_class_name('js-pressTwice'):
             
             logger.info(f"在庫あり:{jan}")
             name = driver.find_element_by_xpath('//*[@id="mainContent"]/div[5]/div[2]/div/div[10]/div/div[3]/div[2]/div/div/div/div[2]/div[1]/p[1]/a')
             url = name.get_attribute("href")

             src = driver.find_element_by_xpath('//*[@id="mainContent"]/div[5]/div[2]/div/div[10]/div/div[3]/div[2]/div/div/div/p/a/img').get_attribute("src")
             responce = requests.get(src)
             with open("img/" + "1.jpg", "wb") as f:
                 f.write(responce.content)

             send_tweet_with_img(f'<セブンネット>\n{name.text}\n{url}')
             send_discord(f'<セブンネット>\n{name.text}\n{url}')
             print(f'<セブンネット>\n{name.text}\n\n{url}')
        else:
            logger.info(f"在庫なし:{jan}")
            
def main():
    start_chrome()
    check_stock()
        
        
# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()