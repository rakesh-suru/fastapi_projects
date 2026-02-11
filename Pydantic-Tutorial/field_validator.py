from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator
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

    @field_validator("email")
    @classmethod
    def email_validator(cls, value):
        valid_domains = ["hdfc.com", "icici.com"]
        domain_name = value.split("@")[-1]

        if domain_name not in valid_domains:
            raise ValueError("Not a valid domain")

        return value
    
    @field_validator("name")
    @classmethod
    def name_validator(cls, value):
        return value.upper()
    
    @field_validator("age", mode = "before")
    @classmethod
    def age_validator(cls, value):
        if 0 < value < 100:
            return value
        else:
            raise ValueError("Age Should be between 0 and 100")
    
    
def check_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)


patient_info = {"name" : "kaushik", "email" : "kaushikkonda@hdfc.com" ,"website" : "http://kaushikkonda.com", "age" : 21, "weight" : 65.5, "married" : False, "allergies" : ["dust", "cold"], "contact_details" : {"website" : "kaushikkonda.com"}}
patient1 = Patient(**patient_info)

check_patient_data(patient1)