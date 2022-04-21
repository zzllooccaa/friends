from fastapi import FastAPI


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




if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")
