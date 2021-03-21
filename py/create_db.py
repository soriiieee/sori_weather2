# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

import sqlite3

db_name = "../weather.db"
conn = sqlite3.connect(db_name)


#必須コマンド
conn.close()