from pydantic import BaseModel

class Address(BaseModel):
    city: str 
    country: str 

class Student(BaseModel):
    id: str=None
    name: str
    age: int
    address: Address


