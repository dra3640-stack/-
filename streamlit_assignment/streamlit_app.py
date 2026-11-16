import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="생성 AI 응용 프로그래밍", page_icon="🤖", layout="wide")

st.title("생성 AI 응용 프로그래밍")
st.caption("Streamlit + OpenAI 실습 프로젝트")

with st.sidebar:
    st.header("OpenAI 설정")
    api_key = st.text_input("OpenAI API Key", type="password",
                            value=st.session_state.get("api_key", ""))
    if api_key:
        st.session_state["api_key"] = api_key
        st.session_state["openai_client"] = OpenAI(api_key=api_key)
        st.success("API Client가 준비되었습니다.")
    else:
        st.session_state.pop("openai_client", None)
        st.info("기능을 사용하려면 API Key를 입력하세요.")

    st.divider()
    st.caption("API Key는 코드나 GitHub 저장소에 저장하지 않습니다.")

pages = [
    st.Page("app_pages/Home.py", title="Home", icon=":material/home:"),
    st.Page("app_pages/Chat.py", title="Chat", icon=":material/chat:"),
    st.Page("app_pages/Chatbot.py", title="도서관 Chatbot", icon=":material/local_library:"),
    st.Page("app_pages/ChatPDF.py", title="ChatPDF", icon=":material/picture_as_pdf:"),
]
pg = st.navigation(pages)
pg.run()
