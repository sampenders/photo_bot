import sqlite3
import csv
from random import *

class photoDB:
    def __init__(self, db_name):
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()

    def update_database(self, data):
        self.cur.execute('''UPDATE photos
                SET posted_date = ? 
                WHERE
                    id = ?
                '''
                , data
                )
        self.con.commit() 

    def get_random_row(self, collection):
        d = self.cur.execute('''
        SELECT record FROM photos 
        WHERE collection=? AND 
        posted_date IS NULL AND
        dont_post IS NOT 1 AND
        invalid_record IS NOT 1
        ''',
        [collection])

        records = d.fetchall()
        return records[randint(0,len(records)-1)][0]

    def update_row_status(self, date, id_, dont_post):
        self.cur.execute('''
        UPDATE photos 
        SET posted_date=?, dont_post=?
        WHERE id=?
        ''',
        [date, dont_post, id_])
        
        self.con.commit()

#con = sqlite3.connect('photoDB.db')
#cur = con.cursor()

#collections = ['CPED', 'MplsPhotos', 'FloydKelley', 'MPRB', 'p17208coll18', 'p17208coll1' ]
#max_idx = [21250, 60000, 212, 251, 1100, 820]
collections = ['msn' ]
max_idx = [2776]

# generate all rows based on collection, max_idx number
def populate_all(cur, con):
    for i in range (0,len(collections)):
        for j in range (0, max_idx[i]):
            data = (collections[i] + '_' + str(j), collections[i], j)
            try:
                cur.execute("INSERT INTO photos (id, collection, record) VALUES (?,?,?)", data)
            except:
                print(collections[i], j)

            if j % 1000 == 0:
                print(collections[i], j)
    con.commit()


'''
with open('post_log.txt', newline='\n') as f:
    reader = csv.reader(f)
    for row in reader:
        data = [row[0], row[1] + '_' + str(row[2])]
        print(row)

#populate_all(cur, con)
#update_database(cur, con)

a = cur.execute('SELECT * FROM photos WHERE posted_date IS NOT NULL')


for row in cur.execute("SELECT * FROM photos WHERE id='p17208coll1_305'"):
    print(row)
    print(row[0])

'''

db = photoDB('photoDB.db')
#populate_all(db.cur, db.con)

'''
with open('post_log.txt', newline='\n') as f:
    reader = csv.reader(f)
    for row in reader:
        data = [row[0], row[1] + '_' + str(row[2])]
        db.update_database(data)
        print(row)
'''
'''
print(db.get_random_row('CPED'))
db.update_row_status('01/01/21 00:00:55', 'CPED_2', 20)
#db.update_database(['01/01/01 00:00:00','CPED_2'])
'''
db.con.commit()
db.con.close()
'''
# print(get_random_row(cur, con, 'CPED'))

#update_row_status(cur, con, '01/01/21 00:00:00', 'CPED_1', None)

#con.commit()
#con.close()
'''
