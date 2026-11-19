from fastapi import FastAPI
from app.core.database import engine
from app.models.user import Base
from app.models import card  # noqa: F401
from app.routers import auth, users, cards

# Створюємо таблиці в БД
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Virtual Neobank API")

# Підключаємо роути
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(cards.router)

@app.get("/")
def root():
    return {"message": "Neobank API is running"}
