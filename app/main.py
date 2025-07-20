from fastapi import FastAPI, APIRouter

from app.api import payments, subscriptions, tasks, users, misc, auth, assistant
from app.services import yookassa_routes
import uvicorn

app = FastAPI(
    title="DatabaseAPI",
    version="2.0"
)
router = APIRouter()


@router.get("/")
async def root():
    return {200: "Database is working"}


app.include_router(router, prefix="/api/v2")
app.include_router(users.router, prefix="/api/v2")
app.include_router(misc.router, prefix="/api/v2")
app.include_router(payments.router, prefix="/api/v2")
app.include_router(subscriptions.router, prefix="/api/v2")
app.include_router(tasks.router, prefix="/api/v2")
app.include_router(assistant.router, prefix="/api/v2")
app.include_router(yookassa_routes.router, prefix="/api/v2")
app.include_router(auth.router, prefix="/api/v2")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
