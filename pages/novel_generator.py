import streamlit as st
from openai import OpenAI
import textwrap

# OpenAI 라이브러리를 이용해 텍스트를 생성하는 함수
def generate_text(keyword, model="gpt-4-turbo-2024-04-09"):
    # API 키 설정
    client = OpenAI(api_key=st.secrets["api_key"])

    # 대화 메시지 정의
    messages = [
        {"role": "user", "content": f"Write a novel based on the keyword: {keyword}."}
    ]
    
    # Chat Completions API 호출
    response = client.chat.completions.create(
                            model=model,          # 사용할 모델 선택 
                            messages=messages,    # 전달할 메시지 지정
                            max_tokens=1000,      # 응답 최대 토큰 수 지정 
                            temperature=0.7,      # 완성의 다양성을 조절하는 온도 설정
                            n=1                   # 생성할 완성의 개수 지정
    )
    
    novel_text = response.choices[0].message.content
    return novel_text

def main():
    # 페이지 제목
    st.title("Novel Generator")

    # 사용자로부터 키워드 입력 받기
    keyword = st.text_input("Enter a keyword to generate a novel:", "")

    if st.button("Generate Novel"):
        if keyword:
            st.write("Generating novel based on the keyword...")
            # 소설 생성
            novel = generate_text(keyword)
            # 생성된 소설 출력
            st.write("Generated Novel:")
            st.write(novel)
        else:
            st.error("Please enter a keyword to generate a novel.")

if __name__ == "__main__":
    main()