import sqlite3
import csv
from datetime import datetime
import boto3

filename = datetime.now().strftime("%d%m%Y-%H%M%S")
conn = sqlite3.connect("tradesv3.dryrun.sqlite")
cur = conn.cursor()
data = cur.execute("SELECT * FROM trades WHERE strategy = 'adx_opt_live' AND is_open = 0")

#write to csv
with open(filename + '.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames = ['id','exchange','pair','is_open','fee_open',
    'fee_close','open_rate','open_rate_requested','open_trade_price','close_rate',
    'close_rate_requested','close_profit','close_profit_abs','stake_amount','amount','open_date','close_date',
    'open_order_id','stop_loss','stop_loss_pct','initial_stop_loss','initial_stop_loss_pct','stoploss_order_id',
    'stoploss_last_update','max_rate','min_rate','sell_reason','strategy','ticker_interval','PRIMARY KEY','CHECK'], delimiter = ',')
    writer.writeheader()
    writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerows(data)

f.close()

#upload to s3
s3 = boto3.client('s3')
s3.upload_file(filename + '.csv', 'adx-results', filename + '.csv')

