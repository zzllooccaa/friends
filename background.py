import requests
import json

apikey = '165d7e769fc14cc7aa07c13c6680bfb9'
ipadress = '89.216.117.87'


def get_api():
    # response = requests.get("https://ipgeolocation.abstractapi.com/v1/?api_key=165d7e769fc14cc7aa07c13c6680bfb9")
    response = requests.get(
        "https://ipgeolocation.abstractapi.com/v1/?api_key=" + apikey + "& ip_address=" + ipadress + "&fields=country")
    text_json = json.loads(response.text)
    ''' izvlaci samo ime drzave'''
    print(text_json['country'])



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
