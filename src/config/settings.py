import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    HOST = os.environ.get('HOST')
    PORT = os.environ.get('PORT')

    AUTH_URL = os.environ.get('AUTH_URL')
    PROFILE_URL = os.environ.get('PROFILE_URL')

    TIME_COOKIES = os.environ.get('TIME_COOKIES')
