import sqlite3
import csv
from datetime import datetime
import pandas as pd

conn = sqlite3.connect("tradesv3.dryrun.sqlite")
cur = conn.cursor()
data = cur.execute("SELECT * FROM trades WHERE strategy = 'adx_opt_live' AND is_open = 0")
print(data)
conn.close()
