import os
from os.path import join, dirname

from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.models.condition import Condition
from paapi5_python_sdk.models.get_items_request import GetItemsRequest
from paapi5_python_sdk.models.get_items_resource import GetItemsResource
from paapi5_python_sdk.models.partner_type import PartnerType
from amazon.paapi import AmazonAPI


import pprint
import json
import re
import csv

from dotenv import load_dotenv
from common.logger import set_logger
from common.google_spreadsheet import *
from twitter.twitter_tweet import *
from discord.discord_post import *

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

logger = set_logger(__name__)


KEY    = os.environ["AMAZON_API_KEY"]
SECRET = os.environ["AMAZON_API_SECRET"]
TAG    = os.environ["AMAZON_API_PARTNER_TAG"]
COUNTRY = "JP"

def detect_amazon_stock():
    amazon = AmazonAPI(KEY, SECRET, TAG, COUNTRY)
    jan_list = download_target_jan('Amazon')

    for jan in jan_list:
        if jan == '':
            pass
        else:
            products = amazon.search_items(keywords=jan)
            amazon_df = pd.read_csv('jan_csv/amazon_jan.csv',encoding='cp932',header=None)

            # 結果が１件以上あれば在庫ありとみなす
            if len(products["data"][0]) >= 1:
                if jan in amazon_df.values.astype(str):
                    logger.info(f'ツイート済みの商品{jan}')
                else:
                    name = products["data"][0].item_info.title.display_value
                    item_url = products["data"][0].detail_page_url
                    logger.info(f"在庫あり:{jan}")
                    send_tweet(f'<Amazon>\n{name}\n{item_url}')
                    send_discord(f'<Amazon>\n{name}\n{item_url}')
                    with open('jan_csv/amazon_jan.csv','a') as f:
                        writer = csv.writer(f)
                        writer.writerow([])
                        writer.writerow([jan])
            else:
                logger.info(f"在庫なし:{jan}")
                if jan in amazon_df.values.astype(str):
                    delete_jan = amazon_df.replace(jan, 'soldout')
                    delete_jan.to_csv('jan_csv/amazon_jan.csv', index=False,header=None)


if __name__ == "__main__":
    detect_amazon_stock()
