import os
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import load_model
from sklearn.ensemble import RandomForestRegressor
import joblib

MODEL_PATH = "models/token_growth_model.h5"

def initialize_ml_model():
    """
    Загружает модель, если файл модели существует. Если нет, обучает новую модель.
    """
    if os.path.exists(MODEL_PATH):
        model = load_model(MODEL_PATH)
        print("Модель загружена.")
    else:
        model = train_new_model()
        model.save(MODEL_PATH)
        print("Новая модель обучена и сохранена.")
    return model

def train_new_model():
    """
    Создаёт и обучает новую модель, если сохранённой модели нет.
    """
    # Замените на логику обучения модели, например, с помощью RandomForestRegressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    # Пример: создайте и сохраните модель в формате h5 или joblib, если используете RandomForest
    joblib.dump(model, "models/token_growth_model.pkl")
    return model
