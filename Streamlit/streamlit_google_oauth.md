✅ Streamlit에서 Google OAuth 로그인 구현이 일반 웹 프론트엔드보다 더 어렵냐?
👉 Streamlit이 일반 웹 프론트(React, Vue, Django, Flask 등)보다 OAuth 로그인 구현이 더 복잡할 수 있어.
✅ 하지만, Streamlit에 맞는 방식으로 구현하면 충분히 간단하게 만들 수도 있어! 🚀

🔹 1️⃣ 일반 웹 프론트(React, Vue) vs Streamlit에서 OAuth 로그인 비교
구분	일반 웹 프론트 (React, Vue, Django 등)	Streamlit
로그인 UI	<button onClick={handleLogin}> 클릭 이벤트	st.button("로그인") 버튼 사용
OAuth 리디렉션 처리	window.location.href = "https://accounts.google.com/o/oauth2/auth..."	st.experimental_rerun() 등 별도 처리 필요
토큰 저장 위치	localStorage, sessionStorage, 쿠키 등	st.session_state (단, 새로고침 시 유지 안됨)
서버에서 토큰 검증	Express, Django, Flask API	Streamlit 내부에서 API 요청 처리 가능
로그아웃 처리	localStorage.clear() 후 페이지 리로드	st.session_state.pop("token", None) 사용
➡ Streamlit은 기본적으로 "싱글 페이지 앱(SPA) 구조가 아니기 때문에" OAuth 리디렉션 처리와 토큰 저장이 더 어렵게 느껴질 수 있음!

🔹 2️⃣ 일반 웹 프론트에서 OAuth 로그인 흐름 (React + Flask 예제)
일반적인 웹 프론트(React, Vue)에서는 아래처럼 Google OAuth 로그인을 쉽게 구현할 수 있어.

✅ React에서 Google OAuth 로그인 버튼

javascript
복사
편집
const handleLogin = () => {
    window.location.href = `https://accounts.google.com/o/oauth2/auth?client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost:3000/callback&response_type=code&scope=email profile`;
};
<button onClick={handleLogin}>Google 로그인</button>
➡ 버튼 클릭하면 OAuth 인증 URL로 리디렉션됨.

✅ Flask 백엔드에서 OAuth 인증 처리

python
복사
편집
@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_url = "https://oauth2.googleapis.com/token"
    
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": "http://localhost:3000/callback",
        "grant_type": "authorization_code",
    }
    
    response = requests.post(token_url, data=data)
    access_token = response.json()["access_token"]
    
    return jsonify({"access_token": access_token})  # 클라이언트로 토큰 반환
➡ React가 이 토큰을 localStorage에 저장하고 API 요청 시 Authorization 헤더에 포함하면 됨.

🔹 3️⃣ Streamlit에서 Google OAuth 로그인 구현이 어려운 이유
OAuth 리디렉션을 직접 처리해야 함

일반 웹 프론트(React, Django)에서는 redirect_uri를 설정하면 자동으로 이동하지만,
Streamlit은 기본적으로 싱글 페이지 앱(SPA)이 아니므로 직접 st.experimental_rerun()을 사용해서 리디렉션을 처리해야 함.
세션 상태 (st.session_state)는 새로고침하면 날아감

일반 웹 프론트에서는 localStorage 또는 쿠키에 토큰을 저장할 수 있지만,
Streamlit에서는 기본적으로 세션이 새로고침하면 사라지기 때문에 저장 방법을 따로 마련해야 함.
OAuth 로그인 UI를 만들기가 불편함

Streamlit은 st.button()을 사용해서 OAuth 로그인 버튼을 만들 수 있지만,
React처럼 onClick 이벤트에서 직접 OAuth 요청을 보낼 수 없기 때문에 UI/UX가 제한적임.
🔹 4️⃣ 그래도 Streamlit에서 OAuth 로그인 만들 수 있음! (구현 예제)
💡 Streamlit에서 Google OAuth 로그인 버튼을 만들고, 토큰을 세션에 저장하는 방법!

✅ 1. Streamlit에서 Google OAuth 로그인 버튼 만들기
python
복사
편집
import streamlit as st
import requests

CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REDIRECT_URI = "http://localhost:8501"

# 세션 상태 초기화
if "token" not in st.session_state:
    st.session_state.token = None

# 로그인 버튼 클릭 시 Google OAuth로 이동
if st.button("Google 로그인"):
    auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=email profile"
    st.write(f"[로그인하세요]({auth_url})")  # Streamlit에서는 직접 링크를 제공해야 함

# OAuth 콜백 처리 (사용자가 로그인하면 URL에 "code=..." 포함됨)
if "code" in st.query_params:
    code = st.query_params["code"]
    
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    
    response = requests.post(token_url, data=data)
    
    if response.status_code == 200:
        st.session_state.token = response.json()["access_token"]
        st.success("로그인 성공! 🎉")
    else:
        st.error("로그인 실패!")
➡ ✅ 로그인 버튼을 클릭하면 Google OAuth 로그인 페이지로 이동!
➡ ✅ 로그인이 성공하면 토큰을 st.session_state에 저장!
➡ ❌ 하지만 페이지를 새로고침하면 세션 상태가 날아감 → 해결 방법 필요!

✅ 2. Streamlit에서 OAuth 토큰을 유지하는 방법 (해결책)
Streamlit의 st.session_state는 페이지를 새로고침하면 사라지므로, st.secrets 또는 쿠키/Redis에 저장하면 해결 가능!

python
복사
편집
import streamlit as st

if "token" not in st.session_state:
    st.session_state.token = st.secrets.get("oauth_token", None)

if st.session_state.token:
    st.write("✅ 로그인 성공! 관리자 페이지 접근 가능")
else:
    st.write("🚀 Google 로그인이 필요합니다.")
➡ ✅ 이렇게 하면 OAuth 토큰이 유지되므로 페이지 새로고침 후에도 로그인 상태 유지 가능! 🚀

🔹 5️⃣ 정리: 일반 웹 프론트와 Streamlit의 OAuth 로그인 비교
구분	일반 웹 프론트(React, Vue)	Streamlit
OAuth 로그인 버튼	onClick={handleLogin} 이벤트 사용	st.button("로그인") 후 링크 제공
토큰 저장	localStorage, sessionStorage, 쿠키	st.session_state, st.secrets 사용
리디렉션 처리	window.location.href = "OAuth_URL"	st.experimental_rerun() 또는 링크 제공
로그아웃 처리	localStorage.clear() 후 리디렉션	st.session_state.pop("token") 사용
페이지 새로고침 후 유지	✅ 가능 (localStorage 사용)	❌ 기본적으로 불가능 (st.session_state가 날아감)
OAuth 로그인 난이도	⭐⭐⭐ (쉬움)	⭐⭐⭐⭐ (약간 어려움)
💡 결론:
✅ Streamlit에서 OAuth 로그인 구현이 일반 웹 프론트보다 더 어려울 수 있음!
✅ 하지만 st.session_state, st.secrets, 쿠키/Redis를 활용하면 충분히 가능함!
✅ 페이지 새로고침 후에도 로그인 상태를 유지하려면 추가 구현이 필요!

🚀 그래도 Streamlit에서도 OAuth 로그인을 만들 수 있으니 도전해볼 만해! 😊