import requests
import json
import sqlite3

# this script gets a list of records
# that incldue some keywords, and updates
# a working copy of the database with that

con = sqlite3.connect('photoDB_working.db')
cur = con.cursor()

keywords = ['hall',
        'building',
        'lab',
        'dorm',
        'center',
        'stadium',
        'field',
        'arena',
        'bridge',
        'street',
        'ave',
        'mall',
        'auditorium',
        'campus',
        'view',
        'aerial',
        'river',
        'hospital',
        'plaza',
        'park',
        'train',
        'class'
        ]

base_url = 'https://umedia.lib.umn.edu/search.json?facets[collection_name_s][]=University+of+Minnesota+Archives+Photograph+Collection&rows=20000&q=' 

records = []

for keyword in keywords:

    url = base_url + keyword
    r = requests.get(url)
    data = json.loads(r.text)
    new_records = []

    for i in range(0,len(data)):
        if 'Hall,' not in data[i]['title']:
            new_records.append(data[i]['id'].split(':')[1])

    records = list(set(records + new_records))

for id_ in records:
    coll = 'p16022coll175'
    full_id = coll + '_' + id_

    cur.execute('''INSERT OR IGNORE INTO photos (id, collection, record)
        VALUES (?, ?, ?)''', (full_id, coll, id_)) 

con.commit()
con.close()
