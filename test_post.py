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
#m = get_metadata('https://digitalcollections.hclib.org/digital/collection/MplsPhotos/id/', '54680')

'''
r = '1'
m = get_metadata('https://collection.mndigital.org//catalog/msn:' + r + '.json', 'images/metadata.txt')
print(m)
'''

'''
for i in range(1,100):
    r = str(randint(1, 2700))
    print(r)
    m = get_metadata('https://collection.mndigital.org//catalog/msn:' + r + '.json', 'images/metadata.txt')
    #print(m)
'''
create_send_post('msn', '2618')
