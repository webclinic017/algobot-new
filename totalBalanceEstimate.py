import pandas as pd
import sqlite3


conn = sqlite3.connect("tradesv3.dryrun.sqlite")
df = pd.read_sql_query("SELECT * FROM trades WHERE strategy = 'adx_opt_live' AND is_open = 0", conn)
total = df['close_profit'].sum()
print ((total) + (0.18018761))

conn.close()

