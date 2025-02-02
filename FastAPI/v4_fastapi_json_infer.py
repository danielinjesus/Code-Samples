import sys; sys.path.append (r"C:\Code_test\Twitter") #파이썬에 가져올 패키지 경로 등록 
from m3_mlflow.infer_model import infer
import pandas as pd, logging; from fastapi import FastAPI; from pydantic import BaseModel
class Input_Type (BaseModel):
    infer : str
    
app=FastAPI()

@app.post("/infer")
def post(user_input: Input_Type):    
    new_test = pd.DataFrame([ [79.9700, 202307] ],
                            columns = ["apt_area", "contract_date"]
                            )   
    try:
        result = infer(new_test) # 모델 추론 부분        
        return {'result' : f"{user_input.infer}==행복하군요+{result[0]}+후후하하"}    
    except Exception as e:
        logging.error(f"Error occurred: {e}", exc_info=True)
        return {'error': str(e)}
@app.get("/")
def get():
    return "행복하군요"

# 서버실행 : uvicorn v4_fastapi_json_infer:app --reload