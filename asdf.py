import streamlit as st
import openai
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = st.secrets["hagunloc"]

def generate_story(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # 최신 모델로 변경
            messages=[
                {"role": "system", "content": "You are a creative and imaginative AI."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,  # 생성할 텍스트 길이 조절
            temperature=0.7,  # 텍스트 생성의 창의성 조절
        )
        story = response['choices'][0]['message']['content'].strip()
        return story
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")
        return ""

st.title("AI 소설 생성기")
st.write("키워드를 입력하면 AI가 소설을 생성합니다.")

# 키워드 입력 받기
keywords = st.text_input("키워드를 입력하세요:", "")

if st.button("소설 생성"):
    if keywords:
        prompt = f"다음 키워드를 기반으로 소설을 작성하세요: {keywords}"
        story = generate_story(prompt)
        st.subheader("생성된 소설")
        st.write(story)
    else:
        st.error("키워드를 입력하세요.")
