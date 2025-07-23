import streamlit as st
import random
from datetime import date

st.set_page_config(page_title="공부 기록 앱 - 미루지 말자!", layout="centered")

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

if "motivation" not in st.session_state:
    st.session_state.motivation = ""

# ------------------- 1. 할 일 목록 -------------------
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

# ------------------- 2. 목표 입력 -------------------
st.markdown("---")
st.header("🎯 오늘의 목표 집중 시간")

goal = st.number_input("오늘의 목표 집중 시간 (분)", min_value=0, max_value=1440, value=st.session_state.goal_minutes)
st.session_state.goal_minutes = goal
st.info(f"오늘의 목표: **{goal}분** 집중")

# ------------------- 3. 동기부여 -------------------
st.markdown("---")
st.header("💬 동기부여 한 마디")

quotes = [
    "시작이 반이다 💪",
    "5분만 해보자, 그다음은 생각하지 말자!",
    "완벽하지 않아도 괜찮아. 일단 시작!",
    "너는 해낼 수 있어. 작은 한 걸음부터!",
    "포기하지 마. 조금씩 앞으로 가자!",
    "느리더라도 맞게 가자",
    "천리길도 한 걸음부터",
    "늦었을 때가 진짜 늦었으니까 지금부터라도 하자",
    "후회하지 말자",
    "내 인생 아니라 너 인생",
    "문제 잘 풀어서 간Zㅣ나는 사람 되고 싶으신 분?"
]

if st.button("🎯 동기부여 듣기"):
    st.session_state.motivation = random.choice(quotes)

if st.session_state.motivation:
    st.success(f"🌟 {st.session_state.motivation}")

# ------------------- 4. 집중/휴식 시간 기록 -------------------
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

# ------------------- 5. 오늘의 일기 -------------------
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
