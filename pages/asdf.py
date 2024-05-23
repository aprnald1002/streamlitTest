import streamlit as st
import openai

# OpenAI API 키 설정
openai.api_key = st.secrets["hagunloc"]

def generate_story(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # 또는 "gpt-4"로 변경 가능
        prompt=prompt,
        max_tokens=500,  # 생성할 텍스트 길이 조절
        temperature=0.7,  # 텍스트 생성의 창의성 조절
    )
    story = response.choices[0].text.strip()
    return story

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