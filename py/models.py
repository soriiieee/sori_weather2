from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime


Base = declarative_base()

#参考の記事
# https://qiita.com/mink0212/items/d7f31f6e2903c5f0b837

class Now(Base):
  __tablename__ = "now_weather"
  
  id = Column(Integer, primary_key = True)
  name = Column(String)
  weather = Column(Text)
  date = Column(DateTime, default= datetime.now())
  
  def __init__(self, name, weather, date):
    self.name = name
    self.weather = weather
    self.date = date

  def __str__(self):
    return 'id:{}, weather:{}, age:{}, birthday:{}'.format(self.id, self.name, self.weahter["weather"][0]["main"], self.date)

def connect():
  # engine = create_engine("postgresql///?User=sori&Password=admin&Database=soriweather&Server=127.0.0.1&Port=5432")
  engine = create_engine('postgresql://scott:tiger@localhost/mydatabase')
  SessionClass = sessionmaker(bind=engine)
  session = SessionClass()
  
  for i in range(20):
    
    weather = "{'coord': {'lon': 139.7104, 'lat': 35.7186}, 'weather': [{'id': 503, 'main': 'Rain', 'description': 'very heavy rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 291.5, 'feels_like': 288.27, 'temp_min': 290.93, 'temp_max': 292.59, 'pressure': 1003, 'humidity': 94}, 'visibility': 6000, 'wind': {'speed': 8.23, 'deg': 180, 'gust': 13.38}, 'rain': {'1h': 17.61}, 'clouds': {'all': 75}, 'dt': 1616305298, 'sys': {'type': 1, 'id': 8077, 'country': 'JP', 'sunrise': 1616273030, 'sunset': 1616316777}, 'timezone': 32400, 'id': 1850144, 'name': 'Tokyo', 'cod': 200}"
    now = Now(name="tokyo", weather=weather)
    session.add(user_a)
  session.commit()

if __name__ ==  "__main__":
  connect()