from fastapi import APIRouter,HTTPException, status, Query
from models.user import Student
from config.db import get_mongo_client

import uuid


user=APIRouter()

def generate_id():
    return str(uuid.uuid4())

client = get_mongo_client()

@user.post('/students', status_code=status.HTTP_201_CREATED)
async def create_students(user:Student):
   user_data = dict(user)
   if not user_data.get("id"):
       user_data["id"] = generate_id() 
   user_data["address"] = dict(user_data["address"])  
   result  = client.crud.user.insert_one(user_data)
   if result.inserted_id:
        return {"id": user_data["id"]}
   else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create student")

@user.get('/students')
async def list_students(country: str = Query(None), age: int = Query(None)):
    query = {}
    if country is not None:
        query["address.country"] = {"$eq":country}
    if age is not None:
        query["age"] = {"$gte": age}
    students = client.crud.user.find(query)
    
    response_data = [{"name": student["name"], "age": student["age"]} for student in students]

    return {"data": response_data}

@user.get('/students/{id}')
async def fetch_student(id:str):
    student_data = client.crud.user.find_one({"id": id})
    if student_data:
        return {
            "name": student_data["name"],
            "age": student_data["age"],
            "address": {
                "city": student_data["address"]["city"],
                "country": student_data["address"]["country"]
            }
        }
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

@user.patch('/students/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_student(id: str, user: Student):
    user_data = user.dict() 
    user_data.pop("id", None) 
    result = client.crud.user.update_one({"id": id}, {"$set": user_data})
    if result.modified_count != 0:
        return {}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")



@user.delete('/students/{id}')
async def delete_student(id: str):
    deleted_student = client.crud.user.find_one_and_delete({"id": id})
    if deleted_student:
        return {}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")


