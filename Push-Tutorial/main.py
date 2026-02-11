from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal

app = FastAPI()

class Patient(BaseModel):
    id : Annotated[str, Field(..., description = "ID of the patient", examples = ["P001"])]
    name : Annotated[str, Field(..., description = "Name of the patient", examples = ["Badri"] )]
    city : Annotated[str, Field(..., description = "City of the patient", examples = ["Hyderabad"] )]
    age : Annotated[int, Field(..., gt = 0, lt = 120, description = "Age of the patient", examples = ["21"] )]
    gender : Annotated[Literal["male", "female", "others"], Field(..., description = "Gender of the patient")]
    height : Annotated[float, Field(..., description = "Height of the patient in meters", examples = ["1.74"] )]
    weight : Annotated[float, Field(..., description = "Weight of the patient in kgs", examples = ["60"] )]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Normal"
        else:
            return "Obese"
        
def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    
    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)


@app.get("/")
def hello():
    return {'message' : 'Patient Management System API'}

@app.get('/about')
def about():
    return {'message' : "A functional API to manage patient records"}

@app.get('/view')
def view():
    data = load_data()

    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description= "ID of the Patient", example = "P001")):
    data = load_data() 

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code = 404, detail = "Patient not Found!")

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description= "Sort the patients on the basis of height, weight or BMI"), order: str = Query("asc", description= "Sort in ascending or descending order")):

    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code= 400, detail = f"Invalid Field, please select from {valid_fields}")
    

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code= 400, detail= "Invalid order, please select form 'asc' or 'desc'")

    data = load_data()

    sort_order = True if order == "desc" else False
    
    sorted_data = sorted(data.values(), key = lambda x : x.get(sort_by, 0), reverse= sort_order)

    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):

    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code= 400, detail= "Patient Already Exist")
    
    data[patient.id] = patient.model_dump(exclude = ["id"])

    save_data(data)

    return JSONResponse(status_code= 201, content= {"message" : "patient created successfully"})
