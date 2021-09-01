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


def rakuten_stock_detect():
    jan_list = download_target_jan('楽天')

    for jan in jan_list:
      request_url = f'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?applicationId={rakuten_app_id}&keyword={jan}&affiliateId={rakuten_affiliate_id}'

      r = requests.get(request_url)
      resp = r.json()
      
      # 結果が１件以上あれば在庫ありとみなす
      if len(resp["Items"]) >= 1:
          item = resp['Items'][0]['Item']
          name = item['itemName']
          affiliate_url = item['affiliateUrl']

          logger.info(f"在庫あり:{jan}")
          send_tweet(f'<楽天>\n{name}\n{affiliate_url}')
          send_discord(f'<楽天>\n{name}\n{affiliate_url}')
          print(f'<楽天>\n\n{name}\n\n{affiliate_url}')
      else:
          logger.info(f"在庫なし:{jan}")
 

if __name__ == "__main__":
    rakuten_stock_detect()