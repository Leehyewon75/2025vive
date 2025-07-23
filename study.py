import streamlit as st
import time
import random
from datetime import date

st.set_page_config(page_title="공부 앱 - 미루지 말자!", layout="centered")

# 🌟 동기부여 문구
quotes = [
    "지금 하는 작은 노력이 내일의 큰 결과를 만든다.",
    "포기하지 마! 너는 할 수 있어 💪",
    "꾸준함은 천재를 이긴다.",
    "시작이 반이다. 지금 시작해!",
    "오늘의 노력은 내일의 나를 만든다."
]
st.markdown(f"### 🌟 {random.choice(quotes)}")

# ---------------- 세션 상태 초기화 ----------------
if "focus_running" not in st.session_state:
    st.session_state.focus_running = False
    st.session_state.focus_remaining = 25 * 60
    st.session_state.focus_last_update = time.time()
    st.session_state.focus_total = 0
    st.session_state.focus_logged = False

if "break_running" not in st.session_state:
    st.session_state.break_running = False
    st.session_state.break_remaining = 5 * 60
    st.session_state.break_last_update = time.time()
    st.session_state.break_total = 0
    st.session_state.break_logged = False

if "checklist" not in st.session_state:
    st.session_state.checklist = []

if "diary" not in st.session_state:
    st.session_state.diary = {}

if "new_task_input_val" not in st.session_state:
    st.session_state.new_task_input_val = ""

# ---------------- 타이머 갱신 ----------------
def update_timer(timer_type):
    now = time.time()
    if timer_type == "focus" and st.session_state.focus_running:
        delta = now - st.session_state.focus_last_update
        st.session_state.focus_remaining = max(0, st.session_state.focus_remaining - int(delta))
        st.session_state.focus_last_update = now
        if st.session_state.focus_remaining == 0 and not st.session_state.focus_logged:
            st.session_state.focus_total += 25 * 60
            st.session_state.focus_logged = True
    elif timer_type == "break" and st.session_state.break_running:
        delta = now - st.session_state.break_last_update
        st.session_state.break_remaining = max(0, st.session_state.break_remaining - int(delta))
        st.session_state.break_last_update = now
        if st.session_state.break_remaining == 0 and not st.session_state.break_logged:
            st.session_state.break_total += 5 * 60
            st.session_state.break_logged = True

# ---------------- 집중 타이머 ----------------
st.markdown("## ⏱️ 25분 집중 타이머")
focus_col1, focus_col2, focus_col3 = st.columns(3)
with focus_col1:
    if st.button("▶️ 시작", key="focus_start"):
        st.session_state.focus_running = True
        st.session_state.focus_last_update = time.time()
with focus_col2:
    if st.button("⏸️ 일시정지", key="focus_pause"):
        st.session_state.focus_running = False
with focus_col3:
    if st.button("🔁 초기화", key="focus_reset"):
        st.session_state.focus_running = False
        st.session_state.focus_remaining = 25 * 60
        st.session_state.focus_logged = False

update_timer("focus")
fmin, fsec = divmod(st.session_state.focus_remaining, 60)
st.subheader(f"🕒 남은 집중 시간: {fmin:02d}:{fsec:02d}")
if st.session_state.focus_remaining == 0:
    st.success("🎉 집중 시간 종료! 휴식하세요.")

# ---------------- 휴식 타이머 ----------------
st.markdown("---")
st.markdown("## 🛌 5분 휴식 타이머")
break_col1, break_col2, break_col3 = st.columns(3)
with break_col1:
    if st.button("▶️ 시작", key="break_start"):
        st.session_state.break_running = True
        st.session_state.break_last_update = time.time()
with break_col2:
    if st.button("⏸️ 일시정지", key="break_pause"):
        st.session_state.break_running = False
with break_col3:
    if st.button("🔁 초기화", key="break_reset"):
        st.session_state.break_running = False
        st.session_state.break_remaining = 5 * 60
        st.session_state.break_logged = False

update_timer("break")
bmin, bsec = divmod(st.session_state.break_remaining, 60)
st.subheader(f"🕒 남은 휴식 시간: {bmin:02d}:{bsec:02d}")
if st.session_state.break_remaining == 0:
    st.info("☕ 휴식 끝! 다시 집중해볼까요?")

# ---------------- 오늘의 할 일 ----------------
st.markdown("---")
st.header("✅ 오늘의 할 일")

new_task = st.text_input("할 일을 입력하세요", value=st.session_state.new_task_input_val)
if st.button("추가"):
    if new_task.strip():
        st.session_state.checklist.append({"text": new_task.strip(), "checked": False})
        st.session_state.new_task_input_val = ""

for i, item in enumerate(st.session_state.checklist):
    checked = st.checkbox(item["text"], value=item["checked"], key=f"task_{i}")
    st.session_state.checklist[i]["checked"] = checked

# ---------------- 오늘의 일기 ----------------
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

# ---------------- 통계 ----------------
st.markdown("---")
st.header("📊 집중/휴식 누적 통계")

focus_min = st.session_state.focus_total // 60
break_min = st.session_state.break_total // 60

st.write(f"🧠 총 집중 시간: **{focus_min}분**")
st.write(f"☕ 총 휴식 시간: **{break_min}분**")

st.bar_chart({"집중": [focus_min], "휴식": [break_min]})
