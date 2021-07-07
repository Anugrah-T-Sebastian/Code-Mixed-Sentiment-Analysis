#import settings2 as settings
#import mysql.connector
import pandas as pd
import time
import datetime
import plotly.express as px
import plotly.offline as py
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import nltk
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

df = pd.read_csv(r"C:\Users\Anugrah\FlaskSentiment\Sentiment\oneplus_tweets.csv")


#UTC for date time at default

df['created_at'] = pd.to_datetime(df['created_at'])

fig = make_subplots(
    rows=2, cols=2,
    column_widths=[1, 0.4],
    row_heights=[0.6, 0.4],
    subplot_titles=("OnePlus Mentions By Sentiment vs Time", "Sentiment Distribution", "Most Frequent Words"),
    specs=[[{"type": "scatter", "rowspan": 2}, {"type": "pie"}],
           [            None                    , {"type": "bar"}]],
    horizontal_spacing=0.2
    )


'''
Plot the Line Chart
'''
# Clean and transform data to enable time series
result = df.groupby([pd.Grouper(key='created_at', freq='15min'), 'sentiment']).count().unstack(fill_value=0).stack().reset_index()
result = result.rename(columns={"id_str":"Num of OnePlus mentions", "created_at":"Time in UTC"})  
time_series = result["Time in UTC"].drop_duplicates()
fig.add_trace(go.Scatter(
    x=time_series,
    y=result["Num of OnePlus mentions"][result['sentiment']==2].reset_index(drop=True),
    name="Neutral",
    opacity=0.1,
    fill='tonexty'), row=1, col=1)
fig.add_trace(go.Scatter(
    x=time_series,
    y=-1*result["Num of OnePlus mentions"][result['sentiment']==0].reset_index(drop=True),
    name="Negative",
    opacity=0.1,
    fill='tozeroy'), row=1, col=1)   
fig.add_trace(go.Scatter(
    x=time_series,
    y=result["Num of OnePlus mentions"][result['sentiment']==1].reset_index(drop=True),
    name="Positive",
    opacity=0.1,
    fill='tozeroy'), row=1, col=1)
fig.update_layout(template="plotly_dark", hovermode='x unified')
fig.update_xaxes(title_text="Number of OnePlus mentions", row=1, col=1)
fig.update_yaxes(title_text="Count", row=1, col=1)
fig.show()



'''
Plot the Bar Chart
'''
content = ' '.join(df["text"])
tokenized_word = word_tokenize(content)
stop_words=set(stopwords.words("english"))
filtered_sent=[]
for w in tokenized_word:
    if w not in stop_words:
        filtered_sent.append(w)
fdist = FreqDist(filtered_sent)
fd = pd.DataFrame(fdist.most_common(10), columns = ["Word","Frequency"]).drop([0]).reindex()

# Plot Bar chart   
fig.add_trace(go.Bar(x=fd["Word"], y=fd["Frequency"], name="Freq Dist"), row=2, col=2)
# 59, 89, 152
fig.update_traces(marker_color='rgb(59, 89, 152)', marker_line_color='rgb(8,48,107)', \
        marker_line_width=0.5, opacity=0.7, row=2, col=2)
fig.update_xaxes(title_text="Word", row=2, col=2)
fig.update_yaxes(title_text="Count", row=2, col=2)
fig.show()


'''
Plot the Donut Chart
'''
labels = ['Neutral','Positive','Negative']
distr = df.groupby('sentiment').count()
values = [distr.id_str[2], distr.id_str[1], distr.id_str[0]]

fig.add_trace(go.Pie(labels=labels, values=values, hole=.4), row=1, col=2)
fig.update_traces(hoverinfo='label+percent', textinfo='value', row=1, col=2)
fig.show()


fig.write_html(r"C:\Users\Anugrah\FlaskSentiment\Sentiment\Templates\chart1.html")