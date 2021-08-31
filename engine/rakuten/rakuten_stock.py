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
    jan_list = download_target_jan('楽天')

    for jan in jan_list:
      request_url = f'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?applicationId=1071977349781880110&keyword={jan}'

      r = requests.get(request_url)
      resp = r.json()

      if len(resp["Items"]) >= 1:
          print('在庫あり')
          item = resp['Items'][0]['Item']
            #   item = i['Item']
          name = item['itemName']
          item_url = item['itemUrl']
          send_tweet(f'<楽天>\n{name}\n{item_url}')
          print(f'<楽天>\n\n{name}\n\n{item_url}')
      else:
          print('在庫なし')
 

if __name__ == "__main__":
    main()