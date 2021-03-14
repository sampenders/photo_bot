from send_tweet import *
from random import *

'''
for i in range (0, 100):

    r = str(randint(1,20000))
    url = 'https://digitalcollections.hclib.org/digital/collection/CPED/id/' + r
    m = get_metadata(url, 'images/metadata.txt')
    print(m['permis'])
'''
r = '12345'
url = 'https://digitalcollections.hclib.org/digital/collection/CPED/id/' + r
m = get_metadata(url, 'images/metadata.txt')
#create_send_post('CPED', r)
