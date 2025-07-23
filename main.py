import streamlit as st
import time
import random

st.set_page_config(page_title="오늘은 미루지 말자!", page_icon="⏳")

# 동기 부여 문구 리스트
motivations = [
    "시작이 반이다 💪",
    "5분만 해보자, 그다음은 생각하지 말자!",
    "완벽하지 않아도 괜찮아. 일단 시작!",
    "너는 해낼 수 있어. 작은 한 걸음부터!",
    "포기하지 마. 조금씩 앞으로 가자!"
]

# 세션 상태 초기화
if "tasks" not in st.session_state:
    st.session_state.tasks = []

st.title("⏳ 미루는 사람을 위한 오늘의 할 일 앱")

st.markdown("### 🎯 오늘의 목표를 입력하세요")

new_task = st.text_input("해야 할 일", placeholder="예: 리포트 작성하기")

if st.button("추가하기"):
    if new_task:
        st.session_state.tasks.append({"task": new_task, "done": False, "subtasks": []})
        st.success("할 일이 추가되었습니다!")
    else:
        st.warning("할 일을 입력해주세요.")

st.markdown("## 📋 해야 할 일 목록")

for i, item in enumerate(st.session_state.tasks):
    col1, col2 = st.columns([0.05, 0.95])
    with col1:
        checked = st.checkbox("", value=item["done"], key=f"task_{i}")
    with col2:
        st.write(f"**{item['task']}**")
    
    if checked:
        st.success(f"🎉 '{item['task']}' 완료! 잘했어요!")
        st.session_state.tasks[i]["done"] = True

    # Subtasks
    with st.expander("세부 작업 쪼개기"):
        subtask = st.text_input(f"세부 작업 입력 (할 일: {item['task']})", key=f"sub_{i}")
        if st.button("세부 작업 추가", key=f"sub_add_{i}"):
            if subtask:
                st.session_state.tasks[i]["subtasks"].append({"title": subtask, "done": False})
        for j, sub in enumerate(item["subtasks"]):
            sub_done = st.checkbox(sub["title"], value=sub["done"], key=f"subcheck_{i}_{j}")
            st.session_state.tasks[i]["subtasks"][j]["done"] = sub_done

# 포모도로 타이머
st.markdown("## ⏱ 집중 타이머 (25분)")

if st.button("포모도로 시작"):
    with st.empty():
        for minutes in range(25, 0, -1):
            for seconds in range(59, -1, -1):
                timer_text = f"{minutes:02d}:{seconds:02d}"
                st.markdown(f"### ⏳ 집중 중... {timer_text}")
                time.sleep(1)
        st.balloons()
        st.success("25분 집중 완료! 5분 휴식하세요 😊")

# 랜덤 동기부여
st.markdown("## 💡 오늘의 동기 부여")

if st.button("동기 부여 한마디"):
    st.info(random.choice(motivations))
