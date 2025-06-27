from fastapi import FastAPI, Depends

from app.api import misc, payments, subscriptions, tasks, users
import uvicorn

app = FastAPI(
    title="DatabaseAPI",
    version="2.0",
)
app.include_router(users.router)
app.include_router(misc.router)
app.include_router(payments.router)
app.include_router(subscriptions.router)
app.include_router(tasks.router)





if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)