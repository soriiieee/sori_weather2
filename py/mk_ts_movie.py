# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# basic-module
if 1:
  import os, sys, gc
  import glob
  # import datetime as
  from datetime import datetime, timedelta
  import time
  import itertools
  import importlib
  import pickle
  import warnings
  import tqdm
  warnings.simplefilter("ignore")

  #描画系
  import matplotlib
  import matplotlib.ticker as mticker
  from mpl_toolkits.axes_grid1 import make_axes_locatable
  # matplotlib.use('Qt5Agg')
  import matplotlib.pyplot as plt
  import matplotlib.cm as cm

  #png読み込み
  from PIL import Image
  from io import BytesIO
  import plotly
  import plotly.graph_objects as go

  import numpy as np
  import pandas as pd
  import subprocess
  try:
    #mapping tool (~GMT)
    import cartopy.crs as ccrs
    import cartopy.feature as cfea
    import cartopy.io.shapereader as shapereader
    from cartopy.feature import ShapelyFeature
    # initial setting...
    color_polygon = "k"
    lakes_ = cfea.NaturalEarthFeature('physical', 'lakes', '10m', edgecolor=color_polygon, facecolor="none", linewidth=0.5)
    states_ = cfea.NaturalEarthFeature('cultural', 'admin_1_states_provinces_lines', '10m', edgecolor=color_polygon, facecolor='none', linewidth=0.2)
  except:
    print("cartoy not install...")
  
  import cv2

  # "/home/ysorimachi/.conda/envs/sori_conda/lib/python3.7/site-packages/cv2.cpython-37m-x86_64-linux-gnu.so"

#画像処理汎用モジュール

"""
静止画からmp4動画を作成する
参考：https://yusei-roadstar.hatenablog.com/entry/2019/11/29/174448

"""
def conv_img2movie(cate,movie_path,frame_rate):
  png_dir=f"/home/ysorimachi/work/sori_py2/sori_weather/dat/{cate}"

  _img = sorted(glob.glob(f"{png_dir}/*.jpg"))
  img_path = _img[0]
  img = cv2.imread(img_path)
  height,width = img.shape[0],img.shape[1]

  size=(int(width), int(height))
  # print(height,width)
  # print(type(height))
  # sys.exit()
  
  fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
  video = cv2.VideoWriter(movie_path,fourcc,frame_rate,(width,height))
  print("動画作成開始")
  # sys.exit()
  for i, img_path in enumerate(_img):
    img = cv2.imread(img_path)
    img = cv2.resize(img,(width,height))
    video.write(img)
    # print("end",i)
  
  video.release()
  print("動画変換完了")
  print("動画ファイルのパスは下記になります")
  print(movie_path)
  return

if __name__ =="__main__":
  # setting -----------------------------------
  cate = "rain" #fct
  frame_rate=4 #一秒で表示する画像の枚数
  #setting -----------------------------------
  # /home/ysorimachi/work/sori_py2/sori_weather/bin
  out_d = "/home/ysorimachi/work/sori_py2/sori_weather/out/movie"
  #start function...
   #[lat_min ,lon_min,lat_max,lon_max] (google map 等から)
  movie_path = f"{out_d}/{cate}.mp4"
  frame_rate=4

  conv_img2movie(cate,movie_path,frame_rate)