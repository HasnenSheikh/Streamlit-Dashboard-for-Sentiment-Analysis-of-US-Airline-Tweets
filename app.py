import numpy as np
import pandas as pd
import streamlit as st

from data import load_data, map_plot_data
from plots import sentiment_chart, airline_hist, generate_wordcloud


st.title("Sentiment Analysis of Tweets about US Airlines")
st.sidebar.title("Sentiment Analysis of Tweets about US Airlines")

st.markdown("Streamlit Dashboard to analyze the sentiment of Tweets 🐦")
st.sidebar.markdown("Streamlit Dashboard to analyze the sentiment of Tweets 🐦")


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
    fig = sentiment_chart(sentiment_count, select)
    st.plotly_chart(fig)


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
    fig_choice = airline_hist(choice_data)
    st.plotly_chart(fig_choice)


st.sidebar.subheader("Word Cloud")
word_sentiment = st.sidebar.radio("Display word cloud for what sentiment??", ("Positive", "Neutral", "Negative"))

if not st.sidebar.checkbox("Hide", True, key="3"):
    st.header("Word cloud for %s sentiment" % (word_sentiment))
    df = data[data["airline_sentiment"]==word_sentiment.lower()]
    words = " ".join(df["text"])
    processed_words = " ".join([word for word in words.split() if "http" not in word and not word.startswith("@") and word != "RT"])
    fig_wc = generate_wordcloud(processed_words)
    st.pyplot(fig_wc)


