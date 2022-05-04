import requests
import json


response = requests.get('http://api.stackexchange.com/questions?order=desc&sort=activity&site=stackoverflow')

# To access individual stackoverflow statements that have NO ANSWERS
for data in response.json()['items']:
    if data['answer_count'] == 0:
        print(data['title'])
        print(data['link'])
    else:
        print('skipped')
    print()