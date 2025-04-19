import mlflow
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import os
from dotenv import load_dotenv
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import  OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Chargement des données
df = pd.read_csv("get_around_pricing_project.csv")
df.drop(columns=["Unnamed: 0"], inplace=True)

# regroupement des marques de voitures qui ont moins de 30 occurences dans le dataset
brand_count = df['model_key'].value_counts()
min_threshold = 30
rare_brands = brand_count[brand_count < min_threshold].index.to_list()
df['model_key'] = df['model_key'].apply(lambda x: 'Others' if x in rare_brands else x)

# Configuration de MLflow
load_dotenv()
os.environ["APP_URI"] = "https://data-jed-dsfs-mlflow.hf.space" 
EXPERIMENT_NAME="pricing-prediction-getaround-project"
mlflow.set_tracking_uri(os.environ["APP_URI"])

# AWS Cdredentials pour le stockage des artefacts
os.environ['AWS_ACCESS_KEY_ID'] = os.getenv("AWS_ACCESS_KEY_ID")
os.environ['AWS_SECRET_ACCESS_KEY'] = os.getenv("AWS_SECRET_ACCESS_KEY")

# Definir l'experiment
mlflow.set_experiment(EXPERIMENT_NAME)
experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

# Préparation des données
target_variable = "rental_price_per_day"
X = df.drop(target_variable, axis=1)
y = df[target_variable]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Définir les variables catégorielles et numériques
numeric_features = X.select_dtypes(include=[np.number]).columns
categorical_features = X.select_dtypes(exclude=[np.number]).columns

# Démarrer le run MLflow
with mlflow.start_run(experiment_id=experiment.experiment_id, run_name="linear_regression_model_2") as run:

    # Logger les paramètres du split des données
    mlflow.log_param("test_size", 0.2)
    mlflow.log_param("random_state", 42)
    mlflow.log_param("min_brand_threshold", min_threshold)

    # Créer le pipeline de prétraitement
    numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
    ('encoder', OneHotEncoder(drop='first'))
])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
    ]
)

# Pipeline complet
    full_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])
    
    # Entraîner le modèle
    full_pipeline.fit(X_train, y_train)
    
    # Extraire le modèle de régression
    regressor = full_pipeline.named_steps['regressor']
    
    # Logger les paramètres du modèle
    mlflow.log_param("fit_intercept", regressor.fit_intercept)
    
    # Prédire
    y_train_pred = full_pipeline.predict(X_train)
    y_test_pred = full_pipeline.predict(X_test)
    
    # Calculer et logger les métriques de régression
    # Métriques sur l'ensemble d'entraînement
    train_mse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    train_mae = mean_absolute_error(y_train, y_train_pred)
    train_r2 = r2_score(y_train, y_train_pred)
    
    mlflow.log_metric("train_rmse", train_mse)
    mlflow.log_metric("train_mae", train_mae)
    mlflow.log_metric("train_r2", train_r2)
    
    # Métriques sur l'ensemble de test
    test_mse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    test_mae = mean_absolute_error(y_test, y_test_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    
    mlflow.log_metric("test_rmse", test_mse)
    mlflow.log_metric("test_mae", test_mae)
    mlflow.log_metric("test_r2", test_r2)
    
    # Afficher les résultats
    print("Modèle de Régression Linéaire")
    print(f"R² (test): {test_r2:.4f}")
    print(f"RMSE (test): {test_mse:.4f}")
    print(f"MAE (test): {test_mae:.4f}")
    
    
    # Logger le modèle complet
    mlflow.sklearn.log_model(full_pipeline, "linear_regression_model")
    
    # 8. Ajouter des tags
    mlflow.set_tag("model_type", "linear_regression")
    mlflow.set_tag("data_source", "get_around_pricing_project.csv")
    mlflow.set_tag("categorical_encoding", "one_hot_encoder")
    mlflow.set_tag("numeric_scaling", "standard_scaler")
    



