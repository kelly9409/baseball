import random

def make_answer() :
    return random.sample(range(1,10), 3)

def check_input(text):
    if len(text) != 3 or not text.isdigit():
        return '세 자리 숫자를 입력하세요!'
    if not text.isdigit():
        return '숫자만 입력하세요!'
    if '0' in text:
        return '0은 입력할 수 없습니다!(1~9)'
    if len(set(text)) != 3:
        return '중복된 숫자는 입력할 수 없습니다!'
    return ''

# [블록 3] 문자열 '381' → 리스트 [3, 8, 1]
def to_numbers(text):
    nums = []
    for ch in text:
        nums.append(int(ch))
    return nums


# [블록 4] 스트라이크 : 숫자와 자리가 모두 같다
def count_strike(answer, guess):
    strike = 0
    for i in range(3):
        if guess[i] == answer[i]:
            strike += 1
    return strike


# [블록 5] 볼 : 숫자는 있지만 자리가 다르다
def count_ball(answer, guess):
    ball = 0
    for i in range(3):
        if guess[i] != answer[i] and guess[i] in answer:
            ball += 1
    return ball

# [블록 6] 판정 결과를 글자로
def result_text(strike, ball):
    if strike == 0 and ball == 0:
        return 'OUT'
    return f'{strike}S {ball}B'
