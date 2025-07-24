# 🏠 TruValue ML API

A machine learning-powered property price prediction API, built using FastAPI and Docker. This project is developed as part of the TruValue ML Coding Challenge and demonstrates a fully containerized, production-ready pipeline for model inference and retraining.

---

## 📌 About

This repository showcases a FastAPI-based ML inference API that predicts real estate prices based on features such as area, location, number of bedrooms/bathrooms, and age. It also includes the ability to retrain the model on-the-fly using updated data.

The project is fully containerized using Docker and designed for ease of deployment, reproducibility, and extensibility.

---

## 📁 Project Structure

```text
├── Dockerfile               # Defines container image with Python 3.9 + API server
├── docker-compose.yml       # One-click orchestration to build & run API
├── main.py                  # FastAPI app with endpoints: /predict and /retrain
├── train_model.py           # Script to train model and export preprocessor + model
├── requirements.txt         # All required Python dependencies
├── property_data.csv        # Initial dataset used for model training
├── preprocessor.pkl         # Saved preprocessing pipeline (OneHotEncoder, Scaler)
├── truvalue_model.pkl       # Trained RandomForest model for price prediction
├── sample_request.json      # Sample input JSON payload for testing /predict
├── .gitignore               # Ignores __pycache__, .pkl, .env, temp files etc.
