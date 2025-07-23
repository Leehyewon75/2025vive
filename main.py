import streamlit as st
import time
import random
import hashlib
from datetime import date

st.set_page_config(page_title="미루지 말자!", layout="centered")

# 초기 세션 상태
if "checklist" not in st.session_state:
    st.session_state.checklist = []

if "reward_categories" not in st.session_state:
    st.session_state.reward_categories = {}

if "selected_reward" not in st.session_state:
    st.session_state.selected_reward = None

if "diary_entries" not in st.session_state:
    st.session_state.diary_entries = {}

if "timer_running" not in st.session_state:
    st.session_state.timer_running = False

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "paused" not in st.session_state:
    st.session_state.paused = False

if "elapsed" not in st.session_state:
    st.session_state.elapsed = 0


# --------------------------------------------------
# 📋 체크리스트
# --------------------------------------------------
st.title("✅ 체크리스트 + ⏱ 타이머 + 🎁 보상 + 📝 일기")

st.header("📋 오늘의 할 일")
task_input = st.text_input("할 일 입력", key="input_task")
if st.button("➕ 추가"):
    if task_input.strip():
        st.session_state.checklist.append({"text": task_input.strip(), "checked": False})
        st.success("할 일이 추가되었습니다!")

def get_safe_key(text, index):
    return f"task_{index}_" + hashlib.md5(text.encode()).hexdigest()

completed = 0
for i, item in enumerate(st.session_state.checklist):
    key = get_safe_key(item["text"], i)
    checked = st.checkbox(item["text"], value=item["checked"], key=key)
    st.session_state.checklist[i]["checked"] = checked
    if checked:
        completed += 1

total = len(st.session_state.checklist)
if total > 0:
    st.markdown(f"**완료: {completed} / {total}**")
    st.progress(completed / total)
else:
    st.info("할 일을 입력해보세요!")

# --------------------------------------------------
# ⏱ 타이머 (25분, 일시정지/재시작)
# --------------------------------------------------
st.header("⏱ 집중 타이머 (25분)")

TIMER_DURATION = 25 * 60
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶️ 시작", disabled=st.session_state.timer_running):
        st.session_state.start_time = time.time() - st.session_state.elapsed
        st.session_state.timer_running = True
        st.session_state.paused = False

with col2:
    if st.button("⏸ 일시정지", disabled=not st.session_state.timer_running or st.session_state.paused):
        st.session_state.paused = True
        st.session_state.elapsed = time.time() - st.session_state.start_time
        st.session_state.timer_running = False

with col3:
    if st.button("🔁 리셋"):
        st.session_state.timer_running = False
        st.session_state.paused = False
        st.session_state.start_time = None
        st.session_state.elapsed = 0

# 타이머 시간 계산
if st.session_state.timer_running and not st.session_state.paused:
    elapsed = time.time() - st.session_state.start_time
else:
    elapsed = st.session_state.elapsed

remaining = max(0, TIMER_DURATION - int(elapsed))
minutes, seconds = divmod(remaining, 60)
st.markdown(f"### ⏳ 남은 시간: **{minutes:02d}:{seconds:02d}**")

# 타이머 완료
if remaining == 0 and st.session_state.timer_running:
    st.session_state.timer_running = False
    st.session_state.paused = False
    st.success("🎉 집중 완료! 잘했어요!")
    st.balloons()

if st.session_state.timer_running:
    st.experimental_rerun()


# --------------------------------------------------
# 🎁 보상 등록 + 랜덤 뽑기
# --------------------------------------------------
st.header("🎁 카테고리별 보상 등록")

with st.form("reward_form_section"):
    category = st.text_input("카테고리 입력", placeholder="예: 음식, 휴식")
    reward = st.text_input("보상 내용", placeholder="예: 치킨 먹기")
    submit = st.form_submit_button("추가")
    if submit and category.strip() and reward.strip():
        if category not in st.session_state.reward_categories:
            st.session_state.reward_categories[category] = []
        st.session_state.reward_categories[category].append(reward)
        st.success("보상이 추가되었습니다!")

# 보상 보기
if st.session_state.reward_categories:
    for cat, rewards in st.session_state.reward_categories.items():
        st.markdown(f"**🗂️ {cat}**")
        for r in rewards:
            st.write(f"• {r}")

# 보상 뽑기
st.header("🏆 보상 뽑기")
if completed == total and total > 0:
    cat_list = list(st.session_state.reward_categories.keys())
    if cat_list:
        selected_cat = st.selectbox("보상 카테고리 선택", cat_list)
        if st.button("🎲 보상 뽑기"):
            pool = st.session_state.reward_categories[selected_cat]
            if pool:
                st.session_state.selected_reward = random.choice(pool)
    else:
        st.info("보상 카테고리를 먼저 등록하세요.")
else:
    st.info("체크리스트를 모두 완료해야 보상을 뽑을 수 있어요.")

if st.session_state.selected_reward:
    st.success(f"🎉 오늘의 보상: **{st.session_state.selected_reward}**")


# --------------------------------------------------
# 📝 일기 기능
# --------------------------------------------------
st.header("📝 오늘의 일기")

today = date.today().isoformat()
default_text = st.session_state.diary_entries.get(today, "")
diary = st.text_area("오늘 하루 어땠나요?", value=default_text, height=200)

if st.button("💾 일기 저장"):
    st.session_state.diary_entries[today] = diary
    st.success("일기가 저장되었습니다.")

# 이전 일기 열람
if st.session_state.diary_entries:
    st.subheader("📚 이전 일기 보기")
    dates = sorted(st.session_state.diary_entries.keys(), reverse=True)
    selected = st.selectbox("날짜 선택", dates)
    st.text_area("📖 저장된 일기", value=st.session_state.diary_entries[selected], height=200, disabled=True)
