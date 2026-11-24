import streamlit as st
from datetime import datetime
st.set_page_config(page_title="오늘 뭐 먹지?",page_icon="🍚",layout="wide")
st.title("🍚 오늘 뭐 먹지?")
st.caption("대학생을 위한 상황 맞춤 식사 추천")
st.info("식당·가격·대기시간·학식 메뉴는 시연용 예시 데이터입니다. 실제 실시간 정보가 아닙니다.")
restaurants=[
{"name":"캠퍼스 한식집","kind":"한식","price":7500,"walk":12,"solo":True,"wait":8,"desc":"백반·찌개 중심의 빠른 한 끼"},
{"name":"오늘의 국수","kind":"면요리","price":6500,"walk":8,"solo":True,"wait":3,"desc":"국수와 간단한 면 메뉴"},
{"name":"학생 덮밥","kind":"덮밥","price":8000,"walk":10,"solo":True,"wait":18,"desc":"덮밥·돈까스 등 단품 메뉴"},
{"name":"분식 스테이션","kind":"분식","price":5500,"walk":7,"solo":True,"wait":7,"desc":"김밥·떡볶이·라면"},
{"name":"친구들 식당","kind":"한식","price":9000,"walk":15,"solo":False,"wait":10,"desc":"친구들과 먹기 좋은 메뉴"},
{"name":"샐러드 키친","kind":"샐러드","price":8500,"walk":9,"solo":True,"wait":4,"desc":"샐러드와 가벼운 식사"}]
if "reports" not in st.session_state: st.session_state.reports=[]
st.header("1. 원클릭 상황 추천")
cols=st.columns(4)
for col,(label,key) in zip(cols,[("⏰ 공강 50분","gap"),("💰 8,000원 이하","budget"),("🧍 혼밥 가능","solo"),("⚡ 빠른 식사","quick")]):
    if col.button(label,use_container_width=True): st.session_state.scenario=key
scenario=st.session_state.get("scenario")
if scenario:
    filtered=restaurants[:]
    if scenario=="gap": filtered=[r for r in filtered if r["walk"]+r["wait"]<=50]
    elif scenario=="budget": filtered=[r for r in filtered if r["price"]<=8000]
    elif scenario=="solo": filtered=[r for r in filtered if r["solo"]]
    elif scenario=="quick": filtered=[r for r in filtered if r["walk"]+r["wait"]<=25]
    filtered=sorted(filtered,key=lambda r:r["walk"]+r["wait"])[:3]
    st.subheader("추천 식당 3곳")
    for n,r in enumerate(filtered,1):
        with st.container(border=True):
            st.markdown(f"### {n}. {r['name']} · {r['kind']}")
            a,b,c=st.columns(3); a.metric("가격",f"{r['price']:,}원"); b.metric("이동(예시)",f"{r['walk']}분"); c.metric("대기(예시)",f"{r['wait']}분")
            st.write(r["desc"]); st.write("혼밥 가능" if r["solo"] else "혼밥 정보 없음")
st.divider()
st.header("2. 점심 혼잡도 제보")
st.caption("제보는 이 세션에서만 저장되는 시연 기능입니다.")
with st.form("report"):
    place=st.selectbox("식당", [r["name"] for r in restaurants])
    level=st.radio("혼잡도",["여유","보통","혼잡"],horizontal=True)
    wait=st.number_input("예상 대기시간(분)",0,120,5,step=5)
    note=st.text_input("추가 설명(선택)")
    if st.form_submit_button("제보하기"):
        st.session_state.reports.insert(0,{"place":place,"level":level,"wait":wait,"note":note,"time":datetime.now().strftime("%H:%M")})
        st.success("제보 등록!")
if st.session_state.reports:
    for x in st.session_state.reports[:10]: st.write(f"**{x['place']}** · {x['level']} · 대기 {x['wait']}분 · {x['time']} · {x['note']}")
else: st.write("제보가 아직 없습니다.")
st.divider()
st.header("3. 교내 학식 메뉴 비교")
menus=[("학생식당","오늘의 백반",5500),("학생식당","돈까스 정식",6500),("교내 식당","비빔밥",6000)]
st.caption("아래 메뉴는 데모 데이터입니다.")
for p,m,v in menus:
    with st.container(border=True):
        c1,c2=st.columns([3,1]); c1.write(f"**{p} — {m}**"); c2.markdown(f"### {v:,}원")
st.divider()
st.header("4. 세부 조건 검색")
budget=st.slider("예산",3000,15000,8000,500); travel=st.slider("최대 이동시간",5,30,15); solo=st.checkbox("혼밥 가능한 곳")
if st.button("세부 조건으로 검색"):
    candidates=[r for r in restaurants if r["price"]<=budget and r["walk"]<=travel and (not solo or r["solo"])]
    for r in sorted(candidates,key=lambda x:x["walk"]+x["wait"])[:3]: st.write(f"- **{r['name']}** · {r['price']:,}원 · 이동 {r['walk']}분 · 대기(예시) {r['wait']}분")
    if not candidates: st.warning("조건에 맞는 예시 식당이 없습니다.")
st.sidebar.title("앱 소개")
st.sidebar.write("태그 버튼으로 식당 후보를 압축하고 혼잡도 제보와 학식 메뉴를 비교합니다.")
st.sidebar.caption("실시간 정보와 여러 사용자 공유 기능은 DB/API 연동이 필요한 후속 개발 기능입니다.")
