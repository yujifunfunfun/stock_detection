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
import pandas as pd
import time

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


rakuten_app_id = os.environ.get("RAKUTEN_APPLICATION_ID")
rakuten_affiliate_id = os.environ.get("RAKUTEN_AFFILIATE_ID")


def detect_rakuten_stock():
    jan_list = download_target_jan('楽天')
    max_price_list = download_max_price('楽天')
    
    for jan,max_price in zip(jan_list,max_price_list):
        
        if jan == '':
            pass
        else:
            request_url = f'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?applicationId={rakuten_app_id}&keyword={jan}&affiliateId={rakuten_affiliate_id}'
            time.sleep(1)
            r = requests.get(request_url)
            resp = r.json()

            rakuten_df = pd.read_csv('jan_csv/rakuten_jan.csv',encoding='cp932',header=None)

            # 在庫確認
            logger.info('在庫確認中')
            
            if len(resp["Items"]) >= 1:
                if jan in rakuten_df.values.astype(str):
                    logger.info(f'ツイート済みの商品{jan}')
                elif item['itemPrice'] < int(max_price) :
                    logger.info(f"在庫あり:{jan}")
                    item = resp['Items'][0]['Item']
                    name = item['itemName']
                    affiliate_url = item['affiliateUrl']
                    send_tweet(f'<楽天>\n{name}\n{affiliate_url}')
                    send_discord(f'<楽天>\n{name}\n{affiliate_url}')
                
                    # CSVに保存
                    with open('jan_csv/rakuten_jan.csv','a') as f:
                        writer = csv.writer(f)
                        writer.writerow([])
                        writer.writerow([jan])
            else:
                logger.info(f"在庫なし:{jan}")
                if jan in rakuten_df.values.astype(str):
                    delete_jan = rakuten_df.replace(jan, 'soldout')
                    delete_jan.to_csv('jan_csv/rakuten_jan.csv', index=False,header=None)


if __name__ == "__main__":
    detect_rakuten_stock()
