import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

DATA_URL=("bestsellers_with_categories_2022_03_27.csv")

st.set_page_config(
        page_title="Amazon Bestsellers",
        layout="wide",
    )
st.title("Amazon Bestsellers")	
st.markdown(' This application is a Streamlit dashboard that can be used to analyze Amazons bestseller data')

@st.cache(persist=True)
def loadData(row_limit):
    df = pd.read_csv(DATA_URL,nrows=row_limit)
    df.rename(lambda x: str(x).lower(),axis='columns',inplace=True)
    return df

data_frame = loadData(10000)

# st.subheader("Breakdown by minutes between %i and %i hours" % (hour,hour+1))
# filtered=data_frame[(data_frame['crash_date_crash_time'].dt.hour>=hour) & (data_frame['crash_date_crash_time'].dt.hour<hour+1)]
# hist=np.histogram(filtered['crash_date_crash_time'].dt.minute,bins=60,range=(0,60))[0]
# chart_data = pd.DataFrame({"minute":range(60),"crashes":hist})
# fig = px.bar(chart_data,x='minute',y='crashes',hover_data=['minute','crashes'],height=400)
# st.write(fig)

    
st.header("Book by Genre")
select = st.selectbox('Select a Genre',['Fiction','Non-Fiction'])
number = st.slider('Number of books',1,388)

if select == 'Fiction':
    st.write(data_frame.query("genre== 'Fiction'")[["name"]].sort_values(by=['name'],ascending=True)[:number])	
    # .sort_values(by=['injured_pedestrians'],ascending=False).dropna(how="any")
elif select == 'Non-Fiction':
    st.write(data_frame.query("genre== 'Non Fiction'")[["name"]].sort_values(by=['name'],ascending=True)[:number])

st.header("User Rating by Genre from 2009-2022")
fig=plt.figure(figsize=(15, 7))
sns.set_style("dark")
sns.lineplot(x="year", y="user rating",
             hue="genre",
             data=data_frame)
st.pyplot(fig)
st.write("There seems to be an increase in the number of user ratings for bestselling fiction and non-fiction books over the years. The year 2019 especially seems to have a high quantity of user ratings in the Fiction Genre. The Covid-19 pandemic could have insilled people to get back to reading books, and this could be the reason why the quantity of user ratings")

st.header("Price by Genre from 2009-2022")
fig=plt.figure(figsize=(12, 7))
sns.set_style("dark")
sns.lineplot(x="year", y="price",
             hue="genre",
             data=data_frame)
st.pyplot(fig)
st.write("Another reason for the sudden increase in the number of reviews and user ratings on Amazon could be attributed to the price of books. It looks like the prices of both fiction and non-fiction books (top-50) reduced significantly on Amazon's website. The reduction is prices of bestelling novels along with the effects of the covid-19 pandemic have caused more people to buy books and review them on Amazon")

st.header("Number of Fiction vs Non Fiction books in Amazons top-50 list from 2009-2022")
df=data_frame.groupby(['genre', 'year']).size().reset_index(name='counts')
fig=plt.figure(figsize=(15, 7))
sns.set_style("dark")
sns.barplot(x='year', y='counts', hue='genre', data=df)
st.pyplot(fig)
st.write("Even though the popularity of Fiction novels is greater than that of non-fiction, it looks like there are more non-fiction books which are part of Amazon's top-50 bestselling books most years.")


st.header("User Rating vs Reviews")
fig=plt.figure(figsize=(15, 7))
sns.set_style("dark")
sns.scatterplot(x="user rating", y="reviews",data=data_frame)
st.pyplot(fig)

st.subheader("Check the box to see/play with raw data")    
if st.checkbox('Show Raw Data',False):
    st.write(data_frame)