from urllib2 import Request, urlopen
import json

## numpy and pandas to deal with data
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize

## bokeh for plot
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html

from flask import Flask, render_template, request, redirect

app = Flask(__name__)


## download the database
raw_request = Request('https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?qopts.columns=ticker,date,close,adj_close,open&date.gte=20161201&date.lt=20161231&api_key=mZzYwdeyrqRXhGWKzUg6')
response = urlopen(raw_request)
data_sticker_raw = response.read()
data_sticker_json = json.loads(data_sticker_raw)
data_sticker_messy_format = json_normalize(data_sticker_json['datatable'])

data_sticker = pd.DataFrame(data_sticker_messy_format.values[0][1], columns=['Ticker','Date','close', 'close_adj', 'open'])


@app.route('/')
def main():
    return redirect('/index')

@app.route('/index', methods=['GET'])
def index():
	#if request.method == 'GET':
    return render_template('userinfo.2.html',ans1='close',ans2='close_adj',ans3='open')

@app.route('/index_close',methods=['POST'])
def index_close():
    ticker_name = request.form['name']
    price_column = request.form['data_type']

    if ticker_name in list(data_sticker.Ticker):
        p = figure(plot_width=400, plot_height=400, x_axis_type="datetime")
        p.line(pd.to_datetime(data_sticker.Date[data_sticker.Ticker==ticker_name]), data_sticker[price_column][data_sticker.Ticker==ticker_name], color="navy", line_width=2)
        html = file_html(p, CDN, "Ticker Close Values")

        f = open('templates/close_plot.html','w')
        f.write(html)
        f.close()

        return render_template('/close_plot.html')

    else:
        return render_template('/wrong_ticker_name.html')



if __name__ == '__main__':
  app.run(port=33507)
