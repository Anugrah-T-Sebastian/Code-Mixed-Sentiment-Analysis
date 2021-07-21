import mysql.connector
import datetime
import time
import pandas as pd
import json
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import nltk
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import itertools

db_connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "rootpassword",
    database = "TwitterDB",
    charset = "utf8"
)

def getChart(days = 2, hours = 0, mins = 0, freq = "4min", brand = "OnePlus"):
    if brand == "OnePlus":
        TABLE_NAME = "OnePlusStream"
    elif brand == "Airtel":
        TABLE_NAME = "Airtel"
    else:
        TABLE_NAME = "BJP"

    time_now = datetime.datetime(2021, 6, 11, 10, 18, 27)
    # time_now = datetime.datetime.utcnow()
    time_interval = datetime.timedelta(days=days, hours=hours, minutes=mins)
    start_time = (time_now - time_interval).strftime('%Y-%m-%d %H:%M:%S')
    query = "SELECT id_str, text, created_at, sentiment, user_location FROM {} WHERE created_at >= '{}'".format(TABLE_NAME, start_time)
    df = pd.read_sql(query, con=db_connection)
    df['created_at'] = pd.to_datetime(df['created_at'])

    fig = make_subplots(
        rows = 3, 
        cols = 5,
        column_widths = [0.7, 0.7, 0.7, 1, 1],
        row_heights = [1, 0.7, 1],
        subplot_titles = (
            "Mentions over Time", 
            "Most Frequent Words", 
            "Sentiment Distribution", 
            "Mentions Across India"
        ),
        specs = [
            [{"type": "scatter", "rowspan": 3, "colspan": 3}, None, None, {"type": "bar"}, {"type": "pie"}],
            [None, None, None, {"type": "choropleth", "colspan": 2, "rowspan": 2}, None],
            [None, None, None, None, None]
        ],
        horizontal_spacing = 0.08,
        vertical_spacing = 0.25,
    )


    fig.update_annotations(font_size=18)
    fig.update_layout(
        template = "plotly_dark", 
        hovermode = 'x unified',  
        margin = {
            'r': 30, 
            't': 30, 
            'l': 30, 
            'b': 30
        }
    )

    result = df.groupby([pd.Grouper(key = 'created_at', freq = freq), 'sentiment']).count().unstack(fill_value = 0).stack().reset_index()
    result = result.rename(columns = {"id_str":"Num of mentions", "created_at":"Time in UTC"})  
    time_series = result["Time in UTC"].drop_duplicates()

    fig.add_trace(
        go.Scatter(
            x = time_series,
            y = result["Num of mentions"][result['sentiment'] == 2].reset_index(drop=True),
            name = "Neutral",
            opacity = 0.1,
            fill = 'tonexty'
        ), 
        row = 1, 
        col = 1
    )
    fig.add_trace(
        go.Scatter(
            x = time_series,
            y = -1*result["Num of mentions"][result['sentiment'] == 0].reset_index(drop = True),
            name = "Negative",
            opacity = 0.1,
            fill = 'tozeroy'
        ),  
        row = 1, 
        col = 1
    )   
    fig.add_trace(
        go.Scatter(
            x = time_series,
            y = result["Num of mentions"][result['sentiment'] == 1].reset_index(drop = True),
            name = "Positive",
            opacity = 0.1,
            fill = 'tozeroy'
        ), 
        row = 1, 
        col = 1 
    )

    fig.update_traces(
        showlegend = False, 
        row = 1,
        col = 1
    )


    content = ' '.join(df["text"])
    tokenized_word = word_tokenize(content)
    stop_words = set(stopwords.words("english"))
    filtered_sent = []
    for w in tokenized_word:
        if w not in stop_words:
            filtered_sent.append(w)
    fdist = FreqDist(filtered_sent)
    fd = pd.DataFrame(fdist.most_common(10), columns = ["Word","Frequency"]).drop([0]).reindex()

    fig.add_trace(
        go.Bar(
            x = fd["Word"], 
            y = fd["Frequency"], 
            name = "Freq Dist"
        ), 
        row = 1, 
        col = 4
    )

    fig.update_traces(
        marker_color = '#FF7F0E', 
        marker_line_color = '#EF553B',
        marker_line_width = 0.5, 
        showlegend = False, 
        opacity=0.7, 
        row=1, 
        col=4
    )


    labels = ['Negative', 'Positive', 'Neutral']
    distr = df.groupby('sentiment').count()
    values = []
    for ix in range(3):
        if ix in distr.id_str:
            values.append(distr.id_str[ix])
        else:
            values.append(0) 

    fig.add_trace(
        go.Pie(
            labels = labels, 
            values = values, 
            hole = .4, 
            marker = {
                'colors': [
                    'red',
                    'rgb(10,134,10)',
                    '#3366CC'
                ]
            }
        ), 
        row = 1, 
        col = 5
    )

    fig.update_traces(
        hoverinfo = 'label+value+percent', 
        textinfo = 'none',
        row=1, 
        col=5
    )


    CITIES = {
    'noida': 'Delhi', 
    'gurgaon': 'Delhi', 
    'gurugram': 'Delhi',
    'ghaziabad': 'Delhi',
    'faridabad': 'Delhi',
    'dwarka': 'Delhi',
    'bawana': 'Delhi',
    'ahmedabad': 'Gujarat', 
    'pune': 'Maharashtra',
    'chennai': 'Tamil Nadu',
    'hyderabad': 'Telangana',
    'visakhapatnam': 'Andhra Pradesh',
    'amaravati': 'Andhra Pradesh',
    'itanagar': 'Andhra Pradesh',
    'dispur': 'Assam',
    'shillong': 'Meghalaya',
    'bhopal': 'Madhya Pradesh',
    'patna': 'Bihar',
    'gandhinagar': 'Gujarat',
    'bhubaneswar': 'Odisha',
    'kolkata': 'West Bengal',
    'ranchi': 'Jharkhand',
    'dehradun': 'Uttarakhand',
    'thiruvananthapuram': 'Kerala',
    'jaipur': 'Rajasthan',
    'raipur': 'Chhattisgarh',
    'bilaspur': 'Chhattisgarh',
    'bhilai': 'Chhattisgarh',
    'korba': 'Chhattisgarh',
    'raigarh': 'Chhattisgarh',
    'ambikapur': 'Chhattisgarh',
    'jagdalpur': 'Chhattisgarh',
    'rajnandgaon': 'Chhattisgarh',
    'panaji': 'Goa',
    'surat': 'Gujarat',
    'ludhiana': 'Punjab',
    'shimla': 'Himachal Pradesh',
    'dharamshala': 'Himachal Pradesh',
    'bengaluru': 'Karnataka',
    'bangalore': 'Karnataka',
    'kochi': 'Kerala',
    'coimbatore': 'Tamil Nadu',
    'madurai': 'Tamil Nadu',
    'kozhikode': 'Kerala',
    'mumbai': 'Maharashtra',
    'thane': 'Maharashtra',
    'imphal': 'Manipur',
    'guwahati': 'Assam',
    'gangtok': 'Sikkim',
    'darjeeling': 'West Bengal',
    'aizawl': 'Mizoram',
    'kohima': 'Nagaland',
    'jodhpur': 'Rajasthan',
    'udaipur': 'Rajasthan',
    'jaisalmer': 'Rajasthan',
    'lucknow': 'Uttar Pradesh',
    'agartala': 'Tripura',
    'nashik': 'Maharashtra',
    'nagpur': 'Maharashtra',
    'dhaka': 'Bangladesh',
    'srinagar': 'Jammu and Kashmir'
    }

    STATES = [
    'Andhra Pradesh', 'AP', 
    'Arunachal Pradesh', 'AR', 
    'Assam', 'AS', 
    'Bihar', 'BR', 
    'Chhattisgarh', 'CG', 
    'Goa', 'GA',
    'Gujarat', 'GJ',
    'Haryana', 'HR',
    'Himachal Pradesh', 'HP', 
    'Jharkhand', 'JH',
    'Karnataka', 'KA',
    'Kerala', 'KL', 
    'Madhya Pradesh', 'MP',
    'Maharashtra', 'MH', 
    'Manipur', 'MN', 
    'Meghalaya', 'ML', 
    'Mizoram', 'MZ', 
    'Nagaland', 'NL', 
    'Odisha', 'OD', 
    'Punjab', 'PB',
    'Rajasthan', 'RJ', 
    'Sikkim', 'SK', 
    'Tamil Nadu', 'TN', 
    'Telangana', 'TS', 
    'Tripura', 'TR', 
    'Uttar Pradesh', 'UP', 
    'Uttarakhand', 'UK', 
    'West Bengal', 'WB', 
    'Chandigarh', 'CH', 
    'Delhi', 'DL', 
    'Jammu and Kashmir', 'JK', 
    'Ladakh', 'LA'
    ]
    STATE_DICT = dict(itertools.zip_longest(*[iter(STATES)] * 2, fillvalue=""))
    INV_STATE_DICT = dict((v,k) for k,v in STATE_DICT.items())


    is_in_IN = []
    geo = df[['user_location']]
    df = df.fillna(" ")
    for x in df['user_location']:
        check = False
        for s in STATES:
            if s.lower() in x:
                is_in_IN.append(STATE_DICT[s] if s in STATE_DICT else s)
                check = True
                break
        if not check:
            for city in CITIES:
                if city in x:
                    is_in_IN.append(STATE_DICT[CITIES[city]])
                    check = True
            if not check:
                is_in_IN.append(None)

    geo_dist = pd.DataFrame(is_in_IN, columns = ['State']).dropna().reset_index()
    geo_dist = geo_dist.groupby('State').count().rename(columns = {"index": "Number"}).sort_values(by = ['Number'], ascending=False).reset_index()
    geo_dist['Full State Name'] = geo_dist['State'].apply(lambda x: INV_STATE_DICT[x])
    geo_dist['text'] = geo_dist['Full State Name'] + '<br>' + 'Num: ' + geo_dist['Number'].astype(str)

    fig.add_trace(
        go.Choropleth(
            geojson = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey = 'properties.ST_NM',
            locationmode = 'geojson-id',
            locations = geo_dist['Full State Name'],
            z = geo_dist['Number'],
            autocolorscale = False,
            colorscale = 'Mint',
            marker_line_color = 'black',
            text = geo_dist['text'],
            colorbar = dict(
                thickness = 20,
                len = 0.40,
                yanchor = 'bottom',
                y = 0.15
            )
        ),  
        row = 2, 
        col = 4
    )

    fig.update_geos(
        visible = False,
        projection = dict(
            type = 'conic conformal',
            parallels = [12.472944444, 35.172805555556],
            rotation = {'lat': 24, 'lon': 80}
        ),
        lonaxis = {'range': [68, 98]},
        lataxis = {'range': [6, 38]}
    )

    fig.update_traces(
        hoverinfo = 'text', 
        row = 2, 
        col = 4
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON