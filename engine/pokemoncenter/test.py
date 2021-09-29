import os
import csv

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from common.logger import set_logger
from common.google_spreadsheet import *
from twitter.twitter_tweet import *
from discord.discord_post import *
import pandas as pd

logger = set_logger(__name__)


def check_stock():
        jan = 4521329322780
        ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)" \
     "AppleWebKit/537.36 (KHTML, like Gecko)" \
     "Chrome/60.0.3112.113"
        item_url = f'https://www.pokemoncenter-online.com/?main_page=product_list&keyword={jan}&from=search_form&stock=on'
        res = requests.get(item_url, headers={"User-Agent": ua})
        soup = BeautifulSoup(res.text, "html.parser")
        logger.info('商品ページへ遷移しました')

        # 在庫確認
        logger.info('在庫確認中')

        name = soup.find_all('p', class_='name')
        a = soup.find('img',class_='item_image')

        logger.info(a)         

        
        logger.info(name[-1].text)         
           


def main():
    check_stock()
        
        
# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()