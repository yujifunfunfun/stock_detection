import os
from os.path import join, dirname
import tweepy
from dotenv import load_dotenv
from common.logger import set_logger

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

logger = set_logger(__name__)

# 準備で取得したキーを格納する
consumer_key = os.environ.get("TWITTER_API_KEY")
consumer_secret = os.environ.get("TWITTER_API_SECRET")
access_token = os.environ.get("TWITTER_API_TOKEN")
access_token_secret = os.environ.get("TWITTER_API_TOKEN_SECRET")


def send_tweet(message):
    # Twitterオブジェクトの生成
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # tweetを投稿
    try:
        api.update_status(message)
    except Exception as e:
        logger.error(e)

def send_tweet_with_img(message):
    # Twitterオブジェクトの生成
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # tweetを投稿
    try:
        api.update_with_media(filename='img/1.jpg',status=message)
    except Exception as e:
        logger.error(e)

if __name__ == "__main__":
    send_tweet()