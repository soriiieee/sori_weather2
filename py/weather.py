# -*- coding: utf-8 -*-
# when   : 2020.0x.xx
# who : [sori-machi]
# what : [ ]
#---------------------------------------------------------------------------
# basic-module
import matplotlib.pyplot as plt
import sys,os,re,glob
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.simplefilter('ignore')
from tqdm import tqdm
import seaborn as sns
#---------------------------------------------------
# sori -module
sys.path.append('/home/ysorimachi/tool')
from getErrorValues import me,rmse,mae,r2 #(x,y)
from convSokuhouData import conv_sfc #(df, ave=minutes,hour)
#amedas relate 2020.02,04 making...
from tool_AMeDaS import code2name, name2code
from tool_110570 import get_110570,open_110570
from tool_100571 import get_100571,open_100571
#(code,ini_j,out_d)/(code,path,csv_path)


from mapbox import map_lonlat
import plotly
#---------------------------------------------------
import subprocess
import json
import requests
open_weather_api = open("../env/owm.env").read()
BASEURL="https://api.openweathermap.org/data/2.5"


def remover():
  subprocess.run("rm -rf *.csv *.json", cwd ="../tmp" , shell=True)
  return

#api get moduele-------------------------------------------------
def now(reset=None):
  if reset:
    remover()
    
  lat,lon = 35.6827467747325, 139.76946318521107 #marunouti
  lat,lon = 35.7186, 139.71038 #Tokyo
  out_path = "../tmp/now.json"
  
  if not os.path.exists(out_path):
    print("NotFound [start] loading from open weather map...")
    url = f"{BASEURL}/weather?lat={lat}&lon={lon}&appid={open_weather_api}"
    res = requests.get(url)
    if res.status_code ==200:
      data = json.loads(res.text)
      with open(f"../tmp/now.json","w") as f:
        json.dump(data,f)
      now()
  else:
    print("Already getted..")
    with open(f"../tmp/now.json","r") as f:
      data = json.loads(f.read())
  return data

def get_all(name):
  lon,lat = get_lonlat(name)
  url = f"{BASEURL}/onecall?lat={lat}&lon={lon}&appid={api['open_weather']}"
  
  res = requests.get(url)
  if res.status_code ==200:
    data = json.loads(res.text)
    with open(f"../../out/{name}_allin.json","w") as f:
      json.dump(data,f)
  return
#--------------------------------------------------------------------

def unixt2time(unix,offset):
  init = datetime(1970,1,1,0,0,0)
  time = init + timedelta(seconds=int(unix)) + timedelta(seconds=int(offset))
  return time


def load_all(name):
  def info(data):
    lat,lon,timezone,timezone_offset = data["lat"],data["lon"],data["timezone"], data["timezone_offset"]
    return lat,lon,timezone,timezone_offset
  
  #weather info
  def get_current(data):
    now = data["current"]
    lat,lon,timezone,timezone_offset = info(data)
    
    for k,v in now.items():
      if k =="dt" or k=="sunrise" or k=="sunset":
        v = unixt2time(v,timezone_offset)
      if k =="temp" or k=="feels_like" or k=="dew_point":
        v = np.round(v -273.15, 2) 
      # print(k,v)
  #weather info
  def get_min_rain(data):
    fct = data["minutely"]
    lat,lon,timezone,timezone_offset = info(data)

    _i,_dt,_precip = [],[],[]
    for i,item in enumerate(fct):
      _i.append(i)
      _dt.append(unixt2time(item["dt"],timezone_offset))
      _precip.append(item["precipitation"])
    
    df = pd.DataFrame()
    df["time"] = _dt
    df[f"rain({name})"] = _precip
    df.to_csv("../../out/fct_min.csv", index=False)
  #weather info
  def get_hourly(data):
    fct = data["hourly"]
    lat,lon,timezone,timezone_offset = info(data)
    _df=[]
    for i,item in enumerate(fct):
      if 'rain' not in item.keys():
        item.update({"rain": 0})
      df = pd.DataFrame(item)
      _df.append(df)
    
    df = pd.concat(_df,axis=0)
    df["dt"] = df["dt"].apply(lambda x: unixt2time(x,timezone_offset))
    for c in ["temp","feels_like","dew_point"]:
      df[c] = df[c].apply(lambda x: np.round(x -273.15, 2))
    df.to_csv("../../out/fct_hour.csv", index=False)
  
  #weather info
  def get_daily(data):
    fct = data["daily"]
    lat,lon,timezone,timezone_offset = info(data)
    _df=[]
    
    for i,item in enumerate(fct):
      # for cate in ["temp","feels_like"]:
      #   item.update({"rain": 0})
      item["temp"] = [[item["temp"]["day"],item["temp"]["min"],item["temp"]["max"]]]
      item["feels_like"] = [[item["feels_like"]["day"],item["feels_like"]["morn"],item["feels_like"]["night"]]]
      if 'rain' not in item.keys():
        item.update({"rain": 0})
        
      df = pd.DataFrame(item)
      # print(df.head())
      # sys.exit()
      _df.append(df)
    
    df = pd.concat(_df,axis=0)
    for c in ["dt","sunrise","sunset"]:
      df[c] = df[c].apply(lambda x: unixt2time(x,timezone_offset))
    
    df.to_csv("../../out/fct_day.csv", index=False)
    
  
  
  with open(f"../../out/{name}_allin.json","r") as f:
    data = json.loads(f.read())
  #get info
  get_current(data)
  get_min_rain(data)
  get_hourly(data)
  get_daily(data)
  return
  



if __name__ =="__main__":
  data = now(reset=True)
  print(data)
  sys.exit()
  
  # get_now(name)
  if 1:
    # get_now(name)
    get_all(name)
  
  if 1:
    load_all(name)