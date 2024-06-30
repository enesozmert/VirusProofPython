import plotly.graph_objs as go
import plotly.io as pio
import pandas as pd
from database import fetch_data
import logging

def create_plot():
    try:
        query = "SELECT DayOfWeek, ScanCount, PreviousWeekScanCount FROM WebHit"
        data = fetch_data(query)

        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        data_sorted = sorted(data, key=lambda x: days_order.index(x[0]))

        days = [row[0] for row in data_sorted]
        counts = [row[1] for row in data_sorted]
        previous_counts = [row[2] for row in data_sorted]

        df = pd.DataFrame({'Days': days, 'ScanCount': counts, 'LastWeek': previous_counts})

        trace1 = go.Scatter(
            x=df['Days'],
            y=df['ScanCount'],
            mode='lines+markers',
            name='ScanCount',
            line=dict(color='#08F7FE'),
            marker=dict(size=8)
        )

        trace2 = go.Scatter(
            x=df['Days'],
            y=df['LastWeek'],
            mode='lines+markers',
            name='LastWeek',
            line=dict(color='#FE53BB', dash='dash'),
            marker=dict(size=8)
        )

        layout = go.Layout(
            title='Weekly Scan Statistics',
            xaxis=dict(title='Days'),
            yaxis=dict(title='Number of Scans'),
            template='plotly_dark',
        )

        fig = go.Figure(data=[trace1, trace2], layout=layout)

        # HTML dosyasını kaydet
        pio.write_html(fig, file='templates/plot.html', auto_open=False)

        logging.info('Plot created and saved to templates/plot.html')
    except Exception as e:
        logging.error(f'Error creating plot: {e}')
