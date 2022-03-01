import requests
import datetime
import json
import time
import schedule
from twilio.rest import Client

def grab_and_send():
    URL = 'https://newsapi.org/v2/top-headlines?sources=bcc-news,associated-press,reuters,the-wall-street-journal&apiKey=8a39aada2dd443caaabf84c4fae03cc8'
    account_sid = 'AC745b3d471c3796f0653026c1bc26ba7d'
    auth_token = 'b715d4a19b17c714358e51f80e70842a'
    client = Client(account_sid, auth_token)

    #Articles sourced through newsapi.org
    response = requests.get(URL)

    id_one = response.json().get("articles")[0].get("source").get("name")
    id_two = response.json().get("articles")[1].get("source").get("name")
    id_three = response.json().get("articles")[2].get("source").get("name")
    id_four = response.json().get("articles")[3].get("source").get("name")
    id_five = response.json().get("articles")[4].get("source").get("name")

    title_one = response.json().get("articles")[0].get("title")
    title_two = response.json().get("articles")[1].get("title")
    title_three = response.json().get("articles")[2].get("title")
    title_four = response.json().get("articles")[3].get("title")
    title_five = response.json().get("articles")[4].get("title")

    url_one = response.json().get("articles")[0].get("url")
    url_two = response.json().get("articles")[1].get("url")
    url_three = response.json().get("articles")[2].get("url")
    url_four = response.json().get("articles")[3].get("url")
    url_five = response.json().get("articles")[4].get("url")

    month_name = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}

    current_time = datetime.datetime.now()

    year = current_time.year
    month_num = current_time.month
    day = current_time.day
    month = month_name.get(month_num)

    #Links shortened with rebrandly.com

    linkRequest1 = {
        "destination": f"{url_one}", 
        "domain": { "fullName": "news.pkmeiner.com" },
        "slashtag": "article-one"
    }

    linkRequest2 = {
        "destination": f"{url_two}", 
        "domain": { "fullName": "news.pkmeiner.com" },
        "slashtag": "article-two"
    }

    linkRequest3 = {
        "destination": f"{url_three}", 
        "domain": { "fullName": "news.pkmeiner.com" },
        "slashtag": "article-three"
    }

    linkRequest4 = {
        "destination": f"{url_four}", 
        "domain": { "fullName": "news.pkmeiner.com" },
        "slashtag": "article-four"
    }

    linkRequest5 = {
        "destination": f"{url_five}",
        "domain": { "fullName": "news.pkmeiner.com" },
        "slashtag": "article-five"
    }

    requestHeaders = {
    "Content-type": "application/json",
    "apikey": "a654e5313c8d4d89980a508fb67979b5",
    "workspace": "9fc8b4f6b1224ac59dbdaed9d1d9f2ce"
    }

    try:
        r1 = requests.post("https://api.rebrandly.com/v1/links", 
            data = json.dumps(linkRequest1),
            headers=requestHeaders)

        r2 = requests.post("https://api.rebrandly.com/v1/links", 
            data = json.dumps(linkRequest2),
            headers=requestHeaders)

        r3 = requests.post("https://api.rebrandly.com/v1/links", 
            data = json.dumps(linkRequest3),
            headers=requestHeaders)

        r4 = requests.post("https://api.rebrandly.com/v1/links", 
            data = json.dumps(linkRequest4),
            headers=requestHeaders)

        r5 = requests.post("https://api.rebrandly.com/v1/links", 
            data = json.dumps(linkRequest5),
            headers=requestHeaders)

        link1 = r1.json()
        link2 = r2.json()
        link3 = r3.json()
        link4 = r4.json()
        link5 = r5.json()
        short_url_1 = f'https://{link1["shortUrl"]}'
        short_url_2 = f'https://{link2["shortUrl"]}'
        short_url_3 = f'https://{link3["shortUrl"]}'
        short_url_4 = f'https://{link4["shortUrl"]}'
        short_url_5 = f'https://{link5["shortUrl"]}'

    except:
        linkRequest1 = {
            "destination": f"{url_one}", 
            "domain": { "fullName": "news.pkmeiner.com" }
        }

        linkRequest2 = {
            "destination": f"{url_two}", 
            "domain": { "fullName": "news.pkmeiner.com" }
        }

        linkRequest3 = {
            "destination": f"{url_three}", 
            "domain": { "fullName": "news.pkmeiner.com" }
        }

        linkRequest4 = {
            "destination": f"{url_four}", 
            "domain": { "fullName": "news.pkmeiner.com" }
        }

        linkRequest5 = {
            "destination": f"{url_five}",
            "domain": { "fullName": "news.pkmeiner.com" }
        }

        r1 = requests.post("https://api.rebrandly.com/v1/links", 
            data = json.dumps(linkRequest1),
            headers=requestHeaders)

        r2 = requests.post("https://api.rebrandly.com/v1/links", 
            data = json.dumps(linkRequest2),
            headers=requestHeaders)

        r3 = requests.post("https://api.rebrandly.com/v1/links", 
            data = json.dumps(linkRequest3),
            headers=requestHeaders)

        r4 = requests.post("https://api.rebrandly.com/v1/links", 
            data = json.dumps(linkRequest4),
            headers=requestHeaders)

        r5 = requests.post("https://api.rebrandly.com/v1/links", 
            data = json.dumps(linkRequest5),
            headers=requestHeaders)

        link1 = r1.json()
        link2 = r2.json()
        link3 = r3.json()
        link4 = r4.json()
        link5 = r5.json()
        short_url_1 = f'https://{link1["shortUrl"]}'
        short_url_2 = f'https://{link2["shortUrl"]}'
        short_url_3 = f'https://{link3["shortUrl"]}'
        short_url_4 = f'https://{link4["shortUrl"]}'
        short_url_5 = f'https://{link5["shortUrl"]}'

    message = client.messages \
                    .create(
                        body=f"Current Top Articles For: {month} {day}, {year} \n\n\n{id_one} - {title_one}\n{short_url_1}\n\n{id_two} - {title_two}\n{short_url_2}\n\n{id_three} - {title_three}\n{short_url_3}\n\n{id_four} - {title_four}\n{short_url_4}\n\n{id_five} - {title_five}\n{short_url_5}",
                        from_='+19108074989',
                        to='+18179751776'
                    )

    # message2 = client.messages \
    #                 .create(
    #                     body=f"Current Top Articles For: {month} {day}, {year} \n\n\n{id_one} - {title_one}\n{short_url_1}\n\n{id_two} - {title_two}\n{short_url_2}\n\n{id_three} - {title_three}\n{short_url_3}\n\n{id_four} - {title_four}\n{short_url_4}\n\n{id_five} - {title_five}\n{short_url_5}",
    #                     from_='+19108074989',
    #                     to='+18173082476'
    #                 )

    print(message.sid)

    time.sleep(82800)

    requests.delete(f'https://api.rebrandly.com/v1/links/{link1["id"]}', 
    headers=requestHeaders)
    requests.delete(f'https://api.rebrandly.com/v1/links/{link2["id"]}', 
    headers=requestHeaders)
    requests.delete(f'https://api.rebrandly.com/v1/links/{link3["id"]}', 
    headers=requestHeaders)
    requests.delete(f'https://api.rebrandly.com/v1/links/{link4["id"]}', 
    headers=requestHeaders)
    requests.delete(f'https://api.rebrandly.com/v1/links/{link5["id"]}', 
    headers=requestHeaders)

schedule.every().day.at("11:00").do(grab_and_send)

while True:
    schedule.run_pending()
    time.sleep(1)
