import datetime
import json
import requests

URL = 'https://newsapi.org/v2/top-headlines?sources=bcc-news,associated-press,reuters,the-wall-street-journal&apiKey=8a39aada2dd443caaabf84c4fae03cc8'

response = requests.get(URL)

requestHeaders = {
    "Content-type": "application/json",
    "apikey": "a654e5313c8d4d89980a508fb67979b5",
    "workspace": "9fc8b4f6b1224ac59dbdaed9d1d9f2ce"
}


def get_request(art_num):
    r = requests.get(f"https://api.rebrandly.com/v1/links?domain.fullName=news.pkmeiner.com&slashtag=article-{art_num}", 
        headers=requestHeaders)

    return r.json()

print(get_request('one')[0]['id'])