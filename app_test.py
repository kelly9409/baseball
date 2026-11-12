import streamlit as st
from baseball_utils import *

# 최대 기회 설정
MAX_TRY = 10

# 세션 상태 초기화 (게임 상태 유지)
if "answer" not in st.session_state:
    st.session_state.answer = make_answer()
if "history" not in st.session_state:
    st.session_state.history = []
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "win" not in st.session_state:
    st.session_state.win = False

# 타이틀 및 설명
st.markdown("### ⚾ 숫자야구 게임")
st.write(f"1~9 서로 다른 숫자 3개 · 기회는 {MAX_TRY}번")

# 게임이 끝났더라도 입력창을 유지하기 위해 form을 항상 표시
current_try = len(st.session_state.history) + 1

with st.form(key="baseball_form"):
    # 게임이 이미 끝났거나 기회를 다 쓴 경우 입력 비활성화 혹은 안내 문구 처리 가능
    disabled_input = st.session_state.game_over
    
    text = st.text_input(
        f"세 자리 수 입력 ({min(current_try, MAX_TRY)}/{MAX_TRY})",
        disabled=disabled_input,
        placeholder="게임이 종료되었습니다." if disabled_input else ""
    )
    submit_button = st.form_submit_button(label="던지기!", disabled=disabled_input)
    
    if submit_button and not st.session_state.game_over:
        # 입력 검증
        error = check_input(text)
        if error != "":
            st.error(error)
        else:
            # 숫자 변환 및 결과 계산
            guess = to_numbers(text)
            strike = count_strike(st.session_state.answer, guess)
            ball = count_ball(st.session_state.answer, guess)
            res_text = result_text(strike, ball)
            
            # 기록 저장
            st.session_state.history.append({
                "try": current_try,
                "text": text,
                "result": res_text,
                "strike": strike
            })
            
            # 승리 또는 패배 조건 체크
            if strike == 3:
                st.session_state.game_over = True
                st.session_state.win = True
            elif len(st.session_state.history) >= MAX_TRY:
                st.session_state.game_over = True
                st.session_state.win = False
            
            st.rerun()

# 지금까지의 시도 기록 출력
for h in st.session_state.history:
    st.write(f"{h['try']}회 : {h['text']} → {h['result']}")

# 게임 종료 시 결과 메시지 및 축하 효과 (풍선) 출력
if st.session_state.game_over:
    if st.session_state.win:
        # 맞혔을 때 풍선 날리기 효과!
        st.balloons()
        st.success(f"홈런! {len(st.session_state.history)}번 만에 맞혔습니다.")
    else:
        st.error(f"실패! 정답은 {st.session_state.answer}입니다.")
        
    # 다시 하기 버튼
    if st.button("다시 하기"):
        st.session_state.answer = make_answer()
        st.session_state.history = []
        st.session_state.game_over = False
        st.session_state.win = False
        st.rerun()