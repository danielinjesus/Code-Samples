# 서버실행 : uvicorn m2_FastAPI.v3_fastapi_json_wo_dantic_hinting:app --reload

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# class Input_Type(BaseModel):
#     infer : str

@app.post("/infer")
def post(user_input: dict):
    return {'result' : user_input['infer']+"==행복하군요"}

@app.get("/")
def get():
    return "행복하군요"