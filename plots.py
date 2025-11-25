import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


def sentiment_chart(sentiment_count, chart_type: str = "Histogram"):
    """Return a Plotly figure for sentiment counts.

    `chart_type` can be "Histogram" or "Pie Chart" (matching the UI values).
    """
    if chart_type == "Histogram":
        fig = px.bar(sentiment_count, x="Sentiment", y="Tweets", color="Tweets", height=500)
    else:
        fig = px.pie(sentiment_count, values="Tweets", names="Sentiment")
    return fig


def airline_hist(choice_data):
    """Return a Plotly histogram for selected airlines broken down by sentiment."""
    fig_choice = px.histogram(choice_data, x="airline", y="airline_sentiment", histfunc="count",
                             color="airline_sentiment", facet_col="airline_sentiment",
                             labels={"airline_sentiment":"Tweets"}, height=600, width=800)
    return fig_choice


def generate_wordcloud(processed_words: str, width: int = 800, height: int = 640, background_color: str = "white"):
    """Return a Matplotlib Figure with the generated word cloud."""
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color=background_color, height=height, width=width).generate(processed_words)
    fig = plt.figure(figsize=(width / 100, height / 100))
    plt.imshow(wordcloud)
    plt.axis("off")
    return fig
