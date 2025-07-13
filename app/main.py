from fastapi import FastAPI, Depends, APIRouter

from app.api import payments, subscriptions, tasks, users, misc, auth, assistant
from app.services import yookassa_routes
import uvicorn

app = FastAPI(
    title="DatabaseAPI",
    version="2.0",
)
router = APIRouter()


@router.get("/")
async def root():
    return {200: "Database is working"}


app.include_router(router)
app.include_router(users.router)
app.include_router(misc.router)
app.include_router(payments.router)
app.include_router(subscriptions.router)
app.include_router(tasks.router)
app.include_router(assistant.router)
app.include_router(yookassa_routes.router)
app.include_router(auth.router, prefix="/auth")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
