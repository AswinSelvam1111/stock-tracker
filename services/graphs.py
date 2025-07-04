import sqlite3
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

def lineGraph(tableName):
    dbPath = os.path.join("services", "stockhistory.db")
    conn = sqlite3.connect(dbPath)

    query = f"SELECT date, price FROM {tableName} ORDER BY date ASC"
    dataFrame = pd.read_sql_query(query, conn)
    dataFrame['date'] = pd.to_datetime(dataFrame['date'], format='%Y-%m-%d %H:%M')

    #for simplicity sake
    threeMonthsAgo = datetime.now() - timedelta(days=90)
    dataFrame = dataFrame[dataFrame['date'] >= threeMonthsAgo]

    if dataFrame.empty:
        print("Please run the script that helps me scour the internet for information!")
        conn.close()
        return

    fig = go.Figure()
    for i in range(1, len(dataFrame)):
        x = [dataFrame['date'].iloc[i - 1], dataFrame['date'].iloc[i]]
        y = [dataFrame['price'].iloc[i - 1], dataFrame['price'].iloc[i]]
        color = 'green' if y[1] >= y[0] else 'red'
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='lines',
            line=dict(color=color),
            hoverinfo='x+y',
            showlegend=False
        ))


    sharedaxis = dict(
        showspikes=True,
        spikemode='across',
        spikesnap='cursor',
        spikecolor='gray',
        spikethickness=0.5,  
        showline=True
    )
    

    fig.update_layout(
        title=dict(
            text=f"<u>{tableName} Stock Price (Last 3 Months)</u>", 
            font=dict(size=18, family="Arial Black", color="black")  #bc the library doesnt allow bolding words
        ),
        xaxis_title=dict(
            text="Date",
            font=dict(size=14, family="Arial Black", color="black")
        ),
        yaxis_title=dict(
            text="Price (USD)",
            font=dict(size=14, family="Arial Black", color="black")
        ),
        hovermode="closest",
        
        xaxis = sharedaxis,
        yaxis = sharedaxis,

        spikedistance=-1,
    )

    fig.show()
    conn.close()
