import streamlit as st
from baseball_utils import *
 
MAX_TRY = 10
 
def new_game():
    st.session_state.answer = make_answer()
    st.session_state.history = []      # [(입력, 결과), ...]
    st.session_state.done = False
    st.session_state.win = False
 
if 'answer' not in st.session_state:
    new_game()
 
st.title('⚾ 숫자야구 게임')
st.caption('1~9 서로 다른 숫자 3개 · 기회는 10번')

tries = len(st.session_state.history)
with st.form('guess_form', clear_on_submit=True):
    text = st.text_input(f'세 자리 수 입력 ({tries + 1}/{MAX_TRY})',
                         max_chars=3, key='guess')
    ok = st.form_submit_button('던지기!',
                               disabled=st.session_state.done)
 
if ok:
    error = check_input(text)
    if error != '':
        st.warning(error)
    else:
        guess = to_numbers(text)
        strike = count_strike(st.session_state.answer, guess)
        ball = count_ball(st.session_state.answer, guess)
        result = result_text(strike, ball)
        st.session_state.history.append((text, result))
        if strike == 3:
            st.session_state.done = True
            st.session_state.win = True
        elif len(st.session_state.history) >= MAX_TRY:
            st.session_state.done = True
        st.rerun()

n = 1
for g, r in st.session_state.history:
    st.write(f'{n}회 : **{g}** → {r}')
    n += 1
 
if st.session_state.done:
    count = len(st.session_state.history)
    if st.session_state.win:
        st.success(f'홈런! {count}번 만에 맞혔습니다.')
        st.balloons()
    else:
        st.error(f'실패! 정답은 {st.session_state.answer}')
    if st.button('새 게임'):
        new_game()
        st.rerun()
