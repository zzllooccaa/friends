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