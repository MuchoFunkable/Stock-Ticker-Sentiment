# Stock Ticker Sentiment

This project is a Streamlit-based web application that displays stock price data and news sentiment analysis for selected stocks. It combines financial data from Yahoo Finance with news sentiment analysis using the NewsAPI and NLTK.

## Features

- Fetches and displays stock price data for selected stocks (AAPL, MSFT, GOOGL)
- Performs sentiment analysis on recent news articles related to each stock
- Visualizes stock prices and sentiment scores on an interactive chart

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/stock-ticker-sentiment.git
   cd stock-ticker-sentiment
   ```

2. Install dependencies using Poetry:

   ```
   poetry install
   ```

3. Set up your News API key:

   - Sign up for a free API key at [https://newsapi.org/](https://newsapi.org/)
   - Create a `.streamlit/secrets.toml` file in the project root
   - Add your API key to the secrets file:

     ```
     NEWS_API_KEY = "your_api_key_here"

     ```

## Usage

1. Activate the Poetry environment:

   ```
   poetry shell
   ```

2. Run the Streamlit app:

   ```
   streamlit run app.py
   ```

3. Open your web browser and navigate to the URL provided by Streamlit (usually http://localhost:8501).

4. Use the dropdown menu to select a stock and view its price data and sentiment analysis.

## How It Works

1. Stock data is fetched using the `yfinance` library.
2. News articles are retrieved using the NewsAPI.
3. Sentiment analysis is performed on the news articles using NLTK's VADER sentiment analyzer.
4. The data is visualized using Streamlit and Plotly.

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the web app framework
- [yfinance](https://github.com/ranaroussi/yfinance) for stock data
- [NewsAPI](https://newsapi.org/) for news articles
- [NLTK](https://www.nltk.org/) for sentiment analysis
