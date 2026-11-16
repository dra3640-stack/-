import streamlit as st

st.title("💬 Chat")
st.write("대화 내용을 기억하고 응답을 스트리밍하는 챗봇입니다.")

client = st.session_state.get("openai_client")
if client is None:
    st.warning("왼쪽 사이드바에 OpenAI API Key를 입력하세요.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

def clear_chat():
    st.session_state.messages = []

st.button("Clear", on_click=clear_chat)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("메시지를 입력하세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    def text_chunks():
        stream = client.responses.create(
            model="gpt-6-luna",
            input=st.session_state.messages,
            stream=True
        )
        for event in stream:
            if event.type == "response.output_text.delta":
                yield event.delta

    with st.chat_message("assistant"):
        answer = st.write_stream(text_chunks())
    st.session_state.messages.append({"role": "assistant", "content": answer})
