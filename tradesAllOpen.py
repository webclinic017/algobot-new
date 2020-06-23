import pandas as pd
import sqlite3
import datetime

conn = sqlite3.connect("tradesv3.dryrun.sqlite")
df = pd.read_sql_query("SELECT * FROM trades WHERE strategy = 'adx_opt_live' AND is_open = 1 ", conn)
df1 = df[['id', 'pair', 'is_open', 'open_rate', 'close_rate', 'close_profit', 'stake_amount', 'amount', 'open_date', 'close_date', 'sell_reason', 'strategy']]
print(df1)

conn.close()

