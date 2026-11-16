import streamlit as st

st.title("📄 ChatPDF")
st.write("PDF를 업로드하고 해당 문서의 내용에 관해 질문할 수 있습니다.")

client = st.session_state.get("openai_client")
if client is None:
    st.warning("왼쪽 사이드바에 OpenAI API Key를 입력하세요.")
    st.stop()

if "pdf_vector_store_id" not in st.session_state:
    st.session_state.pdf_vector_store_id = None
if "pdf_file_name" not in st.session_state:
    st.session_state.pdf_file_name = None
if "pdf_messages" not in st.session_state:
    st.session_state.pdf_messages = []

def clear_pdf_chat():
    st.session_state.pdf_messages = []

def leave_pdf():
    vector_id = st.session_state.get("pdf_vector_store_id")
    if vector_id:
        try:
            client.vector_stores.delete(vector_store_id=vector_id)
        except Exception as e:
            st.session_state["pdf_delete_error"] = str(e)
    st.session_state.pdf_vector_store_id = None
    st.session_state.pdf_file_name = None
    st.session_state.pdf_messages = []

col1, col2 = st.columns(2)
with col1:
    st.button("Clear 대화", on_click=clear_pdf_chat)
with col2:
    st.button("Leave (벡터 스토어 삭제)", on_click=leave_pdf)

if st.session_state.pdf_vector_store_id is None:
    uploaded = st.file_uploader("질문할 PDF 파일 하나를 업로드하세요", type=["pdf"])
    if uploaded is not None:
        if st.button("PDF 등록 및 검색 준비", type="primary"):
            try:
                with st.spinner("PDF를 업로드하고 검색용 Vector Store를 만들고 있습니다..."):
                    vector_store = client.vector_stores.create(
                        name=f"chatpdf-{uploaded.name}"
                    )
                    uploaded.seek(0)
                    file_obj = client.files.create(
                        file=(uploaded.name, uploaded.getvalue()),
                        purpose="assistants"
                    )
                    client.vector_stores.files.create(
                        vector_store_id=vector_store.id,
                        file_id=file_obj.id
                    )
                    st.session_state.pdf_vector_store_id = vector_store.id
                    st.session_state.pdf_file_name = uploaded.name
                st.success("PDF 등록이 완료되었습니다. 이제 질문할 수 있습니다.")
                st.rerun()
            except Exception as e:
                st.error(f"PDF 등록 중 오류가 발생했습니다: {e}")
else:
    st.success(f"현재 문서: {st.session_state.pdf_file_name}")
    for message in st.session_state.pdf_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("PDF 내용에 관해 질문하세요"):
        st.session_state.pdf_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        def text_chunks():
            stream = client.responses.create(
                model="gpt-6-luna",
                input=st.session_state.pdf_messages,
                tools=[{
                    "type": "file_search",
                    "vector_store_ids": [st.session_state.pdf_vector_store_id]
                }],
                stream=True
            )
            for event in stream:
                if event.type == "response.output_text.delta":
                    yield event.delta

        with st.chat_message("assistant"):
            answer = st.write_stream(text_chunks())
        st.session_state.pdf_messages.append({"role": "assistant", "content": answer})
