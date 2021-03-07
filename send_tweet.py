import subprocess
import json
from random import randint
import tweepy
import datetime

def get_metadata(url, out_file):
      
    cmd = 'wget ' + url + ' --output-file=/dev/null -O ' + out_file
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()

    t = ''
    with open('images/metadata.txt') as f:
        for line in f:
            if 'JSON' in line:
                t = line[line.find('JSON') + 12: len(line)-4]
    if t == '':
        return
   
    # clean data
    t = t.replace('\\\\\\"',"'")
    t = t.replace('\\','')
    t = t.strip('\n')
    t = t.rstrip('"')
    t = t.lstrip('"')

    data = json.loads(t)

    metadata = {}
    try:
        for i in range(0, len(data['item']['item']['fields'])):
            entry = data['item']['item']['fields'][i]

            metadata.update({entry['key']:entry['value']})
    except:
        print('failure to get metadata')
        print(data['item']['item'])

    return metadata

def get_photo(url, out_image):

    cmd = 'wget ' + url + ' --output-file=/dev/null -O ' + out_image

    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()

    # check if photo doesn't exist from source and return 1 if it doesn't
    ls = subprocess.check_output('ls -lt ' + out_image, shell=True).decode('utf-8')

    # return false if photo not created for some reason
    try:
        size = ls.split(' ')[4]
    except:
        return False

    if size == '0':
        return False
    else:
        return True

# return true if bad word in title of description string
def bad_word_in_post(title, descr, input_file):

    bad_word_list = []
    with open(input_file) as f:
        for line in f:
            bad_word = line.strip('\n')
            bad_word_list.append(bad_word) 

    for word in bad_word_list:
        if word in title.lower() or word in descr.lower():
            return True
    return False

def get_api_keys(input_file):
    keys = {}
    with open(input_file) as f:
        for line in f:
            l = line.strip('\n')
            l = l.split(',')
            keys.update({l[0]:l[1]})

    return keys

def create_send_post(collection, photo_id):

    # connect to twitter
    keys = get_api_keys('api_keys.txt')
    auth = tweepy.OAuthHandler(keys['api_key'], keys['api_key_secret'])
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])
    api = tweepy.API(auth)

    base_url = 'https://digitalcollections.hclib.org/'
    full_url = base_url + 'digital/download/collection/' + collection + '/id/' + str(photo_id) + '/size/large'
    metadata_url = base_url + 'digital/collection/' + collection + '/id/' + str(photo_id)

    out_image = 'images/' + collection + photo_id + '.jpg'

    # try until photo is saved and metadata is retrieved
    photo_created = False
    len_metadata = 1
    while photo_created == False or len_metadata < 2:
        photo_created = get_photo(full_url, out_image)
        metadata = get_metadata(metadata_url, 'images/metadata.txt')
        len_metadata = len(metadata)

        '''
        print(metadata)
        print(len_metadata)
        print(base_url)
        print(metadata_url)
        '''

        if photo_created == True and len_metadata > 1:
            
            metadata_keys = list(metadata.keys())

            title = metadata['title']

            # get date of tweet, if exists
            if 'year' in metadata_keys:
                date = metadata['year']
            elif 'decade' in metadata_keys:
                date = metadata['decade']
            else:
                date = 'unknown'

            # get attribution 
            if 'permis' in metadata_keys:
                # assuming normal format
                try:
                    source = metadata['permis'].split(':')[1]
                    source = source.strip(' ').strip('"').strip("'")

                # if the format isn't as expected:
                except:
                    source = 'Hennepin County Library'
            else:
                source = 'Hennepin County Library'
    
            # make main tweet
            tweet1 = title
            tweet1 += '\nDate: ' + date
            if 'addres' in metadata_keys:
                tweet1 += '\nAddress: ' + metadata['addres'] 
                if 'SE' in metadata['addres'].upper().split(' '):
                    tweet1 += ' (#SEmpls)'
            tweet1 += '\nSource: ' + source
            print(tweet1)

            if 'descri' in metadata_keys:
                description = metadata['descri']
            else:
                description = ''

            # check for offensive content
            dont_post = bad_word_in_post(title, description, 'bad_words.txt')
            if dont_post == False:
                print('sending tweet')
                status = api.update_with_media(out_image, tweet1)

        else:
            print(full_url + ' failed')

if __name__ == '__main__':

    time = datetime.datetime.now()

    if time.hour > 8 and time.hour < 22 and time.minute % 5 == 0:

        collections = ['CPED', 'MplsPhotos']
        max_idx = [21250, 60000]

        # randomly choose collection and photo
        coll = randint(0,1)
        photo_idx = randint(1,max_idx[coll])

        create_send_post(collections[coll], str(photo_idx)) 
'''

# historical research inc (823 records)
https://digitalcollections.hclib.org/digital/download/collection/HRInc/id/55/size/large

# CPED collection (21250 records)
https://digitalcollections.hclib.org/digital/download/collection/CPED/id/9219/size/large
https://digitalcollections.hclib.org/digital/collection/CPED/id/21200

# urban renewal:
https://digitalcollections.hclib.org/digital/collection/FloydKelley/id/210 (210)

# hennepin history museum collection
https://digitalcollections.hclib.org/digital/collection/p17208coll13/id/14462/rec/1

# african american collection
# shouldn't use because need permission of copywriter
https://digitalcollections.hclib.org/digital/collection/p17208coll1/id/0/rec/1 (820)


# Mpls Photo collection (60000 records)
https://digitalcollections.hclib.org/digital/collection/MplsPhotos/id/60000 
'''

