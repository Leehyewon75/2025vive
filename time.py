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
    """세션 상태의 기본값을 설정하거나 초기화하는 함수"""
    defaults = {
        "checklist": [],
        "reward_categories": {},
        "selected_reward": None,
        "diary_entries": {},
        "start_time": None,
        "running": False, # 타이머 실행 상태
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

    # 안전성 강화: diary_entries가 딕셔너리인지 확인
    if not isinstance(st.session_state.diary_entries, dict):
        st.session_state.diary_entries = {}

init_session_state()

# ----------------------------
# ✅ 체크리스트
# ----------------------------
st.title("✅ study")
st.header("📋 오늘의 할 일")

# 할 일 입력 필드를 st.form 안에 넣어서 제출 시 자동으로 초기화되게 변경
with st.form("task_input_form", clear_on_submit=True): # clear_on_submit=True 중요!
    task_input = st.text_input("할 일 입력", key="form_task_input") # key 변경 (충돌 방지)
    add_button = st.form_submit_button("➕ 추가")

    if add_button: # 폼 제출 버튼 클릭 시
        if task_input.strip(): # 빈 문자열이 아닐 경우에만 추가
            st.session_state.checklist.append({"text": task_input.strip(), "checked": False})
            st.success("할 일이 추가되었습니다")
        else:
            st.warning("할 일을 입력해주세요") # 입력 내용이 없으면 경고 메시지

# 할 일 목록을 고유하게 식별하기 위한 함수
def get_safe_key(text, index):
    return f"task_{index}_" + hashlib.md5(text.encode()).hexdigest()

completed = 0
# 체크리스트 항목 표시 및 완료 상태 업데이트
for i, item in enumerate(st.session_state.checklist):
    # 각 할 일 옆에 체크박스를 만들고 고유 키를 부여
    key = get_safe_key(item["text"], i)
    checked = st.checkbox(item["text"], value=item["checked"], key=key)
    st.session_state.checklist[i]["checked"] = checked
    if checked:
        completed += 1 # 완료된 할 일 개수 세기

total = len(st.session_state.checklist)
if total > 0:
    st.markdown(f"**완료: {completed} / {total}**")
    st.progress(completed / total) # 완료 진행률 막대
else:
    st.info("할 일을 입력해서 미루기 방지 시작해보세요! 💪")

# ----------------------------
# ✅ 보상 등록 + 랜덤 뽑기
# ----------------------------
st.header("🎁 보상")

with st.form("reward_form_section"):
    category = st.text_input("카테고리 입력", placeholder="예: 맛있는 간식, 힐링 타임", key="reward_category_input")
    reward = st.text_input("보상 내용", placeholder="예: 내가 좋아하는 초콜릿 먹기, 따뜻한 차 한 잔", key="reward_content_input")
    submit_reward = st.form_submit_button("추가") # 버튼 이름 변경 (다른 폼과 구분)
    if submit_reward and category.strip() and reward.strip():
        # 딕셔너리에 카테고리가 없으면 새로 만들고 보상 추가
        st.session_state.reward_categories.setdefault(category, []).append(reward)
        st.success("새로운 보상이 등록되었습니다! 🥰")

# 등록된 보상 출력
if st.session_state.reward_categories:
    st.subheader("💡 내가 등록한 보상 목록")
    for cat, rewards in st.session_state.reward_categories.items():
        st.markdown(f"**⭐ {cat}**")
        for r in rewards:
            st.write(f"• {r}")
else:
    st.info("열심히 일한 당신, 보상도 등록하고 계획해 볼까요? 🥳")

# 보상 뽑기
st.header("🏆 보상 뽑기")
# 모든 체크리스트 완료 시에만 보상 뽑기 가능
if completed == total and total > 0:
    cat_list = list(st.session_state.reward_categories.keys())
    if cat_list: # 등록된 카테고리가 있을 경우
        selected_cat = st.selectbox("어떤 카테고리에서 뽑아볼까?", cat_list)
        if st.button("🎲 보상 뽑기"):
            pool = st.session_state.reward_categories[selected_cat]
            if pool:
                st.session_state.selected_reward = random.choice(pool) # 랜덤으로 보상 선택
            else:
                st.warning(f"'{selected_cat}' 카테고리에는 아직 보상이 없어요! 추가해주세요")
    else:
        st.info("보상을 뽑으려면 먼저 '카테고리별 보상 등록'에서 보상을 등록해줘야 합니다! 😥")
else:
    st.info("아직 할 일이 남아있어요! 모든 체크리스트를 완료하면 보상을 뽑을 수 있습니다. ✨")

# 선택된 보상이 있을 경우 표시
if st.session_state.selected_reward:
    st.success(f"🎉 오늘 보상은 **{st.session_state.selected_reward}**! 🎉")

# ----------------------------
# ✅ 25분 집중 타이머 (포모도로)
# ----------------------------
st.header("⏱ 25분 집중 타이머")
st.markdown("규칙적인 휴식으로 집중력을 높여보세요 🔥")

# 타이머 시작 버튼
if st.button("▶️ 타이머 시작", key="start_timer_btn"):
    # 이미 타이머가 실행 중이 아니라면 시작
    if not st.session_state.running:
        st.session_state.start_time = time.time()
        st.session_state.running = True

# 타이머 중단 버튼
if st.button("⏹️ 타이머 중단", key="stop_timer_btn"):
    st.session_state.running = False
    st.session_state.start_time = None # 시작 시간 초기화 (타이머 중단 시)

total_seconds = 25 * 60 # 총 25분 (초 단위)

# 타이머가 실행 중일 경우 남은 시간 계산 및 표시
if st.session_state.running:
    # 현재 시간에서 시작 시간을 빼서 경과 시간을 계산
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = total_seconds - elapsed # 남은 시간 계산

    if remaining <= 0:
        st.success("⏰ 25분 집중 시간 완료! 🥳")
        st.session_state.running = False # 타이머 중단
        st.session_state.start_time = None # 시작 시간 초기화
    else:
        mins, secs = divmod(remaining, 60) # 남은 시간을 분과 초로 변환
        st.subheader(f"남은 시간: **{mins:02d}:{secs:02d}** 틱톡 ⏰")
        st.progress((total_seconds - remaining) / total_seconds) # 진행률 막대 업데이트
        # 타이머가 계속 틱톡 거리도록 페이지를 계속 새로고침
        time.sleep(1) # 1초 대기 (CPU 부하 줄임)
        st.rerun() # 페이지 새로고침

else:
    st.write("버튼을 눌러 집중 타이머를 시작할 수 있습니다")

# ----------------------------
# ✅ 일기 기능
# ----------------------------
st.header("📝 일기")

# 오늘 날짜를 YYYY-MM-DD 형식으로 가져오기
today = datetime.date.today().isoformat()
# 해당 날짜에 저장된 일기가 있으면 불러오고, 없으면 빈 문자열
default_text = st.session_state.diary_entries.get(today, "")
# 일기 입력 필드
diary_input = st.text_area("오늘 하루 어땠나요? 마음껏 적어보세요! 💖", value=default_text, height=200, key="diary_textarea")

if st.button("💾 일기 저장", key="save_diary_btn"):
    if isinstance(st.session_state.diary_entries, dict): # diary_entries가 딕셔너리인지 다시 확인 (안전성)
        st.session_state.diary_entries[today] = diary_input # 현재 날짜로 일기 저장
        st.success("일기가 저장되었습니다")
    else:
        st.error("❗️이런! 일기 저장에 문제가 생겼습니다. 다시 시도해 주세요 😥")

# 이전 일기 보기
if st.session_state.diary_entries:
    st.subheader("📚 지나간 내 일기 다시 보기")
    # 저장된 일기 날짜들을 최신순으로 정렬
    dates = sorted(st.session_state.diary_entries.keys(), reverse=True)
    selected_date = st.selectbox("궁금한 날짜를 선택해보세요!", dates)
    # 선택된 날짜의 일기 내용 불러오기
    saved_diary_content = st.session_state.diary_entries.get(selected_date, "")
    st.text_area(f"📖 {selected_date}의 일기", value=saved_diary_content, height=200, disabled=True, key="view_diary_textarea")
else:
    st.info("아직 작성된 일기가 없습니다 오늘 하루를 기록해보는 건 어떨가요? ✍️")
