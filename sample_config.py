import os

class Config(object):
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
    IMGBB_API_KEY = os.environ.get("IMGBB_API_KEY", "")
