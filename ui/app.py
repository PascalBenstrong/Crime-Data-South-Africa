'''
author: Pascal
'''
from dataclasses import dataclass
from flask import Flask, request, render_template
from multiprocessing import Process
from pandas.core.frame import DataFrame, Index
import webbrowser as wb
from os import environ
from time import sleep

app = Flask(__name__)
utils = {}
browserStarting = False

def startBrowser():
  '''
  Opens a browser window to http://localhost:5000
  return None
  '''
  sleep(0.5)
  wb.open("http://localhost:5000")

## dataclass to cache the csv data at app startup
@dataclass
class ApiData: 
  data: DataFrame
  summary: DataFrame
  headers: Index

#cache
data: ApiData = {}

def run(utils_funcs, **kwargs):
  """
  Takes in:
    utils_funcs: module

  sets up the required functions to retrieve the data
  returns None
  
  """

  # setup the 
  global utils, app, data
  utils = utils_funcs
  _data = utils.get_data()
  _summary = _data.head(5)
  _headers = _summary.columns

  data = ApiData(_data, _summary, _headers)
  # this is just used to make sure the app only opens 
  # browser one browser tab
  if not environ.get("WERKZEUG_RUN_MAIN") == "true":
    child_process = Process(target=startBrowser, args=())
    child_process.start()
  app.run(debug=True)

@app.route("/")
def index():

  return render_template("index.html", data=data, utils=utils)

@app.route("/province-and-period")
def get_data_for_province_and_period():
  # get request parameters
  province = request.args.get("province")
  period_start = int(request.args.get("period_start"))
  period_end = int(request.args.get("period_end"))
  period = str(period_start) + '-' + str(period_end)
  total = utils.get_data_for_period_and_province(period, province, data.data).sum().sum()
  return str(total)

@app.route("/total-for-station/<station>")
def get_total_data_for_station(station: str):
  total = utils.get_data_for_station(station, data.data).sum().sum()
  return str(total)

@app.route("/truck_hijacking")
def get_data_for_truck_hijacking():
  # filter by category
  frame: DataFrame = utils.filter_by_column("Category","truck hijacking",data.data)
  total = frame["2010-2011"].sum()
  
  return str(total)
  
