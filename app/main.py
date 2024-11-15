import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from api import routes
from services.blockchain import initialize_blockchain_monitor
from services.ml_model import initialize_ml_model
from services.coin_initializer import initialize_token_addresses

# Создание таблиц базы данных
Base.metadata.create_all(bind=engine)

blockchain_client = initialize_blockchain_monitor()
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

app = FastAPI(
    title="Memecoin Tracker",
    description="API для отслеживания и прогнозирования роста мемкоинов на базе Solana",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

initialize_token_addresses()
initialize_ml_model()

# Dependency для сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Подключение маршрутов
app.include_router(routes.router)

# Пример корневого эндпоинта
@app.get("/")
def read_root():
    return {"message": "Memecoin Tracker API работает"}
