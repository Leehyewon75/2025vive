import streamlit as st
import random
from datetime import date

st.set_page_config(page_title="공부 기록 앱 - 미루지 말자!", layout="centered")

# ------------------- 동기부여 문구 -------------------
quotes = [
    "지금 하는 작은 노력이 내일의 큰 결과를 만든다.",
    "포기하지 마! 너는 할 수 있어 💪",
    "꾸준함은 천재를 이긴다.",
    "시작이 반이다. 지금 시작해!",
    "오늘의 노력은 내일의 나를 만든다."
]
st.markdown(f"### 🌟 {random.choice(quotes)}")

# ------------------- 세션 상태 초기화 -------------------
if "checklist" not in st.session_state:
    st.session_state.checklist = []

if "new_task_input_val" not in st.session_state:
    st.session_state.new_task_input_val = ""

if "diary" not in st.session_state:
    st.session_state.diary = {}

if "goal_minutes" not in st.session_state:
    st.session_state.goal_minutes = 0

if "focus_log" not in st.session_state:
    st.session_state.focus_log = []

if "break_log" not in st.session_state:
    st.session_state.break_log = []

# ------------------- 오늘의 목표 입력 -------------------
st.markdown("---")
st.header("🎯 오늘의 목표 집중 시간")

goal = st.number_input("오늘의 목표 집중 시간 (분)", min_value=0, max_value=1440, value=st.session_state.goal_minutes)
st.session_state.goal_minutes = goal
st.success(f"오늘의 목표: {goal}분 집중")

# ------------------- 할 일 목록 -------------------
st.markdown("---")
st.header("✅ 오늘의 할 일")

new_task = st.text_input("할 일을 입력하세요", value=st.session_state.new_task_input_val)
if st.button("추가"):
    if new_task.strip():
        st.session_state.checklist.append({"text": new_task.strip(), "checked": False})
        st.session_state.new_task_input_val = ""

for i, item in enumerate(st.session_state.checklist):
    key = f"task_{i}"
    checked = st.checkbox(item["text"], value=item["checked"], key=key)
    st.session_state.checklist[i]["checked"] = checked

# ------------------- 오늘의 일기 -------------------
st.markdown("---")
st.header("📓 오늘의 일기")

today = date.today().isoformat()
diary_text = st.text_area("오늘 하루를 기록해보세요", value=st.session_state.diary.get(today, ""), height=200)

if st.button("💾 일기 저장"):
    st.session_state.diary[today] = diary_text
    st.success("✅ 오늘의 일기가 저장되었습니다!")

if today in st.session_state.diary:
    st.markdown("📖 **오늘 쓴 일기 미리 보기:**")
    st.info(st.session_state.diary[today])

# ------------------- 집중/휴식 기록 -------------------
st.markdown("---")
st.header("🧠 집중 / ☕ 휴식 시간 기록")

with st.form("time_log_form"):
    focus = st.number_input("오늘 추가한 집중 시간 (분)", min_value=0, step=1)
    rest = st.number_input("오늘 추가한 휴식 시간 (분)", min_value=0, step=1)
    submitted = st.form_submit_button("기록하기")

    if submitted:
        if focus > 0:
            st.session_state.focus_log.append(focus)
        if rest > 0:
            st.session_state.break_log.append(rest)
        st.success("⏱ 시간이 기록되었습니다!")

# ------------------- 통계 -------------------
st.markdown("---")
st.header("📊 집중/휴식 누적 통계")

total_focus = sum(st.session_state.focus_log)
total_break = sum(st.session_state.break_log)

progress = min(100, int((total_focus / st.session_state.goal_minutes) * 100)) if st.session_state.goal_minutes > 0 else 0
st.progress(progress / 100)

st.write(f"🧠 총 집중 시간: **{total_focus}분**")
st.write(f"☕ 총 휴식 시간: **{total_break}분**")
st.write(f"🎯 목표 달성률: **{progress}%**")

st.bar_chart({"집중": [total_focus], "휴식": [total_break]})
