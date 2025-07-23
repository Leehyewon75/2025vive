import streamlit as st
import time
import random
from datetime import date

st.set_page_config(page_title="공부 앱 - 미루지 말자!", layout="centered")

quotes = [
    "지금 하는 작은 노력이 내일의 큰 결과를 만든다.",
    "포기하지 마! 너는 할 수 있어 💪",
    "꾸준함은 천재를 이긴다.",
    "시작이 반이다. 지금 시작해!",
    "오늘의 노력은 내일의 나를 만든다."
]
st.markdown(f"### 🌟 {random.choice(quotes)}")

# ------------------- 상태 초기화 -------------------
if "focus_running" not in st.session_state:
    st.session_state.focus_running = False
    st.session_state.focus_paused = False
    st.session_state.focus_start = None
    st.session_state.focus_remaining = 25 * 60
    st.session_state.focus_total = 0
    st.session_state.focus_logged = False

if "break_running" not in st.session_state:
    st.session_state.break_running = False
    st.session_state.break_paused = False
    st.session_state.break_start = None
    st.session_state.break_remaining = 5 * 60
    st.session_state.break_total = 0
    st.session_state.break_logged = False

if "checklist" not in st.session_state:
    st.session_state.checklist = []

if "diary" not in st.session_state:
    st.session_state.diary = {}

# ------------------- 타이머 함수 -------------------
def start_focus():
    st.session_state.focus_start = time.time()
    st.session_state.focus_running = True
    st.session_state.focus_paused = False

def pause_focus():
    st.session_state.focus_running = False
    st.session_state.focus_paused = True

def reset_focus():
    st.session_state.focus_running = False
    st.session_state.focus_paused = False
    st.session_state.focus_remaining = 25 * 60
    st.session_state.focus_logged = False

def start_break():
    st.session_state.break_start = time.time()
    st.session_state.break_running = True
    st.session_state.break_paused = False

def pause_break():
    st.session_state.break_running = False
    st.session_state.break_paused = True

def reset_break():
    st.session_state.break_running = False
    st.session_state.break_paused = False
    st.session_state.break_remaining = 5 * 60
    st.session_state.break_logged = False

# ------------------- 집중 타이머 -------------------
st.markdown("---")
st.header("⏱️ 25분 집중 타이머")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("▶️ 집중 시작"):
        start_focus()
with col2:
    if st.button("⏸️ 집중 일시정지"):
        pause_focus()
with col3:
    if st.button("🔁 집중 초기화"):
        reset_focus()

# 타이머 계산
if st.session_state.focus_running:
    elapsed = int(time.time() - st.session_state.focus_start)
    st.session_state.focus_remaining = max(0, st.session_state.focus_remaining - elapsed)
    st.session_state.focus_start = time.time()  # 기준 시점 재설정

    if st.session_state.focus_remaining == 0 and not st.session_state.focus_logged:
        st.session_state.focus_total += 25 * 60
        st.session_state.focus_logged = True

mins, secs = divmod(st.session_state.focus_remaining, 60)
st.subheader(f"🕒 남은 집중 시간: {mins:02d}:{secs:02d}")

if st.session_state.focus_remaining == 0:
    st.success("🎉 집중 종료! 이제 휴식하세요.")

# ------------------- 휴식 타이머 -------------------
st.markdown("---")
st.header("🛌 5분 휴식 타이머")

col4, col5, col6 = st.columns(3)
with col4:
    if st.button("▶️ 휴식 시작"):
        start_break()
with col5:
    if st.button("⏸️ 휴식 일시정지"):
        pause_break()
with col6:
    if st.button("🔁 휴식 초기화"):
        reset_break()

# 휴식 계산
if st.session_state.break_running:
    elapsed = int(time.time() - st.session_state.break_start)
    st.session_state.break_remaining = max(0, st.session_state.break_remaining - elapsed)
    st.session_state.break_start = time.time()

    if st.session_state.break_remaining == 0 and not st.session_state.break_logged:
        st.session_state.break_total += 5 * 60
        st.session_state.break_logged = True

b_mins, b_secs = divmod(st.session_state.break_remaining, 60)
st.subheader(f"🕒 남은 휴식 시간: {b_mins:02d}:{b_secs:02d}")

if st.session_state.break_remaining == 0:
    st.info("☕ 휴식 끝! 다시 집중해봐요.")

# ------------------- 할 일 -------------------
st.markdown("---")
st.header("✅ 오늘의 할 일")

new_task = st.text_input("할 일을 입력하세요", key="new_task_input")
if st.button("추가"):
    if new_task:
        st.session_state.checklist.append({"text": new_task, "checked": False})
        st.session_state["new_task_input"] = ""

for i, task in enumerate(st.session_state.checklist):
    checked = st.checkbox(task["text"], value=task["checked"], key=f"task_{i}")
    st.session_state.checklist[i]["checked"] = checked

# ------------------- 일기 -------------------
st.markdown("---")
st.header("📓 오늘의 일기")

today = date.today().isoformat()
diary_text = st.text_area("오늘 하루를 기록해보세요", value=st.session_state.diary.get(today, ""), height=200)
if st.button("💾 일기 저장"):
    st.session_state.diary[today] = diary_text
    st.success("✅ 일기가 저장되었습니다!")

if st.session_state.diary.get(today):
    st.markdown("📖 **오늘 쓴 일기 미리 보기:**")
    st.info(st.session_state.diary[today])

# ------------------- 통계 -------------------
st.markdown("---")
st.header("📊 집중/휴식 누적 통계")

focus_min = st.session_state.focus_total // 60
break_min = st.session_state.break_total // 60

st.write(f"🧠 총 집중 시간: **{focus_min}분**")
st.write(f"☕ 총 휴식 시간: **{break_min}분**")

st.bar_chart({"시간(분)": [focus_min, break_min]})
