import streamlit as st
import time
import random
import hashlib
import datetime

st.set_page_config(page_title="미루지 말자!", layout="centered")

# ----------------------------
# ✅ 세션 상태 초기화
# ----------------------------
def init_session_state():
    defaults = {
        "checklist": [],
        "reward_categories": {},
        "selected_reward": None,
        "diary_entries": {},
        "timer_running": False,
        "start_time": None,
        "paused": False,
        "elapsed": 0,
        "running": False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

    # 안전성 강화
    if not isinstance(st.session_state.diary_entries, dict):
        st.session_state.diary_entries = {}

init_session_state()

# ----------------------------
# ✅ 체크리스트
# ----------------------------
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

# ----------------------------
# ✅ 보상 등록 + 랜덤 뽑기
# ----------------------------
st.header("🎁 카테고리별 보상 등록")

with st.form("reward_form_section"):
    category = st.text_input("카테고리 입력", placeholder="예: 음식, 휴식")
    reward = st.text_input("보상 내용", placeholder="예: 치킨 먹기")
    submit = st.form_submit_button("추가")
    if submit and category.strip() and reward.strip():
        st.session_state.reward_categories.setdefault(category, []).append(reward)
        st.success("보상이 추가되었습니다!")

# 등록된 보상 출력
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

# ----------------------------
# ✅ 25분 타이머
# ----------------------------
st.header("⏱ 25분 집중 타이머")

if st.button("▶️ 타이머 시작"):
    st.session_state.start_time = time.time()
    st.session_state.running = True

if st.button("⏹️ 타이머 중단"):
    st.session_state.running = False

total_seconds = 25 * 60

if st.session_state.running:
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = total_seconds - elapsed

    if remaining <= 0:
        st.success("⏰ 25분이 끝났어요! 잠시 쉬어가요 🍅")
        st.session_state.running = False
    else:
        mins, secs = divmod(remaining, 60)
        st.subheader(f"{mins:02d}:{secs:02d} 남음")
        st.progress((total_seconds - remaining) / total_seconds)
        st.rerun()
else:
    st.write("버튼을 눌러 타이머를 시작하세요.")

# ----------------------------
# ✅ 일기 기능
# ----------------------------
st.header("📝 오늘의 일기")

today = datetime.date.today().isoformat()
default_text = st.session_state.diary_entries.get(today, "")
diary = st.text_area("오늘 하루 어땠나요?", value=default_text, height=200)

if st.button("💾 일기 저장"):
    if isinstance(st.session_state.diary_entries, dict):
        st.session_state.diary_entries[today] = diary
        st.success("일기가 저장되었습니다.")
    else:
        st.error("❗️일기 저장에 문제가 발생했습니다.")

# 이전 일기 보기
if st.session_state.diary_entries:
    st.subheader("📚 이전 일기 보기")
    dates = sorted(st.session_state.diary_entries.keys(), reverse=True)
    selected = st.selectbox("날짜 선택", dates)
    saved = st.session_state.diary_entries.get(selected, "")
    st.text_area("📖 저장된 일기", value=saved, height=200, disabled=True)
