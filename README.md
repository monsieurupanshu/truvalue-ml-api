# 🏠 TruValue ML

A machine learning-powered property price prediction API, built using FastAPI and Docker. This project is developed as part of the TruValue ML Coding Challenge and demonstrates a fully containerized, production-ready pipeline for model inference and retraining.

---

## 📌 About

This repository showcases a FastAPI-based ML inference API that predicts real estate prices based on features such as area, location, number of bedrooms/bathrooms, and age. It also includes the ability to retrain the model on-the-fly using updated data.

The project is fully containerized using Docker and designed for ease of deployment, reproducibility, and extensibility.

---

## 📁 Project Structure

<pre>
├── Dockerfile               # Defines container image with Python 3.9 + API server
├── docker-compose.yml       # One-click orchestration to build & run API
├── main.py                  # FastAPI app with endpoints: /predict and /retrain
├── train_model.py           # Script to train model and export preprocessor + model
├── requirements.txt         # All required Python dependencies
├── property_data.csv        # Initial dataset used for model training
├── preprocessor.pkl         # Saved preprocessing pipeline (OneHotEncoder, Scaler)
├── truvalue_model.pkl       # Trained RandomForest model for price prediction
├── sample_request.json      # Sample input JSON payload for testing /predict
├── .gitignore               # Ignores __pycache__, .pkl, .env, temp files etc. </pre>

---

## 🔀 FLOW CONNECTIONS

1. `Client` → `FastAPI App`

2. `FastAPI App` → `Preprocessor` → `ML Model` → `Response` (back to Client)

3. `FastAPI App` → `Dataset (CSV)` (for retrain)

4. `Dataset` → `Preprocessor + Model` → `.pkl files`

5. All components grouped inside the Docker Cloud shape box

`/predict`: Sends JSON → preprocess → model → price

`/retrain`: Reloads dataset → retrains model → updates in memory

---

## 🧭 System Architecture

<img src="https://github.com/monsieurupanshu/truvalue-ml-api/blob/main/HDLC.png?raw=true" width="700"/>

---

## 🧠 How It Works
This section outlines how each core task in the project is implemented:

| ✅ Task                             | 💡 Implementation                                                                  |
| ---------------------------------- | ---------------------------------------------------------------------------------- |
| **Load + preprocess CSV data**     | `train_model.py` uses `pandas` + `scikit-learn` preprocessing pipelines            |
| **Train ML model**                 | `RandomForestRegressor` is trained and exported using `joblib`                     |
| **REST API creation**              | FastAPI app (`main.py`) serves endpoints `/predict` and `/retrain`                 |
| **Inference endpoint `/predict`**  | Accepts structured JSON, loads model/preprocessor, and returns the price output    |
| **Retraining endpoint `/retrain`** | Reloads dataset, retrains model, updates preprocessor + model in memory            |
| **Containerized deployment**       | `Dockerfile` + `docker-compose.yml` ensure consistent environment + easy execution |
| **Documentation**                  | Swagger UI is auto-hosted at [`localhost:8000/docs`](http://localhost:8000/docs)   |

## 🚀 Getting Started (Local Docker Setup)
Make sure Docker is installed and running.

### Clone this repo
```bash
git clone https://github.com/monsieurupanshu/truvalue-ml-api.git
```
```bash
cd truvalue-ml-api
```

### Build the container
```bash
docker compose build
```

### Run the API
```bash
docker compose up
```
The API will be available at:
[`localhost:8000/docs`](http://localhost:8000/docs)

## 📮 API Endpoints
🔹 POST `/predict`
### Sample JSON Payload
```bash
{
  "Area_sqft": 1800,
  "Bedrooms": 3,
  "Bathrooms": 3,
  "Location": "Downtown Dubai",
  "Age_years": 4
}
```

### Response
```bash
{
  "predicted_price": 2990400
}
```
---

🔹 POST `/retrain`

Triggers retraining of model using property_data.csv.

### Response
```bash
{
  "status": "✅ Model retrained and updated in memory."
}
```

**🔁 How to regenerate `.pkl` files**

Simply run the following command to train the model and export both artifacts:
```bash
python train_model.py
```

---

## 📷 API Endpoints Demo

### `/predict` Endpoint Response
<img src="https://github.com/monsieurupanshu/truvalue-ml-api/blob/main/Predict.png?raw=true" width="700"/>

### `/retrain` Endpoint Response
<img src="https://github.com/monsieurupanshu/truvalue-ml-api/blob/main/Retrain.png?raw=true" width="700"/>

---

## ✅ Sample API Execution via `curl`

<img src="https://github.com/monsieurupanshu/truvalue-ml-api/blob/main/Curl.png?raw=true" width="700"/>

---


### 🧪 Example: Predict Property Price
Use the following command to test the /predict endpoint:

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d @sample_request.json
```

---

### 🔁 Example: Retrain Model with New Data
Use the following command to retrain the model using property_data.csv:

```bash
curl -X POST "http://localhost:8000/retrain" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@property_data.csv;type=text/csv"
```
---

## 🔧 Design Decisions

1. **`FastAPI` for API Development:**
Chosen for its speed, modern async support, built-in validation via Pydantic, and interactive Swagger UI at /docs.

2. **`Random Forest Model` for Price Prediction:**
- ✅ Robustness: Performs well even with minimal hyperparameter tuning.
- 🌳 Handles Non-Linear Interactions: Captures complex relationships without the need for polynomial features.
- 📊 Tabular Data Friendly: Ideal for structured datasets like the one provided.
- 🧹 Minimal Preprocessing: Works well with encoded categorical features and scaled numerical data.
- 🔍 Interpretability: Feature importances can be extracted for insights.
- ⚖️ Strong Performance: Especially suitable for small-to-medium-sized datasets, as in this case.

3. **In-Memory Model Retraining:**
The model is retrained and updated in memory without restarting the API. This ensures zero-downtime deployment and faster response during development.

4. **`Model + Preprocessor` Saved as .pkl:**
Used pickle to persist both the OneHotEncoder + Scaler pipeline and the trained ML model, keeping preprocessing and inference in sync.

5. **CSV Upload for `/retrain`:**
Accepted CSV files using multipart/form-data to simplify input and mirror real-world bulk data ingestion.

6. **Input Validation with `Pydantic`:**
Ensures that the JSON payload for /predict contains all required fields with correct data types, improving reliability and debugging.

7. **`curl` Commands for Testing:**
Added reproducible curl commands in the README for verifying both endpoints via terminal without relying on third-party tools.

8. **Dockerized Deployment:**
Containerized with `Docker` and orchestrated using docker-compose for easy setup and consistent local/production environments.

9. **Modular File Structure:**
Separated `model training` (train_model.py), `API logic` (main.py), `data` (property_data.csv), and requirements for clarity and reusability.
---

## Extras

### 🧠 Other Possible Modeling Approaches

In real estate price prediction, several advanced ML algorithms can be used depending on dataset size, feature complexity, and desired performance.

🔹 XGBoost
- Known for its regularization and boosting power, ideal for tabular data.
- Performs well on large datasets with complex interactions.
- Can replace or complement Random Forest.

🔹 LightGBM
- A faster, memory-efficient alternative to XGBoost.
- Great for large-scale predictions with categorical features.

🔹 Stacked/Ensemble Models
- Combine models like Random Forest + XGBoost to reduce bias and variance.
- Averaging or meta-learners (e.g., Linear Regression on top) can yield better performance.

🔹 Deep Learning Models (e.g., DNNs): Could be explored if the dataset is large and contains more complex patterns, although overkill for this current small dataset.

### 🏠 What Does Zillow Use?
Zillow's Zestimate® leverages:
- Gradient Boosting Machines (GBMs) and deep learning models.
- Combined with location-based features, public records, user data, and historical trends.
- Extensive feature engineering and ensemble modeling.
