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
import streamlit as st

st.set_page_config(page_title="체크리스트 앱", page_icon="✅", layout="centered")

# 세션 상태 초기화
if "checklist" not in st.session_state:
    st.session_state.checklist = []

st.title("✅ 나만의 체크리스트")

# 항목 추가
with st.form(key="add_item"):
    new_item = st.text_input("새 항목 추가", placeholder="예: 책 읽기")
    submitted = st.form_submit_button("➕ 추가하기")
    if submitted and new_item.strip():
        st.session_state.checklist.append({"text": new_item, "checked": False})
        st.success("항목이 추가되었습니다!")

# 체크리스트 표시
st.markdown("## 📋 체크리스트")
if not st.session_state.checklist:
    st.info("아직 체크리스트 항목이 없습니다.")
else:
    for i, item in enumerate(st.session_state.checklist):
        col1, col2 = st.columns([0.1, 0.9])
        with col1:
            checked = st.checkbox("", value=item["checked"], key=f"item_{i}")
        with col2:
            if checked:
                st.markdown(f"~~{item['text']}~~")
            else:
                st.write(item["text"])
        st.session_state.checklist[i]["checked"] = checked

# 완료된 항목 수 요약
total = len(st.session_state.checklist)
completed = sum(1 for item in st.session_state.checklist if item["checked"])
if total:
    st.markdown(f"**🎉 완료된 항목: {completed} / {total}**")
    st.progress(completed / total)
import streamlit as st
import random

st.set_page_config(page_title="체크리스트 + 보상 시스템", page_icon="🎁", layout="centered")

# 세션 상태 초기화
if "checklist" not in st.session_state:
    st.session_state.checklist = []
if "rewards" not in st.session_state:
    st.session_state.rewards = []
if "reward_drawn" not in st.session_state:
    st.session_state.reward_drawn = None

st.title("✅ 오늘의 체크리스트 & 🎁 보상 받기")

# -----------------------
# 체크리스트 추가
# -----------------------
st.header("📋 오늘의 할 일")
with st.form(key="add_task"):
    task_input = st.text_input("할 일 입력", placeholder="예: 운동 30분 하기")
    submit_task = st.form_submit_button("➕ 추가")
    if submit_task and task_input.strip():
        st.session_state.checklist.append({"text": task_input, "checked": False})
        st.success("할 일이 추가되었습니다!")

# 체크리스트 표시
if st.session_state.checklist:
    for i, item in enumerate(st.session_state.checklist):
        checked = st.checkbox(item["text"], value=item["checked"], key=f"task_{i}")
        st.session_state.checklist[i]["checked"] = checked

    # 완료 요약
    total = len(st.session_state.checklist)
    completed = sum(1 for item in st.session_state.checklist if item["checked"])
    st.markdown(f"**진행 상황: {completed} / {total} 완료됨**")
    st.progress(completed / total if total > 0 else 0)

else:
    st.info("아직 등록된 할 일이 없습니다.")

# -----------------------
# 보상 목록 입력
# -----------------------
st.header("🎁 내가 좋아하는 보상 리스트")
with st.form(key="add_reward"):
    new_reward = st.text_input("보상 추가", placeholder="예: 치킨 먹기, 영화 보기 등")
    submit_reward = st.form_submit_button("✨ 보상 추가")
    if submit_reward and new_reward.strip():
        st.session_state.rewards.append(new_reward)
        st.success("보상이 추가되었습니다!")

if st.session_state.rewards:
    st.markdown("현재 등록된 보상:")
    for r in st.session_state.rewards:
        st.write(f"🍬 {r}")
else:
    st.info("보상 항목을 추가해보세요!")

# -----------------------
# 보상 랜덤 추첨
# -----------------------
st.header("🏆 계획을 지켰다면, 보상을 뽑아보세요!")

if completed == total and total > 0:
    if st.button("🎲 보상 뽑기"):
        if st.session_state.rewards:
            st.session_state.reward_drawn = random.choice(st.session_state.rewards)
        else:
            st.warning("보상 리스트가 비어 있습니다!")
else:
    st.info("체크리스트를 모두 완료하면 보상을 뽑을 수 있어요!")

# 뽑은 보상 표시
if st.session_state.reward_drawn:
    st.success(f"🎉 오늘의 보상은... **{st.session_state.reward_drawn}** 입니다!")
