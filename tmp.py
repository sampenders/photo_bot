from send_tweet import *
import sqlite3

db = photoDB('photoDB.db')
collection = 'p17208coll15'

for i in range(0, 1407):
    db.cur.execute('''INSERT INTO photos (id, collection, record)
        VALUES (?, ?, ?)''', [collection+'_'+str(i), collection, i])

db.con.commit()
