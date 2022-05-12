import requests
import json
import holidayapi
from datetime import date

import schemas
from model import User, db
import time

apikey = '165d7e769fc14cc7aa07c13c6680bfb9'
ipadress = '89.216.117.87'
save_mail = 'klinikaprojekat45@gmail.com'
api_holiday = 'd32dcfe5-3229-479a-b90c-92aab6bae87b'

""" Background task da na osnovu geolokacije dohvati odakle je user,\
da proveri dal ima neki praznik i da ga upise u tabelu"""
def get_api():
    time.sleep(15)
    # response = requests.get("https://ipgeolocation.abstractapi.com/v1/?api_key=165d7e769fc14cc7aa07c13c6680bfb9")
    response = requests.get(
        "https://ipgeolocation.abstractapi.com/v1/?api_key=" + apikey + "& ip_address=" + ipadress + "&fields=country")
    text_json = json.loads(response.text)
    ''' izvlaci samo ime drzave'''
    print(text_json['country'])
    hapi = holidayapi.v1(api_holiday)
    hapi_month = date.today().month
    print(hapi_month)
    hapi_year = date.today().year
    print(hapi_year)
    hapi_day = date.today().day
    print(hapi_day)
    parameters = {
        # Required
        'country': 'US',
        'year': 2021,
        # Optional
        # 'month': hapi_month,
        # 'day': hapi_day,
        # 'previous': True,
        # 'upcoming': True,
        # 'public':   True,
        # 'pretty':   True,
    }
    holidays = hapi.holidays(parameters)
    user = User.get_user_by_email(email=save_mail)
    message = holidays['status']
    messages = holidays['warning']
    print(user.id, user.name)
    print(str(message))
    print(str(messages))
    user.holiday = str(message)
    db.commit()
    return print('success')
