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
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from common.google_spreadsheet import *
from twitter.twitter_tweet import *

def main():

    jan_list = download_target_jan('Yahoo')

    for jan in jan_list:
      
      request_url = f'https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch?appid=dj00aiZpPVdLMHFVS1dpTTMzVyZzPWNvbnN1bWVyc2VjcmV0Jng9MDQ-&query={jan}'

      r = requests.get(request_url)
      resp = r.json()

      if len(resp["hits"]) >= 1:
          print('在庫あり')
          name = resp["hits"][0]['name']
          item_url = resp["hits"][0]['url']
          send_tweet(f'<Yahoo>\n{name}\n{item_url}')
          print(f'<Yahoo>\n\n{name}\n\n{item_url}')
      else:
          print('在庫なし')

if __name__ == "__main__":
    main()