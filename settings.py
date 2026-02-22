import os
from dotenv import load_dotenv

load_dotenv()


class URL:
    MAIN = os.getenv("MAIN_URL")
    LOGIN = "login"

class User:
    MAIL = os.getenv("USER_MAIL")
    PASSWORD = os.getenv("USER_PASSWORD")
