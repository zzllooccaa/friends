import requests
import json
import holidayapi
from datetime import date

apikey = '165d7e769fc14cc7aa07c13c6680bfb9'
ipadress = '89.216.117.87'

api_holiday = 'd32dcfe5-3229-479a-b90c-92aab6bae87b'


def get_api():
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
    print(holidays)



get_api()


# import reques
# import json
#
# with open("city.txt", "r") as imegrada:
#     try:
#         ime = imegrada.read()
#     except Error as er:
#         print(er)
#
# print(ime)
#
# r1 = requests.get(
#     'http://api.openweathermap.org/data/2.5/weather?q=' + ime + ',&appid=53428c410e91b12f9199fd56515ea70c')
# web1 = r1.text
#
# r = requests.get(
#     'http://api.openweathermap.org/data/2.5/weather?q=' + ime + ',&appid=53428c410e91b12f9199fd56515ea70c')
# web = r.json()
# print(web1)
