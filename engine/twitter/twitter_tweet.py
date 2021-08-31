import tweepy


def send_tweet(message):
    # 準備で取得したキーを格納する
    consumer_key = "HJ6oxtsePATJYMqVHqsBzqUbT"
    consumer_secret = "sF9geAhhVGM6IHQ3zGOczx7MedgyeUokFNIiYtWmIn9pxGYdPQ"
    access_token = "1265632106132037633-NkkXbqyS2iaCeSlUtRW9GeDZrmQPGD"
    access_token_secret = "uDd2SpZ7y6d9oGqa3AM0XbSkJaC42cpwFsg1ZHoBFLutX"

    # Twitterオブジェクトの生成
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # tweetを投稿
    api.update_status(message)

if __name__ == "__main__":
    send_tweet()