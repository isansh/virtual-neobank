from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, SessionLocal
from app.core.security import hash_password
from app.models.user import Base, User
from app.routers import auth, users

Base.metadata.create_all(bind=engine)

def create_initial_admin():
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.email == "admin@neobank.ua").first():
            admin = User(
                email="admin@neobank.ua",
                hashed_password=hash_password("admin123"),
                full_name="Головний Адміністратор Банку",
                role="admin",
                kyc_status="verified",
                is_active=True
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()

create_initial_admin()

app = FastAPI(title="Virtual Neobank API")

# Глобальний перехоплювач помилок валідації (422)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field = err["loc"][-1]
        msg = err["msg"]
        if "at least 6 characters" in msg:
            errors.append("Пароль має містити щонайменше 6 символів")
        elif "valid email" in msg:
            errors.append("Введіть коректну адресу електронної пошти")
        elif "Field required" in msg:
            errors.append(f"Поле '{field}' є обов'язковим")
        else:
            errors.append(f"Помилка у полі '{field}': {msg}")
            
    return JSONResponse(
        status_code=422,
        content={"detail": ". ".join(errors)}
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Neobank API is running"}