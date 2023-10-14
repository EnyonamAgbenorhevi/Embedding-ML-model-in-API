from fastapi import FastAPI,Form, Body,Path
from typing import Annotated
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import numpy as np
import uvicorn
from fastapi.responses import JSONResponse


app = FastAPI()

# Load the numerical imputer, scaler, and model
num_imputer_filepath = "joblib_files/numerical_imputer.joblib"
scaler_filepath = "joblib_files/scaler.joblib"
model_filepath = "joblib_files/lr_model.joblib"

num_imputer = joblib.load(num_imputer_filepath)
scaler = joblib.load(scaler_filepath)
model = joblib.load(model_filepath)

class PatientData(BaseModel):
    PRG: float 
    PL: float
    PR: float
    SK: float
    TS: float
    M11: float
    BD2: float
    Age: float
    Insurance: int

def preprocess_input_data(user_input):
    input_data_df = pd.DataFrame([user_input])
    num_columns = [col for col in input_data_df.columns if input_data_df[col].dtype != 'object']
    input_data_imputed_num = num_imputer.transform(input_data_df[num_columns])
    input_scaled_df = pd.DataFrame(scaler.transform(input_data_imputed_num), columns=num_columns)
    return input_scaled_df

@app.get("/")
def read_root():
        return "Sepsis Prediction App"
@app.post("/sepsis/predict")
def get_data_from_user(data:PatientData):
    user_input = data.dict()
    input_scaled_df = preprocess_input_data(user_input)
    probabilities = model.predict_proba(input_scaled_df)[0]
    prediction = np.argmax(probabilities)

    sepsis_status = "Positive" if prediction == 1 else "Negative"
    probability = probabilities[1] if prediction == 1 else probabilities[0]

    if prediction == 1:
        sepsis_explanation = "A positive prediction suggests that the patient might be exhibiting sepsis symptoms and requires immediate medical attention."
    else:
        sepsis_explanation = "A negative prediction suggests that the patient is not currently exhibiting sepsis symptoms."

    statement = f"The patient's sepsis status is {sepsis_status} with a probability of {probability:.2f}. {sepsis_explanation}"

    user_input_statement = "user-inputted data: "
    output_df = pd.DataFrame([user_input])

    result = {'predicted_sepsis': sepsis_status, 'statement': statement, 'user_input_statement': user_input_statement, 'input_data_df': output_df.to_dict('records')}
    return result

