from pydantic import BaseModel

class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    IIN: str
    date_of_birth: str
    password: str

class PatientLogin(BaseModel):
    email: str
    password: str
