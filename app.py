import streamlit as st
import google.generativeai as genai

def get_gemini_response(prompt):
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        if not api_key:
            return "❌ API key not found. Please set GOOGLE_API_KEY in .streamlit/secrets.toml."

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"❌ Error: {str(e)}"

# 페이지 설정
st.set_page_config(page_title="Gemini Chatbot", page_icon="💬")

# 세션 히스토리 초기화
if "history" not in st.session_state:
    st.session_state.history = []

# UI 렌더링
st.title("💬 Gemini Chatbot")

# 기존 대화 표시
for role, message in st.session_state.history:
    with st.chat_message(role):
        st.markdown(message)

# 사용자 입력
user_input = st.chat_input("Ask something...")

if user_input:
    # 사용자 메시지 출력
    st.session_state.history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # Gemini 응답 생성
    with st.chat_message("assistant"):
        response = get_gemini_response(user_input)
        st.markdown(response)
        st.session_state.history.append(("assistant", response)) 
