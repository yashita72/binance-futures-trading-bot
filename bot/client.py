from binance.client import Client
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

client = Client(API_KEY, API_SECRET)

client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

print("Binance Testnet Connected Successfully!")