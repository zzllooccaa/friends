from fastapi import FastAPI
from api.user import user_router
from api.dashboard import dashboard_router
from fastapi_pagination import add_pagination

import uvicorn

app = FastAPI(title="FRIENDS",
              description="WEB SOCIAL NETWORK",
              version="0.0.1",
              )

app.include_router(
    user_router,
    prefix="/user",
    tags=["user"],
)


app.include_router(
    dashboard_router,
    prefix="/dashboard",
    tags=["dashboard"],
)

add_pagination(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")
