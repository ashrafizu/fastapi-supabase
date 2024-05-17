import requests
from datetime import datetime, timezone
from supabase import create_client
import os
from dotenv import load_dotenv
load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = create_client(url, key)

# This is to call API endpoints
# print(requests.get("http://127.0.0.1:8000/items?count=20").json())
# print(datetime.now())
# print(
#   requests.post(
#     "http://127.0.0.1:8000/fuel-price",
#     json={
#   "date": datetime.now(timezone.utc),
#   "ron95": 9.0,
#   "ron97": 8.99,
#   "diesel": 7.77,
#   "series_type": "string"
#     }
#   ).json()
# )

payload = {
    "date": "2024-05-14",
    "ron95": 9.99,
    "ron97": 9.99,
    "diesel": 9.99,
    "series_type": "test"
  }
print(list(payload))



