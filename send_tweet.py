import subprocess
import json
from random import randint
import tweepy
from mastodon import Mastodon
import datetime
import sqlite3
import requests

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

        # if there are no records found
        if len(records) == 0:
            return -1
        else:
            return records[randint(0,len(records)-1)][0]

    def update_row_status(self, date, id_, dont_post):
        self.cur.execute('''
        UPDATE photos
        SET posted_date=?, dont_post=?
        WHERE id=?
        ''',
        [date, dont_post, id_])

        self.con.commit()

# break up description into valid length parts
def description_parts(desc):
    desc_parts = []

    desc = 'Description: ' + desc

    if len(desc) <= 280:
        desc_parts = [desc]

    else:
        l_idx = 0
        r_idx = 276
        finished = False
        while finished == False:
            # finish if we've reached the end of the string
            if r_idx >= len(desc)-1:
                finished = True
                desc_parts.append(desc[l_idx:])
            else:
                r_idx = desc[l_idx:r_idx].rfind(' ') + l_idx
                desc_parts.append(desc[l_idx:r_idx] + ' ...')

            l_idx=r_idx+1
            r_idx+=276

    return desc_parts

# randomly choose index of collection given weights
def choose_collection(weights):
    sum_w = 0
    for i in weights: sum_w+= i

    # find out which set r is in
    r = randint(1,sum_w)
    for i in range(0, len(weights)):
        sum_ = 0
        for j in range(0,i+1): sum_+=weights[j]
        if r <= sum_:
            return(i)

def get_metadata(url):
    
    # get json  
    t = json.loads(requests.get(url).text)

    # if this if from streetcar collection:
    if 'msn' in url:
        try:
            keys = list(t['response']['document'].keys())
            metadata = {}
        # if invalid record
        except:
            return {}
        
        # get title
        metadata.update({'title':t['response']['document']['title_ssi']})
        metadata.update({'permis':'Minnesota Streetcar Museum'})
        metadata.update({'id':t['response']['document']['id'].split(':')[1]})
        
        # get description
        if 'description_ts' in keys:
            metadata.update({'descri':t['response']['document']['description_ts']})
        #else:
        #    metadata.update({'descri':''})
            
        if 'dat_tesi' in keys:
            metadata.update({'year':t['response']['document']['dat_tesi']})
            
        if 'city_ssim' in keys:
            cities = t['response']['document']['city_ssim']
            if 'Minneapolis' in cities:
                metadata.update({'city':'Minneapolis'})
            else:
                metadata.update({'city':t['response']['document']['city_ssim'][0]})
            
        #m.update{'title':t['response']['document']['title_ssi']}
        
    # university of minnesota archives
    elif 'p16022coll175' in url:
        try:
            keys = list(t.keys())
            metadata = {}
        # if invalid record
        except:
            return {}
            
        metadata.update({'title':t['title']})
        metadata.update({'permis':t['contributing_organization_name']})
        metadata.update({'id':t['id'].split(':')[1]})
          
        # get description
        if 'description' in keys:
            metadata.update({'descri':t['description']})
            
        if 'date_created' in keys:
            metadata.update({'year':t['date_created'][0]})
            
        if 'city' in keys:
            cities = t['city']
            # initialize
            metadata.update({'city':t['city'][0]})
            for city in cities:
                # format typically like 'Minneapolis;  St Paul'
                if 'minneapolis' in city.lower():
                    metadata.update({'city':'Minneapolis'})

    # else if this is hclib photo
    else:
        try:
            metadata = t
            
            fields_to_remove = []
            for field in t:
                if metadata[field] == {}:
                    fields_to_remove.append(field)
            for field in fields_to_remove:
                metadata.pop(field)
                
            # manually add this field in as 'id' for compatibility purposes
            metadata.update({'id': metadata['dmrecord']})
                    
        except Exception as e:
            print('failure to get metadata')
            print(e)
            print(metadata)
            return {}

    return metadata

def get_photo(url, out_image):

    cmd = 'wget --user-agent="Mozilla" ' + url + ' --output-file=/dev/null -O ' + out_image

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
def bad_word_in_post(title, descr, subj, input_file):

    bad_word_list = []
    with open(input_file) as f:
        for line in f:
            bad_word = line.strip('\n')
            bad_word_list.append(bad_word) 

    for word in bad_word_list:
        if word in title.lower() or word in descr.lower() or word in subj.lower():
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

    # connect to mastodon
    mast_key = get_api_keys('api_keys_mastodon.txt')
    mastodon = Mastodon(
    access_token = mast_key['access_token_secret'],
    api_base_url = 'https://botsin.space/'
    )

    # images we'll be pulling
    if collection == 'msn':
        full_url = 'https://cdm16022.contentdm.oclc.org/digital/iiif/msn/' + str(photo_id) + '/full/full/0/default.jpg'
        metadata_url = 'https://collection.mndigital.org//catalog/msn:' + str(photo_id) + '.json'

        out_image = 'images/' + collection + photo_id + '.jpg'
    
    # umn archives    
    elif collection == 'p16022coll175':
        full_url = 'https://cdm16022.contentdm.oclc.org/digital/iiif/p16022coll175/' + str(photo_id) + '/full/full/0/default.jpg'
        metadata_url = 'https://umedia.lib.umn.edu/item/p16022coll175:' + str(photo_id) + '.json'

        out_image = 'images/' + collection + photo_id + '.jpg'  
                 
    # if hclib collection:
    else:
        base_url = 'https://digitalcollections.hclib.org/'
        full_url = base_url + 'digital/download/collection/' + collection + '/id/' + str(photo_id) + '/size/large'
        metadata_url = base_url + 'digital/bl/dmwebservices/index.php?q=dmGetItemInfo/' + collection + '/' + str(photo_id) + '/json'

        out_image = 'images/' + collection + photo_id + '.jpg'

    # try to create photo and get metadata
    photo_created = get_photo(full_url, out_image)
    metadata = get_metadata(metadata_url)
    len_metadata = len(metadata)

    # return false if photo or metadata weren't retrieved or 
    # index of metadata doesn't match intended value
    if photo_created == True and len_metadata > 1 and str(metadata['id']) == str(photo_id):
        
        metadata_keys = list(metadata.keys())
        title = metadata['title']

        # get date of tweet, if exists
        if 'year' in metadata_keys:
            date = metadata['year']
        elif 'decade' in metadata_keys:
            date = metadata['decade']
        else:
            date = 'Unknown'

        # get attribution
        perm_exists = False
        if 'permis' in metadata_keys:

            # assuming normal format for hclb
            if ':' in metadata['permis']:
                try:
                    source = metadata['permis'].split(':')[1]
                    source = source.strip(' ').strip('"').strip("'")
                    perm_exists = True

                # if the format isn't as expected:
                except:
                    perm_exists = False
                    source = ''
                    #source = 'Hennepin County Library'

            # different format for glanton
            if 'glanton' in metadata['permis'].lower():
                source = 'Hennepin County Library and the children of John Glanton'
                
            if 'Streetcar Museum' in metadata['permis']:
                source = metadata['permis']
                perm_exists = True
                
            if 'University Archives' in metadata['permis']:
                source = metadata['permis']
                perm_exists = True                
            
            # if the permissions say you need to contact them, don't post
            if 'viewed' in metadata['permis'] and 'specialcoll@hclib.org' in metadata['permis']:
                source = ''
                perm_exists = False

        # if there is no permissions field 
        else:
            perm_exists = True
            source = 'Hennepin County Library'

        # make main tweet
        tweet1 = title
        tweet1 += '\nDate: ' + date
        if 'addres' in metadata_keys:
            tweet1 += '\nAddress: ' + metadata['addres'] 
            if 'SE' in metadata['addres'].upper().split(' '):
                tweet1 += ' #SEmpls'
        tweet1 += '\nSource: ' + source
        print(tweet1)

        if 'descri' in metadata_keys:
            description = metadata['descri']
        else:
            description = ''

        if 'subjec' in metadata_keys:
            subject = metadata['subjec']
        else:
            subject = ''

        # check that the photo was taken in minneapolis
        # if there's no city field, assume it was in mpls
        in_mpls = False
        if 'city' in metadata_keys:
            city = metadata['city']
            cities = ['minneapolis','saint anthony and minneapolis', 'saint anthony', 'richfield', 'hopkins', 'saint louis park', 'st. louis park', 'robbinsdale', 'fort snelling', 'golden valley', 'columbia heights']
            if city.lower() in cities:
                in_mpls = True
            else:
                in_mpls = False

        # assume in minneapolis is minneapolis mentioned. this is
        # redundant for now
        elif 'minneapolis' in title.lower() or 'minneapolis' in description.lower() or 'minneapolis' in subject.lower():
            in_mpls = True

        # assume it's in minneapolis if no city provided
        else:
            in_mpls = True

        # check for offensive content
        # post if non-offensive and there are permissions
        dont_post = bad_word_in_post(title, description, subject, 'bad_words.txt')
        if dont_post == False and perm_exists == True and in_mpls == True:
            print('sending tweet')
            status = api.update_with_media(out_image, tweet1)

            print('sending toot')
            mast_media = mastodon.media_post(out_image)
            toot = mastodon.status_post(tweet1, media_ids=mast_media)
           
            # add description in a reply if available
            if description != '':
                descr_text = description_parts(description)
                prev_id = status.id
                prev_toot_id = toot.id
                for d in descr_text:
                    # tweet thread
                    reply = api.update_status(status=d, 
                                     in_reply_to_status_id=prev_id, 
                                     auto_populate_reply_metadata=True)
                    prev_id = reply.id

                    # mastodon thread
                    mast_reply = mastodon.status_post(status=d, in_reply_to_id=prev_toot_id)
                    prev_toot_id = mast_reply.id

            return True

        # if there's a filtered word in the post
        else:
            print('bad word: ' + str(dont_post))
            print('permission to post: ' + str(perm_exists))
            print('in mpls: ' + str(in_mpls))
            return False

    # failed if couldn't get photo, metadata, or metadata id doesn't match
    else:
        print(' failed')
        return False

# main loop for sending posts
# try to send until we successfully get an image
if __name__ == '__main__':

    time = datetime.datetime.now()

    # coll18 is really old photos, coll1 is glanton photos, coll 175 is university archives
    collections = ['CPED', 'MplsPhotos', 'FloydKelley', 'MPRB', 'p17208coll18', 'p17208coll1', 'msn', 'p17208coll15', 'p16022coll175']
    max_idx = [21250, 60000, 212, 251, 1100, 820, 2776, 1406, 21899]
    weights = [20, 13, 1, 1, 5, 3, 10, 5, 10]

    # open connection to photo database
    db = photoDB('photoDB.db')

    sum_weights = 0
    for i in weights: sum_weights+=i

    # try until a photo is found and posted
    tries = 0
    posted = False
    while posted == False and tries < 10:

        # randomly choose collection based on weights given
        coll = choose_collection(weights)

        # randomly choose photo in collection
        # if = -1, then there are no records left
        photo_idx = db.get_random_row(collections[coll])
        
        #photo_idx = randint(1,max_idx[coll]) 
        if int(photo_idx) != -1:
            posted = create_send_post(collections[coll], str(photo_idx))

            # update database with whether this was posted or not
            if posted == False:
                db.update_row_status(time.strftime('%d/%m/%y %H:%M:%S'), collections[coll] + '_' + str(photo_idx), 1)
            else:
                db.update_row_status(time.strftime('%d/%m/%y %H:%M:%S'), collections[coll] + '_' + str(photo_idx), 0)

                # write to log
                f = open('post_log.txt','a')
                f.write(time.strftime('%d/%m/%y %H:%M:%S') + ',' + collections[coll] + ',' + str(photo_idx) + '\n')
                f.close()

            tries += 1

    db.con.close()
