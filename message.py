import requests
import datetime
import json
import time
import schedule
from twilio.rest import Client

def get_time():
    month_name = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}

    current_time = datetime.datetime.now()

    year = current_time.year
    month_num = current_time.month
    day = current_time.day
    month = month_name.get(month_num)

    return(f"{month} {day}, {year}")

def get_weather():
    URL = 'https://api.weatherapi.com/v1/forecast.json?key=58860c9ca7bf4e2b8b613232222402&q=Grand Prairie&days=1&aqi=no&alerts=no'

    response = requests.get(URL)

    max_temp = round(response.json().get("forecast").get("forecastday")[0].get("day").get("maxtemp_f"))
    min_temp = round(response.json().get("forecast").get("forecastday")[0].get("day").get("mintemp_f"))
    wind = response.json().get("forecast").get("forecastday")[0].get("day").get("maxwind_mph")
    text = response.json().get("forecast").get("forecastday")[0].get("day").get("condition").get("text")

    rain = round(response.json().get("forecast").get("forecastday")[0].get("day").get("daily_chance_of_rain"))
    snow = round(response.json().get("forecast").get("forecastday")[0].get("day").get("daily_chance_of_snow"))

    if rain > 1 and snow < 1:
        return(f"WEATHER\n\nCondition - {text}\nHigh Temp. - {max_temp}\nLow Temp. - {min_temp}\nWind - {wind} mph\nRain - {rain}%")
    
    elif snow > 1 and rain < 1:
        return(f"WEATHER\n\nCondition - {text}\nHigh Temp. - {max_temp}\nLow Temp. - {min_temp}\nWind - {wind} mph\nSnow - {snow}%")

    elif rain > 1 and snow > 1:
        return(f"WEATHER\n\nCondition - {text}\nHigh Temp. - {max_temp}\nLow Temp. - {min_temp}\nWind - {wind} mph\nRain - {rain}%\nSnow - {snow}%")
    
    else:
        return(f"WEATHER\n\nCondition - {text}\nHigh Temp. - {max_temp}\nLow Temp. - {min_temp}\nWind - {wind} mph")

URL = 'https://newsapi.org/v2/top-headlines?sources=bcc-news,associated-press,reuters,the-wall-street-journal&apiKey=8a39aada2dd443caaabf84c4fae03cc8'

response = requests.get(URL)

requestHeaders = {
    "Content-type": "application/json",
    "apikey": "a654e5313c8d4d89980a508fb67979b5",
    "workspace": "9fc8b4f6b1224ac59dbdaed9d1d9f2ce"
}

def get_url(url):
    url_one = response.json().get("articles")[0].get("url")
    url_two = response.json().get("articles")[1].get("url")
    url_three = response.json().get("articles")[2].get("url")
    url_four = response.json().get("articles")[3].get("url")
    url_five = response.json().get("articles")[4].get("url")
    if url == "url_one":
        return(url_one)
    elif url == "url_two":
        return(url_two)
    elif url == "url_three":
        return(url_three)
    elif url == "url_four":
        return(url_four)
    elif url == "url_five":
        return(url_five)

def request_link(url, art_num):
    return{
        "destination": f"{get_url(f'{url}')}", 
        "domain": { "fullName": "news.pkmeiner.com" },
        "slashtag": f"article-{art_num}"
    }

def post_request(url, art_num):
    r = requests.post("https://api.rebrandly.com/v1/links", 
        data = json.dumps(request_link(f'{url}', f'{art_num}')),
        headers=requestHeaders)

    return(r.json())

def news():
    try:
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

        short_url_1 = f"https://{post_request('url_one', 'one')['shortUrl']}"
        short_url_2 = f"https://{post_request('url_two', 'two')['shortUrl']}"
        short_url_3 = f"https://{post_request('url_three', 'three')['shortUrl']}"
        short_url_4 = f"https://{post_request('url_four', 'four')['shortUrl']}"
        short_url_5 = f"https://{post_request('url_five', 'five')['shortUrl']}"

        return(f"{id_one} - {title_one}\n{short_url_1}\n\n{id_two} - {title_two}\n{short_url_2}\n\n{id_three} - {title_three}\n{short_url_3}\n\n{id_four} - {title_four}\n{short_url_4}\n\n{id_five} - {title_five}\n{short_url_5}")
    except:
        del_links()

def get_request(art_num):
    r = requests.get(f"https://api.rebrandly.com/v1/links?domain.fullName=news.pkmeiner.com&slashtag=article-{art_num}", 
        headers=requestHeaders)

    return r.json()

def del_links():
    requests.delete(f"https://api.rebrandly.com/v1/links/{get_request('one')[0]['id']}", 
    headers=requestHeaders)
    requests.delete(f"https://api.rebrandly.com/v1/links/{get_request('two')[0]['id']}", 
    headers=requestHeaders)
    requests.delete(f"https://api.rebrandly.com/v1/links/{get_request('three')[0]['id']}", 
    headers=requestHeaders)
    requests.delete(f"https://api.rebrandly.com/v1/links/{get_request('four')[0]['id']}",  
    headers=requestHeaders)
    requests.delete(f"https://api.rebrandly.com/v1/links/{get_request('five')[0]['id']}", 
    headers=requestHeaders)


def grab_and_send():
    account_sid = 'AC745b3d471c3796f0653026c1bc26ba7d'
    auth_token = 'b715d4a19b17c714358e51f80e70842a'
    client = Client(account_sid, auth_token)

    print(get_time())
    print(news())
    print(get_weather())


    # message = client.messages \
    #                 .create(
    #                     body=f"Current Top Articles For: {get_time()}\n\n\n{news()}\n\n\n{get_weather()}",
    #                     from_='+19108074989',
    #                     to='+18179751776'
    #                 )
    # print(message.sid)

    # message2 = client.messages \
    #                 .create(
    #                     body=f"Current Top Articles For: {get_time()} \n\n\n{news()}\n\n\n{get_weather()}",
    #                     from_='+19108074989',
    #                     to='+18173082476'
    #                 )
    # print(message2.sid)


    time.sleep(5)
    del_links()

schedule.every().day.at("23:13").do(grab_and_send)

while True:
    schedule.run_pending()
    time.sleep(1)
