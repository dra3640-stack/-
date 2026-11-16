import streamlit as st

st.title("📚 국립부경대학교 도서관 챗봇")
st.write("아래 도서관 규정 발췌 내용을 근거로 질문에 답변합니다.")

client = st.session_state.get("openai_client")
if client is None:
    st.warning("왼쪽 사이드바에 OpenAI API Key를 입력하세요.")
    st.stop()

# 국립부경대학교 공식 규정 및 도서관 안내에서 확인한 핵심 조항 발췌.
# 규정 전문은 학교 규정관리시스템에서 확인할 수 있습니다.
LIBRARY_RULES = """
국립부경대학교 도서관 규정 중 시설 및 자료 이용 관련 발췌

제18조(자격): 교직원 및 재학생, 관장의 허가를 받은 사람은 도서관 소장 자료와 시설을 이용할 수 있다.
제19조(개관 시간): 도서관의 개관 시간은 관장이 별도로 정한다.
제20조(휴관일): 자료실은 공휴일과 개교기념일에 휴관한다. 일반열람실은 설날과 추석에 휴관한다.
다만 관장은 필요에 따라 휴관일을 조정할 수 있다.
제21조(자료대출): 대출 자격이 있는 사람은 본인의 신분증으로 자료를 대출할 수 있다.
제22조(대출책수 및 기간): 단행본은 학부생 10책 이내 14일, 직원·조교·대학원생 20책 이내 30일,
전임교원·겸임교원·명예교수·강사 50책 이내 90일 대출할 수 있다.
전자책은 전 구성원 5책 이내이며 대출 기간은 5일이다.
제23조(대출 제한 자료): 연속간행물, 참고자료, 학위논문, 귀중자료, 비도서자료 및 관장이 지정한 자료는
원칙적으로 대출할 수 없다. 관장이 필요하다고 인정하면 단기간 대출을 허가할 수 있다.
제24조(대출기간 중 반납): 휴직, 퇴직, 정학, 퇴학, 제적, 수료, 졸업 등의 사유가 발생하거나
자료 운용상 관장이 요구하면 대출 자료를 즉시 반납해야 한다.
졸업 또는 수료 예정자는 학위수여일 30일 전부터 대출이 중지되고 대출 자료를 반납해야 한다.
제25조(관내수칙): 자료 훼손 및 무단 반출, 신분증 대여·무단 사용, 지정 장소 외 식음·흡연,
무단 게시물 부착, 물품 배포, 타인에게 방해가 되는 행위 등을 해서는 안 된다.

답변 원칙:
- 반드시 위 규정 내용에 근거하여 답한다.
- 규정에 없는 내용은 추측하지 말고 "제공된 규정 내용에서 확인할 수 없습니다"라고 답한다.
- 실제 운영시간이나 변경사항은 도서관 공지를 확인하도록 안내한다.
"""

if "library_messages" not in st.session_state:
    st.session_state.library_messages = []

def clear_library_chat():
    st.session_state.library_messages = []

st.button("Clear 대화", on_click=clear_library_chat)

for message in st.session_state.library_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("도서관 규정에 대해 질문하세요"):
    st.session_state.library_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    def text_chunks():
        stream = client.responses.create(
            model="gpt-6-luna",
            instructions=LIBRARY_RULES,
            input=st.session_state.library_messages,
            stream=True
        )
        for event in stream:
            if event.type == "response.output_text.delta":
                yield event.delta

    with st.chat_message("assistant"):
        answer = st.write_stream(text_chunks())
    st.session_state.library_messages.append({"role": "assistant", "content": answer})

with st.expander("챗봇에 입력한 규정 발췌 보기"):
    st.text(LIBRARY_RULES)
