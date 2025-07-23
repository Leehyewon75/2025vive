import streamlit as st
import time
import random
from datetime import date
from streamlit_autorefresh import st_autorefresh  # ✅ 자동 새로고침

# ✅ 자동 새로고침: 1초마다 새로고침
st_autorefresh(interval=1000, limit=None, key="autorefresh")

st.set_page_config(page_title="공부 앱 - 미루지 말자!", layout="centered")

# ---------------- 세션 상태 초기화 ----------------
def init_state():
    st.session_state.setdefault("focus_running", False)
    st.session_state.setdefault("focus_remaining", 25 * 60)
    st.session_state.setdefault("focus_last_update", time.time())

    st.session_state.setdefault("break_running", False)
    st.session_state.setdefault("break_remaining", 5 * 60)
    st.session_state.setdefault("break_last_update", time.time())

    st.session_state.setdefault("checklist", [])
    st.session_state.setdefault("new_task_input_val", "")
    st.session_state.setdefault("diary", {})
    st.session_state.setdefault("goal_minutes", 0)
    st.session_state.setdefault("focus_log", [])
    st.session_state.setdefault("break_log", [])
    st.session_state.setdefault("motivation", "")

init_state()

# ---------------- 타이머 업데이트 ----------------
def update_timer(timer_type):
    now = time.time()
    if timer_type == "focus" and st.session_state.focus_running:
        elapsed = int(now - st.session_state.focus_last_update)
        st.session_state.focus_remaining = max(0, st.session_state.focus_remaining - elapsed)
        st.session_state.focus_last_update = now
    elif timer_type == "break" and st.session_state.break_running:
        elapsed = int(now - st.session_state.break_last_update)
        st.session_state.break_remaining = max(0, st.session_state.break_remaining - elapsed)
        st.session_state.break_last_update = now

# ---------------- 1. 오늘의 할 일 ----------------
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

# ---------------- 2. 목표 입력 ----------------
st.markdown("---")
st.header("🎯 오늘의 목표 집중 시간")

goal = st.number_input("오늘의 목표 집중 시간 (분)", min_value=0, max_value=1440, value=st.session_state.goal_minutes)
st.session_state.goal_minutes = goal
st.info(f"오늘의 목표: **{goal}분** 집중")

# ---------------- 3. 동기부여 ----------------
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

# ---------------- 4. 집중 타이머 ----------------
st.markdown("---")
st.header("⏱ 25분 집중 타이머")

update_timer("focus")
fmin, fsec = divmod(st.session_state.focus_remaining, 60)
st.subheader(f"🕒 남은 집중 시간: {fmin:02d}:{fsec:02d}")

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

if st.session_state.focus_remaining == 0:
    st.success("🎉 집중 시간 종료! 휴식 시간으로 넘어가세요.")

# ---------------- 5. 휴식 타이머 ----------------
st.markdown("---")
st.header("🛌 5분 휴식 타이머")

update_timer("break")
bmin, bsec = divmod(st.session_state.break_remaining, 60)
st.subheader(f"🕒 남은 휴식 시간: {bmin:02d}:{bsec:02d}")

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

if st.session_state.break_remaining == 0:
    st.info("☕ 휴식 종료! 다시 집중해볼까요?")

# ---------------- 6. 집중/휴식 수동 기록 ----------------
st.markdown("---")
st.header("🧠 수동 집중 / ☕ 휴식 시간 기록")

with st.form("time_log_form"):
    focus = st.number_input("추가할 집중 시간 (분)", min_value=0, step=1)
    rest = st.number_input("추가할 휴식 시간 (분)", min_value=0, step=1)
    submitted = st.form_submit_button("기록하기")

    if submitted:
        if focus > 0:
            st.session_state.focus_log.append(focus)
        if rest > 0:
            st.session_state.break_log.append(rest)
        st.success("✅ 시간이 기록되었습니다!")

# ---------------- 7. 오늘의 일기 ----------------
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

# ---------------- 8. 통계 ----------------
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
