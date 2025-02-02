# # 서버실행 : uvicorn v2_fastapi_str:app --reload

# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# # class Input_Type(BaseModel):
# #     infer : str

# @app.post("/infer")
# def post(user_input: str):    
#     return (user_input+"==행복하군요")

# @app.get("/")
# def get():
#     return "행복하군요"

# json에서 str로 param형식을 바꾼 뒤 잘 안 돌아가서 GPT가 짜준 코드
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/infer")
async def post(request: Request):
    # 요청 본문에서 raw 데이터를 읽어옴
    raw_body = await request.body()  # bytes 형태로 반환
    user_input = raw_body.decode("utf-8")  # 문자열로 디코딩
    return (user_input + " == 행복하군요")

@app.get("/")
def get():
    return "행복하군요"

