# Sentiment Analysis Dashboard — US Airlines Tweets

A small Streamlit dashboard to explore sentiment in tweets about US airlines. The app reads `Dataset/Tweets.csv` and provides interactive visualizations: sentiment distribution, tweet locations by hour, airline sentiment breakdowns, and word clouds.

Tech & Tools
- Python 3.8+
- Streamlit — interactive dashboard UI
- Pandas & NumPy — data loading and processing
- Plotly — interactive charts
- WordCloud & Matplotlib — word cloud generation


Project layout
- `app.py` — Streamlit entrypoint (UI)
- `data.py` — data loading & preprocessing
- `plots.py` — plotting helpers
- `Dataset/Tweets.csv` — tweets dataset (required)

Notes
- Place the dataset at `Dataset/Tweets.csv` relative to the project root.
- Add a `requirements.txt` or `LICENSE` if you plan to publish to GitHub.
