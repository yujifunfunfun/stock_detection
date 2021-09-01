import os
from discordwebhook import Discord
from os.path import join, dirname
from dotenv import load_dotenv
from common.logger import set_logger

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

logger = set_logger(__name__)


webfook_url = os.environ.get("DISCORD_WEBFOOK_URL")
discord = Discord(url=webfook_url)


def send_discord(text):
    try:
        discord.post(content=text)
    except Exception as e:
        logger.error(e)
