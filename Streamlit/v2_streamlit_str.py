# 실행 streamlit run C:\Code_test\Twitter\1.Streamlit\v2_streamlit_str_err.py
import streamlit as st
import requests as req

st.title("Upstage 4조 MLOps 프로젝트")
st.header('Streamlit')
user_input = st.text_input('감정분석 할 텍스트 입력')

if st.button('확인'):
    if user_input.strip():
        try:
            r = req.post(
                "http://127.0.0.1:8000/infer",
                data=user_input, 
                headers={"Content-Type": "text/plain"}
            )
            if r.status_code == 200:
                result = r.text
                st.text("당신의 지금 감정은? :")
                st.text(result)
            else:
                st.text("FastAPI 서버에서 오류가 발생했습니다.")
        except Exception as e:
            st.text(f"FastAPI 서버에 연결할 수 없습니다. 오류: {e}")
    else:
        st.text("감정분석할 내용을 입력해주세요!")