from send_tweet import *
from random import randint

db = photoDB('photoDB.db')
r = db.get_random_row('test')
print(r)

db.con.close()
