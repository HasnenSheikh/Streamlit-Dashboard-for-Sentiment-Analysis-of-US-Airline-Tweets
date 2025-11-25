import ast
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.title("Sentiment Analysis of Tweets about US Airlines")
st.sidebar.title("Sentiment Analysis of Tweets about US Airlines")

st.markdown("Streamlit Dashboard to analyze the sentiment of Tweets 🐦")
st.sidebar.markdown("Streamlit Dashboard to analyze the sentiment of Tweets 🐦")

@st.cache_data
def load_data():
    data = pd.read_csv("Dataset/Tweets.csv")
    data["tweet_created"] = pd.to_datetime(data["tweet_created"])
    
    return data

data = load_data()

st.sidebar.subheader("Show random tweet")
random_tweet = st.sidebar.radio("Sentiment Type", ("Positive", "Neutral", "Negative"))
st.sidebar.markdown(data.query("airline_sentiment == @random_tweet.lower()")[["text"]].sample(n=1).iat[0,0])

st.sidebar.markdown("### Number of Tweets by sentiment")
select = st.sidebar.selectbox("Visualization Type", ["Histogram", "Pie Chart"], key="1")

sentiment_count = data["airline_sentiment"].value_counts()
sentiment_count = pd.DataFrame({"Sentiment":sentiment_count.index, "Tweets": sentiment_count.values})


if not st.sidebar.checkbox("Hide", True):
    st.markdown("### Number of Tweets by sentiment")
    if select == "Histogram":
        fig = px.bar(sentiment_count, x="Sentiment", y="Tweets", color="Tweets", height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values="Tweets", names="Sentiment")
        st.plotly_chart(fig)

def map_plot_data(data):
    data = data[data["tweet_coord"].notna()]
    data[["latitude", "longitude"]] = data["tweet_coord"].apply(
    lambda x: pd.Series(
        ast.literal_eval(x) if isinstance(x, str) else x
    ).reindex([0, 1])
)
    return data

map_data = map_plot_data(data)
st.sidebar.subheader("When and Where are users Tweeting from??")
hour = st.sidebar.slider("Hour of Day", 0, 23)
modified_data = map_data[map_data["tweet_created"].dt.hour==hour]

if not st.sidebar.checkbox("Hide", True, key="2"):
    st.markdown("### Tweets locations based on the time of the day")
    st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour+1)%24))
    st.map(modified_data)

    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)

st.sidebar.subheader("Breakdown airline tweets by sentiment")
choice = st.sidebar.multiselect("Pick Airlines", ("US Airways", "United", "American", "Southwest", "Delta", "Virgin America"), key="0")

if len(choice)>0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x="airline", y="airline_sentiment", histfunc="count", color="airline_sentiment",
                             facet_col="airline_sentiment", labels={"airline_sentiment":"Tweets"}, height=600, width=800)
    st.plotly_chart(fig_choice)


st.sidebar.subheader("Word Cloud")
word_sentiment = st.sidebar.radio("Display word cloud for what sentiment??", ("Positive", "Neutral", "Negative"))

if not st.sidebar.checkbox("Hide", True, key="3"):
    st.header("Word cloud for %s sentiment" % (word_sentiment))
    df = data[data["airline_sentiment"]==word_sentiment.lower()]
    words = " ".join(df["text"])
    processed_words = " ".join([word for word in words.split() if "http" not in word and not word.startswith("@") and word != "RT"])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color = "white", height=640, width=800).generate(processed_words)
    plt.imshow(wordcloud)
    plt.axis("off")
    st.pyplot(plt)


