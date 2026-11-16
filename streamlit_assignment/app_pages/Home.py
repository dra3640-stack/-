import base64
import streamlit as st
from openai import OpenAI

st.title("🏠 Home")
st.write("질문에 대한 답변과 프롬프트 기반 이미지 생성을 할 수 있습니다.")

client = st.session_state.get("openai_client")
if client is None:
    st.warning("왼쪽 사이드바에 OpenAI API Key를 입력하세요.")
    st.stop()

@st.cache_data(show_spinner=False)
def cached_answer(prompt: str, api_key: str) -> str:
    # 같은 질문과 같은 API Key 조합은 캐시된 결과를 재사용합니다.
    cached_client = OpenAI(api_key=api_key)
    result = cached_client.responses.create(
        model="gpt-6-luna",
        input=prompt
    )
    return result.output_text

st.subheader("1. AI에게 질문하기")
question = st.text_area("질문을 입력하세요", placeholder="예: 인공지능을 쉽게 설명해줘")
if st.button("답변 받기", type="primary"):
    if not question.strip():
        st.error("질문을 입력하세요.")
    else:
        try:
            with st.spinner("답변을 생성하고 있습니다..."):
                answer = cached_answer(question.strip(), st.session_state["api_key"])
            st.markdown("### AI 답변")
            st.write(answer)
        except Exception as e:
            st.error(f"API 요청 중 오류가 발생했습니다: {e}")

st.divider()
st.subheader("2. 이미지 생성하기")
prompt = st.text_area("이미지 프롬프트", key="image_prompt",
                      placeholder="예: 별이 가득한 우주를 비행하는 미래형 우주선")
if st.button("이미지 생성", type="primary"):
    if not prompt.strip():
        st.error("이미지 프롬프트를 입력하세요.")
    else:
        try:
            with st.spinner("이미지를 생성하고 있습니다. 수십 초가 걸릴 수 있습니다..."):
                result = client.images.generate(
                    model="gpt-image-2.6-flare",
                    prompt=prompt.strip()
                )
                image_bytes = base64.b64decode(result.data[0].b64_json)
            st.image(image_bytes, caption="생성된 이미지", use_container_width=True)
        except Exception as e:
            st.error(f"이미지 생성 중 오류가 발생했습니다: {e}")
