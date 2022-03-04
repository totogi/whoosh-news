import requests
import datetime
import json
import time
import schedule
from twilio.rest import Client
from random import randint
import os
from dotenv import load_dotenv
load_dotenv('/.env')
news_api_key = os.getenv('NEWS_API_KEY')
weather_api_key = os.getenv('WEATHER_API_KEY')
rebrandly_api_key = os.getenv('REBRANDLY_API_KEY')
rebrandly_workspace = os.getenv('REBRANDLY_WORKSPACE')
twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
number_1 = os.getenv('NUMBER_1')
number_2 = os.getenv('NUMBER_2')
from_number = os.getenv('FROM_NUMBER')
time_to_send = "13:06"
time_to_del = "10:00"

def get_time():
    month_name = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}

    current_time = datetime.datetime.now()

    year = current_time.year
    month_num = current_time.month
    day = current_time.day
    month = month_name.get(month_num)

    return(f"{month} {day}, {year}")

def get_quote():
    with open('quotes.json', encoding='utf-8') as fp:
        data = json.load(fp)
        quotes = data["quotes"]
        random_index = randint(0, len(quotes)-1)
        return f"{quotes[random_index]['quote']} - {quotes[random_index]['author']}"

def get_weather():
    URL = f'https://api.weatherapi.com/v1/forecast.json?key={weather_api_key}&q=Grand Prairie&days=1&aqi=no&alerts=no'

    response = requests.get(URL)

    max_temp = round(response.json().get("forecast").get("forecastday")[0].get("day").get("maxtemp_f"))
    min_temp = round(response.json().get("forecast").get("forecastday")[0].get("day").get("mintemp_f"))
    wind_speed = response.json().get("forecast").get("forecastday")[0].get("day").get("maxwind_mph")
    wind_dir = response.json().get("current").get("wind_dir")
    text = response.json().get("forecast").get("forecastday")[0].get("day").get("condition").get("text")
    wind = f'{wind_speed} mph {wind_dir}'

    rain = round(response.json().get("forecast").get("forecastday")[0].get("day").get("daily_chance_of_rain"))
    snow = round(response.json().get("forecast").get("forecastday")[0].get("day").get("daily_chance_of_snow"))

    if rain > 1 and snow < 1:
        return(f"WEATHER\n\nCondition - {text}\nHigh Temp. - {max_temp}\nLow Temp. - {min_temp}\nWind - {wind}\nRain - {rain}%")
    
    elif snow > 1 and rain < 1:
        return(f"WEATHER\n\nCondition - {text}\nHigh Temp. - {max_temp}\nLow Temp. - {min_temp}\nWind - {wind}\nSnow - {snow}%")

    elif rain > 1 and snow > 1:
        return(f"WEATHER\n\nCondition - {text}\nHigh Temp. - {max_temp}\nLow Temp. - {min_temp}\nWind - {wind}\nRain - {rain}%\nSnow - {snow}%")
    
    else:
        return(f"WEATHER\n\nCondition - {text}\nHigh Temp. - {max_temp}\nLow Temp. - {min_temp}\nWind - {wind}")

URL = f'https://newsapi.org/v2/top-headlines?sources=bcc-news,associated-press,reuters&apiKey={news_api_key}'

response = requests.get(URL)

requestHeaders = {
    "Content-type": "application/json",
    "apikey": f"{rebrandly_api_key}",
    "workspace": f"{rebrandly_workspace}"
}

def get_url(x):
    url = response.json().get("articles")[x].get("url")
    return url

def request_link(url, art_num):
    return{
        "destination": f"{get_url(url)}", 
        "domain": { "fullName": "news.pkmeiner.com" },
        "slashtag": f"article-{art_num}"
    }

def post_request(url, art_num):
    r = requests.post("https://api.rebrandly.com/v1/links", 
        data = json.dumps(request_link(url, f'{art_num}')),
        headers=requestHeaders)

    return(r.json())

def news():
    try:
        del_links()
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

        short_url_1 = f"https://{post_request(0, 'one')['shortUrl']}"
        short_url_2 = f"https://{post_request(1, 'two')['shortUrl']}"
        short_url_3 = f"https://{post_request(2, 'three')['shortUrl']}"
        short_url_4 = f"https://{post_request(3, 'four')['shortUrl']}"
        short_url_5 = f"https://{post_request(4, 'five')['shortUrl']}"

        return(f"{id_one} - {title_one}\n{short_url_1}\n\n{id_two} - {title_two}\n{short_url_2}\n\n{id_three} - {title_three}\n{short_url_3}\n\n{id_four} - {title_four}\n{short_url_4}\n\n{id_five} - {title_five}\n{short_url_5}")
    except:
        print("API DOWN/CODE BROKEN")

def get_request(art_num):
    r = requests.get(f"https://api.rebrandly.com/v1/links?domain.fullName=news.pkmeiner.com&slashtag=article-{art_num}", 
        headers=requestHeaders)

    return r.json()

def del_links():
    try:
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
    except:
        return

def grab_and_send():
    account_sid = f'{twilio_account_sid}'
    auth_token = f'{twilio_auth_token}'
    client = Client(account_sid, auth_token)

    numbers_to_message = [f'{number_1}']
    for number in numbers_to_message:
        client.messages.create(
            body = f'Current Top Articles For: {get_time()}\n\n\n{get_quote()}\n\n\n{get_weather()}\n\n\n{news()}',
            from_ = f'{from_number}',
            to = f'{number}'
        )

schedule.every().day.at(time_to_send).do(grab_and_send)
schedule.every().day.at(time_to_del).do(del_links)

while True:
    schedule.run_pending()
    time.sleep(1)
