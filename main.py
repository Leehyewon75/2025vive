import streamlit as st
import time
import random
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="미루지 말자 앱", layout="centered")

# 세션 상태 초기화
if "users" not in st.session_state:
    st.session_state.users = {}  # 사용자 이름별 할 일 관리
if "focus_logs" not in st.session_state:
    st.session_state.focus_logs = []  # 집중 시간 로그
if "motivations" not in st.session_state:
    st.session_state.motivations = [
        "시작이 반이다 💪",
        "5분만 해보자, 그다음은 생각하지 말자!",
        "작은 한 걸음이 큰 변화를 만든다.",
        "너는 할 수 있어! 지금 시작해!",
        "포기하지 마. 조금씩 앞으로 나아가자!"
    ]

st.title("⏳ 미루는 사람을 위한 습관 앱")

# 사용자 이름 입력
st.sidebar.title("👤 사용자")
username = st.sidebar.text_input("이름을 입력하세요", value="me")

if username not in st.session_state.users:
    st.session_state.users[username] = {
        "tasks": [],
        "focus_time": 0
    }

# 할 일 추가
st.header("📌 오늘의 할 일 추가")
task_input = st.text_input("할 일 입력", placeholder="예: 발표 자료 만들기")
if st.button("➕ 추가"):
    if task_input:
        st.session_state.users[username]["tasks"].append({"title": task_input, "done": False})
        st.success("할 일이 추가되었습니다!")

# 할 일 목록
st.subheader(f"📋 {username}의 할 일 목록")
for i, task in enumerate(st.session_state.users[username]["tasks"]):
    checked = st.checkbox(task["title"], value=task["done"], key=f"{username}_{i}")
    st.session_state.users[username]["tasks"][i]["done"] = checked

# 타이머 설정
st.header("⏱ 집중 타이머")
focus_duration = st.slider("집중 시간 선택 (분)", 5, 120, 25)
if st.button("🚀 타이머 시작"):
    st.success(f"{focus_duration}분 집중 시작!")
    with st.empty():
        for m in range(focus_duration, 0, -1):
            for s in range(59, -1, -1):
                st.markdown(f"### ⏳ 집중 중... {m:02d}:{s:02d}")
                time.sleep(1)
    st.balloons()
    st.success(f"{focus_duration}분 완료! 잘했어요 🎉")
    st.session_state.users[username]["focus_time"] += focus_duration
    st.session_state.focus_logs.append({"user": username, "minutes": focus_duration})

# 동기부여
st.header("💡 동기 부여 한 마디")
if st.button("힘을 주세요!"):
    st.info(random.choice(st.session_state.motivations))

# 통계 시각화
st.header("📊 성과 통계 차트")

# 완료된 작업 수
user_data = st.session_state.users[username]
completed = sum(1 for t in user_data["tasks"] if t["done"])
total = len(user_data["tasks"])
st.write(f"✅ 완료한 할 일: {completed} / {total}")
st.progress(completed / total if total > 0 else 0)

# 집중 시간 시각화
if st.session_state.focus_logs:
    df_logs = pd.DataFrame(st.session_state.focus_logs)
    focus_by_user = df_logs.groupby("user")["minutes"].sum().sort_values(ascending=False)

    st.subheader("🏆 집중 시간 랭킹")
    st.bar_chart(focus_by_user)

# 친구와 비교
st.header("👥 친구와 할 일 비교")
usernames = list(st.session_state.users.keys())
if len(usernames) > 1:
    compare_user = st.selectbox("비교할 친구를 선택하세요", [u for u in usernames if u != username])
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**📋 {username}의 할 일**")
        for task in st.session_state.users[username]["tasks"]:
            status = "✅" if task["done"] else "❌"
            st.write(f"{status} {task['title']}")
    with col2:
        st.markdown(f"**📋 {compare_user}의 할 일**")
        for task in st.session_state.users[compare_user]["tasks"]:
            status = "✅" if task["done"] else "❌"
            st.write(f"{status} {task['title']}")
else:
    st.info("비교하려면 최소 2명의 사용자가 필요합니다. 사이드바에서 이름을 바꿔 추가해보세요.")
pip install matplotlib
streamlit
matplotlib
pandas
