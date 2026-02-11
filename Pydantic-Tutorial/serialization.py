from pydantic import BaseModel

class Address(BaseModel):

    city : str
    state : str
    pin : str

class Patient(BaseModel):

    name : str
    gender : str
    age : str
    address : Address

address_dict = {"city" : "hyderabad", "state" : "telangana", "pin" : "500059"}

address1 = Address(**address_dict)

patient_dict = {"name" : "Vineeth", "gender" : "male", "age" : "22", "address" : address1}

patient1 = Patient(**patient_dict)

temp = patient1.model_dump(exclude = {"address" : ["state"]})
print(temp)
print(type(temp))