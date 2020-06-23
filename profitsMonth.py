import pandas as pd
import sqlite3
import datetime

conn = sqlite3.connect("tradesv3.dryrun.sqlite")
df = pd.read_sql_query("SELECT * FROM trades WHERE close_date BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime') AND strategy = 'adx_opt_live' AND is_open = 0", conn)
total = df['close_profit_abs'].sum()
print (total)

conn.close()

