Stock Dashboard Backend

This is the backend API for the cyber-gothic stock dashboard, built with FastAPI. It provides endpoints for stock data, company lists, market movers, sentiment analysis, and news articles. The backend supports both live API fetching and offline/mock data fallback.

Features

Company Data Endpoint: Fetch the list of available companies.

Stock Data Endpoint: Get historical stock prices for selected companies.

Market Movers Endpoint: Top gainers and losers.

Sentiment Analysis: Bullish, bearish, or neutral based on stock performance.

News Endpoint: Fetch latest news articles, with offline fallback for reliability.

Mock Data Support: Provides mock data for development or when APIs fail.

Tech Stack

Backend: Python 3.11+ & FastAPI

Data: Live API integrations & mock data generation

Server: Uvicorn ASGI server

Serialization: Pydantic models for data validation

Usage

Clone the repo:

git clone <your-repo-url>


Install dependencies:

pip install -r requirements.txt


Run the development server:

uvicorn Main:app --reload --port 8000


API is accessible at http://localhost:8000.
