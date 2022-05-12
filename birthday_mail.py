import time
from datetime import datetime
from time import sleep
from model import User
from api.gmail import send_birth_mail
from config import cache
import asyncio


def act(x):
    return x + 10


def wait_start(runTime, action):
    startTime = time(*(map(int, runTime.split(':'))))
    while startTime > datetime.today().time():  # you can add here any additional variable to break loop if necessary
        sleep(1)  # you can change 1 sec interval to any other
    return action


async def send_birthday_mail():
    wait_start('13:55', lambda: act(100))
    for key in User.check_user_by_date_of_birth():
        print(key.email)
        print(key.name)
        cache.set("save_birth_email", key.email)
        cache.set("save_birth_name", key.name)
        await send_birth_mail()
        pass


asyncio.run(send_birthday_mail())
