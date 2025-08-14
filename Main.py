# main.py
from fastapi import FastAPI
import requests
from datetime import datetime, timedelta
import yfinance as yf
import time
from fastapi.middleware.cors import CORSMiddleware
import random
from datetime import datetime, timedelta
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://jar-nox-frontend0.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cache = {}
CACHE_EXPIRY = 60  # seconds

NEWS_API_KEY = os.getenv("NEWS_API_KEY")  # Get from newsapi.org (free)


def get_mock_data(symbol: str):
    days = [datetime.now() - timedelta(days=i) for i in range(7)]
    days.reverse()

    price = 150  # starting price
    data = []
    for d in days:
        # simulate a daily random change between -3 and +3
        change = random.uniform(-3, 3)
        price += change
        data.append({
            "date": d.strftime("%Y-%m-%d"),
            "close": round(price, 2)
        })
    return data

def fetch_stock_data(symbol: str):
    try:
        df = yf.download(symbol, period="1mo", interval="1d", progress=False)
        if df.empty:
            raise ValueError("No data returned")
        return [
            {"date": idx.strftime("%Y-%m-%d"), "close": float(row["Close"])}
            for idx, row in df.iterrows()
        ]
    except:
        return get_mock_data(symbol)

@app.get("/stocks/{symbol}")
def get_stock(symbol: str):
    now = time.time()
    if symbol in cache and (now - cache[symbol]["timestamp"] < CACHE_EXPIRY):
        return cache[symbol]["data"]
    data = fetch_stock_data(symbol)
    cache[symbol] = {"data": data, "timestamp": now}
    return data

@app.get("/companies")
def get_companies():
    return ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "META", "NFLX", "NVDA", "BABA", "ORCL"]

# --------------------------
# NEW NEWS ENDPOINT
# --------------------------
def get_mock_news(symbol: str):
    return [
        {"title": f"{symbol} Dominates the Cyber Markets", "url": "#"},
        {"title": f"Dark Tech Surge as {symbol} Expands", "url": "#"},
        {"title": f"{symbol} Investors Eye Neon Profits", "url": "#"}
    ]

@app.get("/news/{symbol}")
def get_news(symbol: str):
    try:
        url = f"https://newsapi.org/v2/everything?q={symbol}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        res = requests.get(url, timeout=5)
        if res.status_code != 200:
            raise ValueError("News API failed")
        articles = res.json().get("articles", [])
        if not articles:
            raise ValueError("No news found")
        return [{"title": a["title"], "url": a["url"]} for a in articles[:5]]
    except Exception as e:
        print(f"⚠️ News fetch failed for {symbol}: {e}")
        return get_mock_news(symbol)
