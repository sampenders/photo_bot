import sqlite3
import csv

con = sqlite3.connect('photoDB.db')
cur = con.cursor()

collections = ['CPED', 'MplsPhotos', 'FloydKelley', 'MPRB', 'p17208coll18', 'p17208coll1' ]
max_idx = [21250, 60000, 212, 251, 1100, 820]

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

def update_database(cur, con):
    with open('post_log.txt', newline='\n') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
            data = [row[0], row[1] + '_' + str(row[2])]

            con.execute('''UPDATE photos
                    SET posted_date = ? 
                    WHERE
                        id = ?
                    '''
                    , data
                    )
    con.commit() 


#populate_all(cur, con)
update_database(cur, con)
con.commit()
con.close()
