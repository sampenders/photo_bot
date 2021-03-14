
#d = "L to R: Barbara Hustad (age 3.5), visiting her aunt Lucille Coppersmith in Minneapolis, wandered out of the apartment at dawn and entered a neighbor's apartment in the same building. Her parents and aunt called the police when they discovered the child missing, starting an area search. The neighbor, Mrs. Popponen (not pictured), greeted the child who knocked on her door and waited until a reasonable hour to wake the landlord. Barbara was returned to her relieved parents after an hour-long police search in the fog."
d = '''A group of teenage boys used to call out to Chaunté Ford as she walked the halls of St. Louis Park Middle School in her police uniform.

"Here comes 12," they would mutter, a slang term for law enforcement. She would smile and try to approach them, but most times she was shunned, until one day the boys finally acknowledged her by name.

"I have had some kids who are like 'Nope. Cops are bad. I'm not going to associate myself with you,' " Ford said. "Sometimes that's a challenge. It's just about being consistent and showing them that you care and then eventually they come around."

Ford isn't a stranger to the slow process of building trust, but as a Black policewoman doing her job while a former officer is on trial in George Floyd's death, many of her challenges lately have been within herself.

"Once George was killed I was like, 'Am I part of the problem? Am I really fixing anything? Am I helping to make anything better?' " Ford said. "I questioned that and I didn't want to go to work that day. I was just like, this is too much."

Struggling to reconcile her profession and her cultural identity, she has both marched in peaceful protests and pushed for bias awareness at work.

"I am a Black woman, and I am a police officer," she said. "I do struggle with that."

Doubt and anxiety have plagued law enforcement departments in recent months. The Minneapolis Police Department had 200 fewer officers available to work at the beginning of this year than last, with unprecedented numbers leaving or filing disability claims amid the community outcry following Floyd's death. Many cited post-traumatic stress disorder.'''

def description_parts(description):

    description = 'Description: ' + description
    split_d = description.split(' ')
    d_parts = []
    
    prev_len = 0
    len_phrase = 0
    idx_last_phrase = 0
    for i in range(0, len(split_d)):
        prev_len = len_phrase
        len_phrase += len(split_d[i]) + 1

        # create first part of description
        if len_phrase > 277 and len(description) > 280:
            phrase = ''
            for j in range(idx_last_phrase, i-1):
                phrase += split_d[j] + ' '
            phrase += split[i-1] + '...'
            d_parts.append(phrase)

            # reinitialize to get rest
            len_phrase = 0
            idx_last_phrase = i

        elif i == len(split_d)-1:
            phrase = ''
            for j in range(idx_last_phrase, i):
                phrase += split_d[j] + ' '
            phrase += split_d[i]
            d_parts.append(phrase)

    return d_parts


desc = description_parts(d)
print(desc)
