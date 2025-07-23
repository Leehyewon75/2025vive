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

import streamlit as st
import time

# 🔁 자동 새로고침: 1초마다
st_autorefresh(interval=1000, key="auto_refresh")

# ✅ 타이머 상태 초기화 함수 (먼저 정의!)
def init_timers():
    defaults = {
        "focus_running": False,
        "focus_start": None,
        "focus_remaining": 25 * 60,
        "focus_total": 0,
        "focus_logged": False,
        "break_running": False,
        "break_start": None,
        "break_remaining": 5 * 60,
        "break_total": 0,
        "break_logged": False
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

# ✅ 함수 호출 (정의 아래에서!)
init_timers()

# ---------------- 집중 타이머 ----------------
st.markdown("## ⏱️ 25분 집중 타이머")

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("▶️ 집중 시작"):
        if not st.session_state.focus_running:
            st.session_state.focus_start = time.time()
            st.session_state.focus_running = True
with c2:
    if st.button("⏸️ 집중 일시정지"):
        st.session_state.focus_running = False
with c3:
    if st.button("🔁 집중 초기화"):
        st.session_state.focus_running = False
        st.session_state.focus_remaining = 25 * 60
        st.session_state.focus_logged = False

# 남은 시간 갱신
if st.session_state.focus_running:
    elapsed = int(time.time() - st.session_state.focus_start)
    st.session_state.focus_remaining = max(0, st.session_state.focus_remaining - elapsed)
    st.session_state.focus_start = time.time()

    if st.session_state.focus_remaining == 0 and not st.session_state.focus_logged:
        st.session_state.focus_total += 25 * 60
        st.session_state.focus_logged = True

fmin, fsec = divmod(st.session_state.focus_remaining, 60)
st.subheader(f"🧠 남은 집중 시간: {fmin:02d}:{fsec:02d}")
if st.session_state.focus_remaining == 0:
    st.success("🎉 집중 시간 종료! 이제 휴식해요.")

# ---------------- 휴식 타이머 ----------------
st.markdown("---")
st.markdown("## 🛌 5분 휴식 타이머")

b1, b2, b3 = st.columns(3)
with b1:
    if st.button("▶️ 휴식 시작"):
        if not st.session_state.break_running:
            st.session_state.break_start = time.time()
            st.session_state.break_running = True
with b2:
    if st.button("⏸️ 휴식 일시정지"):
        st.session_state.break_running = False
with b3:
    if st.button("🔁 휴식 초기화"):
        st.session_state.break_running = False
        st.session_state.break_remaining = 5 * 60
        st.session_state.break_logged = False

# 남은 시간 갱신
if st.session_state.break_running:
    elapsed = int(time.time() - st.session_state.break_start)
    st.session_state.break_remaining = max(0, st.session_state.break_remaining - elapsed)
    st.session_state.break_start = time.time()

    if st.session_state.break_remaining == 0 and not st.session_state.break_logged:
        st.session_state.break_total += 5 * 60
        st.session_state.break_logged = True

bmin, bsec = divmod(st.session_state.break_remaining, 60)
st.subheader(f"☕ 남은 휴식 시간: {bmin:02d}:{bsec:02d}")
if st.session_state.break_remaining == 0:
    st.info("🔔 휴식 끝! 다시 집중할 시간이에요.")

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
