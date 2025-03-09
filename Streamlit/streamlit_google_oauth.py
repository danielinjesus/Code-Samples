import streamlit as st
from google_auth_oauthlib.flow import Flow
import requests

st.title("Google OAuth 로그인")

# ✅ 세션 상태에서 토큰 유지 (없으면 초기화)
if "token" not in st.session_state:
    st.session_state.token = None

# ✅ Google OAuth 설정
CLIENT_ID = "your-client-id.apps.googleusercontent.com"
CLIENT_SECRET = "your-client-secret"
REDIRECT_URI = "http://localhost:8501"
SCOPES = ["https://www.googleapis.com/auth/userinfo.profile"]

# ✅ 로그인 버튼 클릭 시 Google OAuth 시작
if st.button("Google 로그인"):
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uris": [REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
    )
    flow.redirect_uri = REDIRECT_URI
    auth_url, _ = flow.authorization_url(prompt="consent")
    st.write(f"[로그인하세요]({auth_url})")

# ✅ 로그인 후 Google이 반환한 콜백 처리 (URL에서 토큰 추출)
if "code" in st.query_params:
    flow.fetch_token(code=st.query_params["code"])
    creds = flow.credentials
    st.session_state.token = creds.token  # ✅ OAuth 토큰을 세션에 저장
    st.success("로그인 성공! 🎉")

# ✅ 저장된 토큰 확인
if st.session_state.token:
    st.write(f"저장된 토큰: {st.session_state.token}")

    # ✅ Google API를 사용해 사용자 정보 가져오기
    user_info = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        headers={"Authorization": f"Bearer {st.session_state.token}"}
    ).json()
    st.write("사용자 정보:", user_info)
