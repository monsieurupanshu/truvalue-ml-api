import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

MODEL_PATH = 'truvalue_model.pkl'
PREPROCESSOR_PATH = 'preprocessor.pkl'

def build_preprocessor(numeric_features, categorical_features):
    numeric_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])

    categorical_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore'))
    ])

    return ColumnTransformer(transformers=[
        ('num', numeric_pipeline, numeric_features),
        ('cat', categorical_pipeline, categorical_features)
    ])

def train_from_df(df: pd.DataFrame, model_path=MODEL_PATH, preprocessor_path=PREPROCESSOR_PATH):
    # Clean rows with missing target
    df = df.dropna(subset=['Price_AED'])

    features = ['Area_sqft', 'Bedrooms', 'Bathrooms', 'Location', 'Age_years']
    target = 'Price_AED'

    X = df[features]
    y = df[target]

    numeric_features = ['Area_sqft', 'Bedrooms', 'Bathrooms', 'Age_years']
    categorical_features = ['Location']

    preprocessor = build_preprocessor(numeric_features, categorical_features)

    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    pipeline.fit(X, y)

    joblib.dump(pipeline, model_path)
    joblib.dump(preprocessor, preprocessor_path)

    return pipeline, preprocessor  # so you can hot-swap in FastAPI