from streamlit_oauth import OAuth2Component
import streamlit as st
import requests as req
from dotenv import load_dotenv
load_dotenv("C:\Code_test\.env")
import os

# Set environment variables
AUTHORIZE_URL = os.getenv('AUTHORIZE_URL')
TOKEN_URL = os.getenv('TOKEN_URL')
REFRESH_TOKEN_URL = os.getenv('REFRESH_TOKEN_URL')
REVOKE_TOKEN_URL = os.getenv('REVOKE_TOKEN_URL')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
SCOPE = os.getenv('SCOPE')

# Create OAuth2Component instance
oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_URL, TOKEN_URL, REFRESH_TOKEN_URL, REVOKE_TOKEN_URL)

# Check if token exists in session state
if 'token' not in st.session_state:
    # If not, show authorize button
    result = oauth2.authorize_button("Authorize", REDIRECT_URI, SCOPE)
    if result and 'token' in result:
        # If authorization successful, save token in session state
        st.session_state.token = result.get('token')
        st.rerun()
else:
    # If token exists in session state, show the token
    token = st.session_state['token']
    st.json(token)
    if st.button("Refresh Token"):
        # If refresh token button is clicked, refresh the token
        token = oauth2.refresh_token(token)
        st.session_state.token = token
        st.rerun()

authorize_button(self, name, redirect_uri, scope, height=800, width=600, key=None, extra_params={}, pkce=None, use_container_width=False, icon=None)

st.title("Upstage 4조 MLOps 프로젝트")
st.header('Streamlit')
user_input = st.text_input('감정분석 할 텍스트 입력')

if st.button('post'):
    if user_input.strip():
        try:
            r = req.post(
                "http://127.0.0.1:8000/infer",
                json={"infer": user_input}
            )
            if r.status_code == 200:
                result = r.json()
                st.text("당신의 지금 감정은? :")
                st.text(result['result'])
            else:
                st.text("FastAPI 서버에서 오류가 발생했습니다.")
                st.text(r.status_code)
        except req.exceptions.RequestException as e:
            st.error(f"Request failed: {str(e)}")
    else: 
        st.text("감정분석할 내용을 입력해주세요!")
        
if st.button('get'):
    st.text(req.get("http://127.0.0.1:8000/").text)

# st.components.v1.html(
#     """
#     <iframe src="https://danielinjesus.github.io/tosspayments/toss_blog_origin.html" width="100%" height="600" frameborder="0">
#     </iframe>
#     """,
#     height=600,
# )

#실행: streamlit run C:\Code_test\Twitter\m1_Streamlit\v3_streamlit_json_google.py