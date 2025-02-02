import sys; sys.path.append(r"C:\Code_test\Twitter")
from m3_mlflow.infer_model import infer

import pandas as pd

new_test = pd.DataFrame([
[79.9700, 202307]
], columns = ["apt_area", "contract_date"])   
    
result = infer(new_test)
print(result)
print(type(result))

# Python에서 from 3_mlflow.infer_model_test import test와 같은 코드는
# 여전히 문법 오류를 유발합니다.
# Python에서는 패키지 이름이나 모듈 이름이
# 숫자로 시작하는 것을 허용하지 않기 때문입니다.