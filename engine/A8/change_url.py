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

def generate_affiliate_url():     
    driver.get("https://pub.a8.net/a8v2/asRakutenGoodsSearchAction.do")

    driver.find_elements_by_name('cartBtn').send_keys('jwanderson')
    driver.find_elements_by_class_name('cartBtn').send_keys('tozuka1998')



def main():
    start_chrome()
    generate_affiliate_url()

        
        
# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()