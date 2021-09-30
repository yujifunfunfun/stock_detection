import os
import csv
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

import requests
from bs4 import BeautifulSoup
from common.logger import set_logger
from common.google_spreadsheet import *
from twitter.twitter_tweet import *
from discord.discord_post import *
import pandas as pd
import re

logger = set_logger(__name__)

def check_stock():

    jan_list = download_target_jan('ポケモンセンター')
    affiliate_urls = download_affiliate_url('ポケモンセンター')
    max_price_list = download_max_price('ポケモンセンター')

    for jan,url,max_price in zip(jan_list,affiliate_urls,max_price_list):        
        if jan == '':
            pass
        else:
            # 一度ツイートしたか確認
            pokemon_df = pd.read_csv('jan_csv/pokemon_jan.csv',encoding='cp932',header=None)            
            # 商品ページへ遷移
            ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)" \
                    "AppleWebKit/537.36 (KHTML, like Gecko)" \
                    "Chrome/60.0.3112.113"
            item_url = f'https://www.pokemoncenter-online.com/?main_page=product_list&keyword={jan}&from=search_form&stock=on'
            res = requests.get(item_url,headers={"User-Agent": ua})
            soup = BeautifulSoup(res.text, "html.parser")
            logger.info('商品ページへ遷移しました')
            price = soup.find('p', class_='price').text
            p = r'(.*)円' 
            price = re.search(p, price).group(1)
            # 在庫確認
            logger.info('在庫確認中')
            if soup.find('img',class_='item_image'):
                if jan in pokemon_df.values.astype(str):
                    logger.info(f'ツイート済みの商品{jan}')
                elif int(price) < max_price:
                    name = soup.find_all('p', class_='name')
                    logger.info(f"在庫あり:{jan}")
                    send_tweet(f'<ポケモンセンターオンライン>\n{name[-1].text}\n{url}')
                    send_discord(f'<ポケモンセンターオンライン>\n{name[-1].text}\n{url}')
                
                    # CSVに保存
                    with open('jan_csv/pokemon_jan.csv','a',newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([jan])
            else:
                logger.info(f"在庫なし:{jan}")
                if jan in pokemon_df.values.astype(str):
                    delete_jan = pokemon_df.replace(jan, 'soldout')
                    delete_jan.to_csv('jan_csv/pokemon_jan.csv', index=False,header=None)
                    logger.info(f"再売り切れ:{jan}")


def detect_pokemoncenter_stock():
    check_stock()
        
        
# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    detect_pokemoncenter_stock()