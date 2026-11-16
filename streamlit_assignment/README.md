# Streamlit 생성 AI 응용 프로그래밍 과제

## 파일 구성
- `streamlit_app.py`: 앱 진입점, 사이드바 API Key, 페이지 내비게이션
- `app_pages/Home.py`: Responses API 질문/답변 및 이미지 생성
- `app_pages/Chat.py`: 대화 기억 및 스트리밍 챗봇
- `app_pages/Chatbot.py`: 국립부경대학교 도서관 규정 챗봇
- `app_pages/ChatPDF.py`: PDF 업로드, Vector Store, File Search 챗봇
- `requirements.txt`: 실행 패키지

## GitHub Codespaces에서 실행
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## GitHub에 올리기
```bash
git add .
git commit -m "Complete Streamlit AI assignment"
git push
```

## Streamlit Community Cloud 배포
1. https://share.streamlit.io 에 접속
2. Create app 선택
3. GitHub 저장소와 브랜치 선택
4. Main file path를 `streamlit_app.py`로 지정
5. Deploy 클릭
6. 배포된 페이지의 사이드바에 OpenAI API Key 입력

## 주의
- API Key를 코드, README, GitHub에 입력하지 마세요.
- 강의자료에 지정된 모델 이름(`gpt-6-luna`, `gpt-image-2.6-flare`)을 코드에 반영했습니다.
- 계정에서 해당 모델을 사용할 수 없다는 오류가 나면 강의에서 안내한 실제 사용 가능 모델명을 확인한 뒤 코드의 모델명을 바꾸세요.
- 도서관 챗봇의 규정은 공식 규정에서 과제 질문에 필요한 주요 조항을 발췌해 넣었습니다. 제출 전 학교 규정관리시스템의 최신 전문과 대조하고 필요하면 `LIBRARY_RULES`에 전문을 추가하세요.
