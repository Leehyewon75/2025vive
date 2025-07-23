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

# ---------------- 세션 상태 초기화 ----------------
if "focus_running" not in st.session_state:
    st.session_state.focus_running = False
    st.session_state.focus_remaining = 25 * 60
    st.session_state.focus_last_update = time.time()

if "break_running" not in st.session_state:
    st.session_state.break_running = False
    st.session_state.break_remaining = 5 * 60
    st.session_state.break_last_update = time.time()

# ---------------- 타이머 로직 (업데이트용) ----------------
def update_timer(timer_type):
    now = time.time()
    if timer_type == "focus" and st.session_state.focus_running:
        delta = now - st.session_state.focus_last_update
        st.session_state.focus_remaining = max(0, st.session_state.focus_remaining - int(delta))
        st.session_state.focus_last_update = now
    elif timer_type == "break" and st.session_state.break_running:
        delta = now - st.session_state.break_last_update
        st.session_state.break_remaining = max(0, st.session_state.break_remaining - int(delta))
        st.session_state.break_last_update = now

# ---------------- 집중 타이머 ----------------
st.markdown("## ⏱️ 25분 집중 타이머")

focus_col1, focus_col2, focus_col3 = st.columns(3)
with focus_col1:
    if st.button("▶️ 시작", key="focus_start_btn"):
        st.session_state.focus_running = True
        st.session_state.focus_last_update = time.time()
with focus_col2:
    if st.button("⏸️ 일시정지", key="focus_pause_btn"):
        st.session_state.focus_running = False
with focus_col3:
    if st.button("🔁 초기화", key="focus_reset_btn"):
        st.session_state.focus_running = False
        st.session_state.focus_remaining = 25 * 60

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
    if st.button("▶️ 시작", key="break_start_btn"):
        st.session_state.break_running = True
        st.session_state.break_last_update = time.time()
with break_col2:
    if st.button("⏸️ 일시정지", key="break_pause_btn"):
        st.session_state.break_running = False
with break_col3:
    if st.button("🔁 초기화", key="break_reset_btn"):
        st.session_state.break_running = False
        st.session_state.break_remaining = 5 * 60

update_timer("break")

bmin, bsec = divmod(st.session_state.break_remaining, 60)
st.subheader(f"🕒 남은 휴식 시간: {bmin:02d}:{bsec:02d}")
if st.session_state.break_remaining == 0:
    st.info("☕ 휴식 끝! 다시 집중해볼까요?")

# ---------------- To-Do 리스트 ----------------
st.markdown("---")
st.header("✅ 오늘의 할 일")

# 입력 상태 값 따로 관리 (rerun 없이도 동작)
if "new_task_input_val" not in st.session_state:
    st.session_state.new_task_input_val = ""

# 할 일 입력창
new_task = st.text_input("할 일을 입력하세요", value=st.session_state.new_task_input_val)

# 추가 버튼
if st.button("추가"):
    if new_task.strip():
        if "checklist" not in st.session_state:
            st.session_state.checklist = []
        st.session_state.checklist.append({"text": new_task.strip(), "checked": False})
        st.session_state.new_task_input_val = ""  # 입력창 초기화 값 리셋

# 체크박스 리스트
if "checklist" not in st.session_state:
    st.session_state.checklist = []

for i, item in enumerate(st.session_state.checklist):
    task_key = f"task_{i}_{item['text']}"
    checked = st.checkbox(item["text"], value=item["checked"], key=task_key)
    st.session_state.checklist[i]["checked"] = checked
# ------------------- 오늘의 일기 -------------------
import datetime
today = datetime.date.today().isoformat()

# ✅ diary 상태 초기화
if "diary" not in st.session_state:
    st.session_state.diary = {}

# ✅ 에러 없이 접근
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
