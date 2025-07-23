import streamlit as st
import time
from datetime import datetime, date

st.set_page_config(page_title="공부 앱", layout="centered")

# -------------------- 세션 상태 초기화 --------------------
if "focus_start_time" not in st.session_state:
    st.session_state.focus_start_time = None
if "focus_running" not in st.session_state:
    st.session_state.focus_running = False
if "focus_remaining" not in st.session_state:
    st.session_state.focus_remaining = 25 * 60

if "break_start_time" not in st.session_state:
    st.session_state.break_start_time = None
if "break_running" not in st.session_state:
    st.session_state.break_running = False
if "break_remaining" not in st.session_state:
    st.session_state.break_remaining = 5 * 60

if "checklist" not in st.session_state:
    st.session_state.checklist = []

if "diary" not in st.session_state:
    st.session_state.diary = {}

# -------------------- 타이머 함수들 --------------------
def start_focus_timer():
    if not st.session_state.focus_running:
        st.session_state.focus_start_time = time.time()
        st.session_state.focus_running = True

def reset_focus_timer():
    st.session_state.focus_running = False
    st.session_state.focus_remaining = 25 * 60

def start_break_timer():
    if not st.session_state.break_running:
        st.session_state.break_start_time = time.time()
        st.session_state.break_running = True

def reset_break_timer():
    st.session_state.break_running = False
    st.session_state.break_remaining = 5 * 60

# -------------------- UI --------------------
st.title("📚 공부 앱 - 미루지 말자!")

st.header("⏱️ 집중 타이머 (25분)")
col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ 집중 시작"):
        start_focus_timer()
with col2:
    if st.button("🔁 집중 초기화"):
        reset_focus_timer()

if st.session_state.focus_running:
    elapsed = int(time.time() - st.session_state.focus_start_time)
    st.session_state.focus_remaining = max(0, 25 * 60 - elapsed)

mins, secs = divmod(st.session_state.focus_remaining, 60)
st.subheader(f"🕒 집중 시간 남음: {mins:02d}:{secs:02d}")

if st.session_state.focus_remaining == 0:
    st.success("🎉 집중 시간 끝! 휴식을 시작하세요.")

st.markdown("---")

st.header("🛌 휴식 타이머 (5분)")
col3, col4 = st.columns(2)
with col3:
    if st.button("▶️ 휴식 시작"):
        start_break_timer()
with col4:
    if st.button("🔁 휴식 초기화"):
        reset_break_timer()

if st.session_state.break_running:
    elapsed = int(time.time() - st.session_state.break_start_time)
    st.session_state.break_remaining = max(0, 5 * 60 - elapsed)

b_mins, b_secs = divmod(st.session_state.break_remaining, 60)
st.subheader(f"🕒 휴식 시간 남음: {b_mins:02d}:{b_secs:02d}")

if st.session_state.break_remaining == 0:
    st.info("☕ 휴식 끝! 다시 집중해볼까요?")

st.markdown("---")

# -------------------- 할 일 리스트 --------------------
st.header("✅ 오늘의 할 일")
new_task = st.text_input("할 일을 입력하세요", key="new_task_input")
if st.button("추가"):
    if new_task:
        st.session_state.checklist.append({"text": new_task, "checked": False})
       st.session_state["new_task_input"] = ""  # 입력창 초기화 효과
for i, item in enumerate(st.session_state.checklist):
    checked = st.checkbox(item["text"], value=item["checked"], key=f"task_{i}")
    st.session_state.checklist[i]["checked"] = checked

# -------------------- 일기 작성 --------------------
st.markdown("---")
st.header("📓 오늘의 일기")
today = date.today().isoformat()
diary_text = st.text_area("오늘 하루를 돌아보며 작성해보세요", value=st.session_state.diary.get(today, ""), height=200)

if st.button("💾 일기 저장"):
    st.session_state.diary[today] = diary_text
    st.success("✅ 일기가 저장되었습니다!")

if st.session_state.diary.get(today):
    st.markdown("🗒️ **오늘 작성한 일기 미리 보기:**")
    st.info(st.session_state.diary[today])

