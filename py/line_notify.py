# -*- coding: utf-8 -*-
# when   : 2023.03.21
# author : sormachi yuichi
#---------------------------------------------------------------------------
# basic-library
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

import requests


#setting
URL = "https://notify-api.line.me/api/notify"
access_token = open("../env/line.env").read()
headers  = {'Authorization' : f'Bearer {access_token}'}

#main commands
def test():
  message = 'Test message ! \nNow is -> {}'.format(datetime.now())
  data = {'message': message}
  r = requests.post(URL, headers=headers, data =data)
  print(r.status_code)
  
def forecast():
  #main massege
  
  
  
  message = 'Test message ! \nNow is -> {}'.format(datetime.now())
  data = {'message': message}
  
  
  # r = requests.post(URL, headers=headers, data =data)
  print(r.status_code)
  

if __name__ == "__main__":
  forecast()