import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    HOST = os.environ.get('HOST')
    PORT = os.environ.get('PORT')

    AUTH_URL = os.environ.get('AUTH_URL')
    PROFILE_URL = os.environ.get('PROFILE_URL')

    TIME_COOKIES = os.environ.get('TIME_COOKIES')

    SECRET_KEY=os.environ.get('JWT_KEY')
    ALGORITHM = os.environ.get("ALGORITHM", "HS256")

    IGNORE_PATH = os.environ.get('IGNORE_PATH')
    FORBIDDEN_SUPPORT_PATH = os.environ.get('FORBIDDEN_SUPPORT_PATH')
    FORBIDDEN_USER_PATH = os.environ.get('FORBIDDEN_USER_PATH')

    SESSION_KEY = os.environ.get('SESSION_KEY')
