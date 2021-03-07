import json

with open('test.json') as f:
    for line in f:
        if 'JSON' in line:
            t = line[line.find('JSON') + 12: len(line)-4]

t = t.replace('\\\\\\"',"'")
t = t.replace('\\','')
t = t.strip('\n')
t = t.rstrip('"')
t = t.lstrip('"')

data = json.loads(t)

for i in range(0, len(data['item']['item']['fields'])):
    print(data['item']['item']['fields'][i]['key'], data['item']['item']['fields'][i]['value'])
