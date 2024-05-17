import requests
from datetime import datetime, timezone
from supabase import create_client
import os
from dotenv import load_dotenv
load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = create_client(url, key)

# This is simple guide to call API, so you might need to disable RLS for specified table in supabase

# This is to call API endpoints
print(requests.get("http://127.0.0.1:8000/fuel-price").json())

payload = {
    "date": "2024-05-14",
    "ron95": 9.99,
    "ron97": 9.99,
    "diesel": 9.99,
    "series_type": "test"
  }




