from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):

    name : Annotated[str, Field(max_length= 50, title = "Name of the Patient", description= "Identifies the Patient by their name(must have less than 50 characters)", examples= ["Sanjay", "Dhruv"])]
    email : EmailStr
    website : AnyUrl
    age : int = Field(gt = 0, lt = 120)
    weight : Annotated[float, Field(gt = 0, strict= True)]
    married : Annotated[bool, Field(default= False, description= "True or False")]
    allergies : Optional[List[str]] = None
    contact_details : Dict[str, str]

def check_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)


patient_info = {"name" : "kaushik", "email" : "kaushikkonda@gmail.com" ,"website" : "http://kaushikkonda.com", "age" : 21, "weight" : 65.5, "married" : False, "allergies" : ["dust", "cold"], "contact_details" : {"website" : "kaushikkonda.com"}}
patient1 = Patient(**patient_info)

check_patient_data(patient1)