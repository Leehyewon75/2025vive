import streamlit as st
import time
import random
from datetime import date

# 기본 설정
st.set_page_config(page_title="공부 앱 - 미루지 말자!", layout="centered")

# 동기부여 문구
quotes = [
    "지금 하는 작은 노력이 내일의 큰 결과를 만든다.",
    "포기하지 마! 너는 할 수 있어 💪",
    "꾸준함은 천재를 이긴다.",
    "시작이 반이다. 지금 시작해!",
    "오늘의 노력은 내일의 나를 만든다."
]
st.markdown(f"### 🌟 {random.choice(quotes)}")

# 세션 상태 초기화
def init_state():
    keys_defaults = {
        "focus_running": False,
        "focus_paused": False,
        "focus_start": None,
        "focus_remaining": 25 * 60,
        "focus_total": 0,
        "focus_logged": False,
        "break_running": False,
        "break_paused": False,
        "break_start": None,
        "break_remaining": 5 * 60,
        "break_total": 0,
        "break_logged": False,
        "checklist": [],
        "diary": {},
    }
    for k, v in keys_defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ---------------- 집중 타이머 ----------------
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

if st.session_state.focus_running:
    elapsed = int(time.time() - st.session_state.focus_start)
    st.session_state.focus_remaining = max(0, st.session_state.focus_remaining - elapsed)
    st.session_state.focus_start = time.time()
    if st.session_state.focus_remaining == 0 and not st.session_state.focus_logged:
        st.session_state.focus_total += 25 * 60
        st.session_state.focus_logged = True

st.markdown("---")
st.header("⏱️ 25분 집중 타이머")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("▶️ 집중 시작"):
        start_focus()
with c2:
    if st.button("⏸️ 일시정지"):
        pause_focus()
with c3:
    if st.button("🔁 초기화"):
        reset_focus()

fmin, fsec = divmod(st.session_state.focus_remaining, 60)
st.subheader(f"🕒 남은 집중 시간: {fmin:02d}:{fsec:02d}")
if st.session_state.focus_remaining == 0:
    st.success("🎉 집중 시간 종료! 이제 휴식하세요.")

# ---------------- 휴식 타이머 ----------------
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

if st.session_state.break_running:
    elapsed = int(time.time() - st.session_state.break_start)
    st.session_state.break_remaining = max(0, st.session_state.break_remaining - elapsed)
    st.session_state.break_start = time.time()
    if st.session_state.break_remaining == 0 and not st.session_state.break_logged:
        st.session_state.break_total += 5 * 60
        st.session_state.break_logged = True

st.markdown("---")
st.header("🛌 5분 휴식 타이머")
c4, c5, c6 = st.columns(3)
with c4:
    if st.button("▶️ 휴식 시작"):
        start_break()
with c5:
    if st.button("⏸️ 일시정지", key="break_pause"):
        pause_break()
with c6:
    if st.button("🔁 초기화", key="break_reset"):
        reset_break()

bmin, bsec = divmod(st.session_state.break_remaining, 60)
st.subheader(f"🕒 남은 휴식 시간: {bmin:02d}:{bsec:02d}")
if st.session_state.break_remaining == 0:
    st.info("☕ 휴식 끝! 다시 집중해봐요.")

# ---------------- To-Do 리스트 ----------------
st.markdown("---")
st.header("✅ 오늘의 할 일")

new_task = st.text_input("할 일을 입력하세요", key="new_task_input")
if st.button("추가"):
    if new_task:
        st.session_state.checklist.append({"text": new_task, "checked": False})
        st.experimental_rerun()

for i, task in enumerate(st.session_state.checklist):
    checked = st.checkbox(task["text"], value=task["checked"], key=f"task_{i}")
    st.session_state.checklist[i]["checked"] = checked

# ---------------- 일기 ----------------
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

# ---------------- 통계 ----------------
st.markdown("---")
st.header("📊 집중/휴식 누적 통계")

focus_min = st.session_state.focus_total // 60
break_min = st.session_state.break_total // 60

st.write(f"🧠 총 집중 시간: **{focus_min}분**")
st.write(f"☕ 총 휴식 시간: **{break_min}분**")

st.bar_chart({"시간(분)": [focus_min, break_min]})
