import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np

JSON_PATH = './chrome-ability-324623-88b6a49f36bb.json'
SHEET_NAME = '在庫検知URL'


# スプレッドシートとの接続
def download_target_jan(site):

    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_PATH, scope)
    gc = gspread.authorize(credentials)

    if site == '楽天':
        worksheet = gc.open(SHEET_NAME).get_worksheet(0)
    elif site == 'Yahoo':
        worksheet = gc.open(SHEET_NAME).get_worksheet(1)

    url_list = worksheet.col_values(1)

    return url_list


