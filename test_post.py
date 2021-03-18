from send_tweet import *
from random import *

'''
for i in range (0, 100):

    r = str(randint(1,20000))
    url = 'https://digitalcollections.hclib.org/digital/collection/CPED/id/' + r
    m = get_metadata(url, 'images/metadata.txt')
    if 'descri' in list(m.keys()):
        print(m['id'], len(m['descri']), m['descri'])
url = 'https://digitalcollections.hclib.org/digital/collection/CPED/id/' + '18289'
m = get_metadata(url, 'images/metadata.txt')

d = description_parts(m['descri'])
print(d)
'''
create_send_post('MplsPhotos', '34077')
