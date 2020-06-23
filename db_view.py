import sqlite3

def view():
    conn=sqlite3.connect("tradesv3.dryrun.sqlite")
    cur=conn.cursor()
    cur.execute("SELECT * FROM trades")
    rows=cur.fetchall()
    conn.close()
    return rows

print(view())