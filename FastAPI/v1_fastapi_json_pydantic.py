# 서버실행 : uvicorn v1_fastapi_json_pydantic:app --reload

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Input_Type(BaseModel):
    infer : str

@app.post("/infer")
def post(user_input: BaseModel):
    return {'result' : user_input.infer+"==행복하군요"}

@app.get("/")
def get():
    return "행복하군요"