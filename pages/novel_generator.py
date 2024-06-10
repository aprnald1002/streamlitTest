import streamlit as st
from openai import OpenAI

# OpenAI 라이브러리를 이용해 텍스트를 생성하는 함수
def generate_text(keywords, model="gpt-4-turbo-2024-04-09"):
    # API 키 설정
    client = OpenAI(api_key=st.secrets["api_key"])

    # 키워드들을 하나의 문자열로 결합
    keyword_text = ", ".join(keywords)

    # 대화 메시지 정의
    messages = [
        {"role": "system", "content": "당신은 창의적이고 자유로운 소설 작가입니다."},
        {"role": "user", "content": f"다음 키워드들을 기반으로 흥미롭고 창의적인 소설을 작성해 주세요: {keyword_text}. 자유롭게 상상력을 발휘해 주세요."}
    ]
    
    # Chat Completions API 호출
    response = client.chat.completions.create(
                            model=model,          # 사용할 모델 선택 
                            messages=messages,    # 전달할 메시지 지정
                            max_tokens=3000,      # 응답 최대 토큰 수 지정 (늘렸습니다)
                            temperature=0.9,      # 완성의 다양성을 조절하는 온도 설정 (높였습니다)
                            n=1                   # 생성할 완성의 개수 지정
    )
    
    novel_text = response.choices[0].message.content
    return novel_text

def main():
    # 페이지 제목
    st.title("소설 생성기")

    # 사용자로부터 키워드 입력 받기
    keywords_input = st.text_area("소설 생성을 위한 키워드를 입력하세요 (쉼표로 구분):", "")

    if st.button("소설 생성"):
        if keywords_input:
            # 입력받은 키워드를 리스트로 변환
            keywords = [keyword.strip() for keyword in keywords_input.split(",")]

            st.write("키워드를 기반으로 소설을 생성하고 있습니다...")
            # 소설 생성
            novel = generate_text(keywords)
            # 생성된 소설 출력
            st.write("생성된 소설:")
            st.write(novel)
        else:
            st.error("소설 생성을 위한 키워드를 입력해주세요.")

if __name__ == "__main__":
    main()
