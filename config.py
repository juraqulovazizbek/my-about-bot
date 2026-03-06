import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    TOKEN = os.getenv("TOKEN", "")
    ADMIN_IDS = [
        int(x.strip())
        for x in os.getenv("ADMIN_IDS", "").split(",")
        if x.strip().isdigit()
    ]