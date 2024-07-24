import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from newsapi import NewsApiClient
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from datetime import datetime, timedelta
import yfinance as yf

# Download NLTK data (run this once)
nltk.download('vader_lexicon')

st.set_page_config(page_title="Stock Data and News Sentiment Viewer", layout="wide")
st.title("Stock Data and News Sentiment Viewer")

NEWS_API_KEY = st.secrets["NEWS_API_KEY"]

newsapi = NewsApiClient(api_key=NEWS_API_KEY)

selected_stocks = ['AAPL', 'MSFT', 'GOOGL']

def fetch_stock_data(symbols, start_date, end_date):
    data = {}
    for symbol in symbols:
        stock = yf.Ticker(symbol)
        hist = stock.history(start=start_date, end=end_date)
        data[symbol] = hist['Close']
    return pd.DataFrame(data)

def fetch_news_sentiment(symbol, from_date, to_date):
    try:
        articles = newsapi.get_everything(q=symbol, 
                                          from_param=from_date, 
                                          to=to_date, 
                                          language='en', 
                                          sort_by='publishedAt',
                                          page_size=100)  # Increase page size
        
        sia = SentimentIntensityAnalyzer()
        sentiments = []
        
        for article in articles['articles']:
            sentiment = sia.polarity_scores(article['title'])
            sentiments.append({
                'date': article['publishedAt'][:10],
                'sentiment': sentiment['compound'],
                'title': article['title'],
                'url': article['url']
            })
        
        return pd.DataFrame(sentiments)
    except Exception as e:
        st.error(f"Error fetching news data: {str(e)}")
        return None

end_date = datetime.now().date()
start_date = end_date - timedelta(days=30)

stock_data = fetch_stock_data(selected_stocks, start_date, end_date)

if not stock_data.empty:
    fig = go.Figure()

    for symbol in selected_stocks:
        fig.add_trace(go.Scatter(
            x=stock_data.index,
            y=stock_data[symbol],
            mode='lines',
            name=f"{symbol} Price"
        ))

        # Fetch and plot sentiment data
        sentiment_df = fetch_news_sentiment(symbol, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        
        if sentiment_df is not None and not sentiment_df.empty:
            sentiment_df['date'] = pd.to_datetime(sentiment_df['date'])
            
            # Calculate daily average sentiment
            daily_sentiment = sentiment_df.groupby('date')['sentiment'].mean().reset_index()
            
            fig.add_trace(go.Scatter(
                x=daily_sentiment['date'],
                y=daily_sentiment['sentiment'],
                mode='lines',
                name=f"{symbol} Sentiment",
                yaxis="y2"
            ))

            # Display articles used for sentiment analysis in an accordion
            st.write(f"### Articles used for {symbol} sentiment analysis:")
            with st.expander("Show articles"):
                for _, article in sentiment_df.iterrows():
                    st.write(f"{article['title']} (Sentiment: {article['sentiment']:.2f})")
                    st.write(f"Date: {article['date']}")
                    st.write(f"URL: {article['url']}")

    fig.update_layout(
        title="Stock Prices and News Sentiment",
        xaxis_title="Date",
        yaxis_title="Price",
        yaxis2=dict(
            title="Sentiment",
            overlaying="y",
            side="right",
            range=[-1, 1],
            tickvals=[-1, -0.5, 0, 0.5, 1],
            ticktext=["-1", "-0.5", "0", "0.5", "1"]
        ),
        legend_title="Stocks",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Unable to fetch stock data. Please try again later.")