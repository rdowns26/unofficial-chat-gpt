import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

OPENAI_EMAIL = os.environ.get("OPENAI_EMAIL")
OPENAI_PASSWORD = os.environ.get("OPENAI_PASSWORD")
BROWSERLESS_KEY = os.environ.get("BROWSERLESS_KEY")
TWILIO_NUMBER = os.environ.get("TWILIO_NUMBER")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")