import streamlit as st
import time

# 타이머 상태 저장용 세션 설정
if "is_running" not in st.session_state:
    st.session_state.is_running = False
if "mode" not in st.session_state:
    st.session_state.mode = "Focus"
if "start_time" not in st.session_state:
    st.session_state.start_time = None

# 시간 설정
focus_duration = 25 * 60  # 25분
break_duration = 10 * 60  # 10분

# 남은 시간 계산
def get_remaining_time():
    elapsed = time.time() - st.session_state.start_time
    total = focus_duration if st.session_state.mode == "Focus" else break_duration
    return max(0, total - elapsed)

# 타이머 출력
def format_time(seconds):
    mins = int(seconds) // 60
    secs = int(seconds) % 60
    return f"{mins:02d}:{secs:02d}"

st.title("⏳ 뽀모도로 집중 타이머")

st.write(f"현재 모드: **{st.session_state.mode}**")

# 타이머 시작
if not st.session_state.is_running:
    if st.button("▶️ 타이머 시작"):
        st.session_state.start_time = time.time()
        st.session_state.is_running = True
else:
    remaining = get_remaining_time()
    st.metric("남은 시간", format_time(remaining))
    
    if remaining <= 0:
        st.success(f"{st.session_state.mode} 시간이 끝났어요! 🎉")
        if st.session_state.mode == "Focus":
            st.session_state.mode = "Break"
        else:
            st.session_state.mode = "Focus"
        st.session_state.is_running = False
    else:
        # 자동 새로고침 (1초마다)
        st.experimental_rerun()

# 초기화 버튼
if st.button("🔄 타이머 리셋"):
    st.session_state.is_running = False
    st.session_state.start_time = None
    st.session_state.mode = "Focus"
    st.rerun()
