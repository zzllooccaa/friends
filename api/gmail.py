from fastapi_mail import MessageSchema, ConnectionConfig, FastMail
from starlette.responses import JSONResponse
import time
from config import cache

conf = ConnectionConfig(
    MAIL_USERNAME="klinikaprojekat45@gmail.com",
    MAIL_PASSWORD="cepidlaka",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    MAIL_FROM="klinikaprojekat45@gmail.com",
)
var = "CLICK ON LINK BELOW"


async def send_birth_mail():
    time.sleep(3)
    birth_mail_redis = cache.get("save_birth_email")
    birth_name_redis = cache.get("save_birth_name")

    message = MessageSchema(
        subject=" HAPPY BIRTHDAY ",
        recipients=[birth_mail_redis],
        body="\n"
             "\n"
             "\n"
             "Dear,     \n"
             "" + birth_name_redis + "\n"
                                     "Wishing you a day full of laughter and happiness and a year that brings you much success.\n"
                                     "\n"
                                     "\n"
                                     "HAPPY BIRTHDAY\n"
                                     "Your clinic\n"
                                     "\n"
                                     "\n"
                                     "\n",
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    print("MAIL JUST SEND TO", birth_mail_redis)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
