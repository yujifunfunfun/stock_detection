import csv
import sys
import codecs
import math
import random
import requests
from time import sleep
import re
import pandas as pd
import urllib.parse
import os
from os.path import join, dirname
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from dotenv import load_dotenv
from common.logger import set_logger
from common.google_spreadsheet import *
from twitter.twitter_tweet import *
from discord.discord_post import *

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

logger = set_logger(__name__)


yahoo_app_id = os.environ.get("YAHOO_APP_ID")
yahoo_affiliate_id = os.environ.get("YAHOO_AFFILIATE_ID")


def detect_yahoo_stock():
    jan_list = download_target_jan('Yahoo')

    for jan in jan_list:
      if jan == '':
          pass
      else:
        request_url = f'https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch?appid={yahoo_app_id}&query={jan}'

        r = requests.get(request_url)
        resp = r.json()

        yahoo_df = pd.read_csv('jan_csv/yahoo_jan.csv',encoding='cp932',header=None)

        # 結果が１件以上あれば在庫ありとみなす
        logger.info('在庫確認中')
        if len(resp["hits"]) >= 1:
            if jan in yahoo_df.values.astype(str):
                logger.info(f'ツイート済みの商品{jan}')
            else:
                logger.info(f"在庫あり:{jan}")
                name = resp["hits"][0]['name']
                item_url = resp["hits"][0]['url']

                send_tweet(f'<Yahoo>\n{name}\n{item_url}')
                send_discord(f'<Yahoo>\n{name}\n{item_url}')
                print(f'<Yahoo>\n\n{name}\n\n{item_url}')
            
                # CSVに保存
                with open('jan_csv/yahoo_jan.csv','a') as f:
                    writer = csv.writer(f)
                    writer.writerow([])
                    writer.writerow([jan])

        else:
            logger.info(f"在庫なし:{jan}")
            if jan in yahoo_df.values.astype(str):
                delete_jan = yahoo_df.replace(int(jan), 'soldout')
                delete_jan.to_csv('jan_csv/yahoo_jan.csv', index=False,header=None)



if __name__ == "__main__":
    detect_yahoo_stock()