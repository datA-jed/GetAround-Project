import mlflow 
import uvicorn
import pandas as pd 
from pydantic import BaseModel
from typing import Literal, List, Union
from fastapi import FastAPI, File, UploadFile
from fastapi.encoders import jsonable_encoder
import joblib

# Log model from mlflow 
logged_model = 'runs:/1d4bad1197fc433ead8f50dde8b7a58c/linear_regression_model'

# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(logged_model)

tags_metadata = [
    {
        "name": "Machine Learning",
        "description": "Prediction Endpoint."
    }
]

app = FastAPI(
    title="ML API GetAround",
    description="This is a simple API to predict the price of a car based on its features.",
    openapi_tags=tags_metadata
)

class Car(BaseModel):
    model_key:Literal['Citroën','Peugeot','PGO','Renault','Audi','BMW','Mercedes','Opel','Volkswagen','Ferrari','Mitsubishi','Nissan','SEAT','Subaru','Toyota','Others']
    mileage:Union[int, float]
    engine_power:Union[int, float]
    fuel:Literal['diesel','petrol','hybrid_petrol', 'electro']
    paint_color:Literal['black','grey','white','red','silver','blue','beige','brown','green', 'orange']
    car_type:Literal['convertible','coupe','estate','hatchback','sedan','subcompact','suv','van']
    private_parking_available:bool
    has_gps:bool
    has_air_conditioning:bool
    automatic_car:bool
    has_getaround_connect:bool
    has_speed_regulator:bool
    winter_tires:bool


@app.get("/", tags=["Introduction Endpoints"])
async def index():
    """
    Simply returns a welcome message!
    """
    message = "Hello world! This `/` is the most simple and default endpoint. If you want to learn more, check out documentation of the api at `/docs`"
    return message


@app.post("/predict", tags=["Machine Learning"])
async def predict(cars: List[Car]):
    # Read data 
    input_data = pd.DataFrame(jsonable_encoder(cars))

    prediction = loaded_model.predict(input_data)

    # Format response
    response = {"prediction": prediction.tolist()}
    return response