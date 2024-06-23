import streamlit as st
from openai import OpenAI

# OpenAI 라이브러리를 이용해 텍스트를 생성하는 함수
def generate_text(prompt, model="gpt-4-turbo-2024-04-09", max_tokens=3000, temperature=0.9):
    client = OpenAI(api_key=st.secrets["api_key"])

    messages = [
        {"role": "system", "content": "당신은 창의적이고 자유로운 소설 작가입니다."},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        n=1
    )

    novel_text = response.choices[0].message.content
    return novel_text

# 세션 상태 초기화
if 'novel_generated' not in st.session_state:
    st.session_state['novel_generated'] = False
if 'current_novel' not in st.session_state:
    st.session_state['current_novel'] = ""

def main():
    st.title("소설 생성기")

    option = st.radio("선택하세요", ["키워드 기반 소설 생성", "문장 기반 소설 생성"])

    if option == "키워드 기반 소설 생성":
        keywords_input = st.text_area("소설 생성을 위한 키워드를 입력하세요 (쉼표로 구분):", "")
        if st.button("소설 생성", key="keyword_generate"):
            if keywords_input:
                keywords = [keyword.strip() for keyword in keywords_input.split(",")]
                prompt = f"다음 키워드들을 기반으로 흥미롭고 창의적인 소설을 작성해 주세요: {', '.join(keywords)}. 자유롭게 상상력을 발휘해 주세요."
                st.write("키워드를 기반으로 소설을 생성하고 있습니다...")
                novel = generate_text(prompt)
                st.write("생성된 소설:")
                st.write(novel)
                st.session_state['novel_generated'] = True
                st.session_state['current_novel'] = novel
            else:
                st.error("소설 생성을 위한 키워드를 입력해주세요.")

    elif option == "문장 기반 소설 생성":
        sentence_input = st.text_area("소설 생성을 위한 문장을 입력하세요:", "")
        if st.button("소설 생성", key="sentence_generate"):
            if sentence_input:
                prompt = f"다음 문장을 기반으로 흥미롭고 창의적인 소설을 작성해 주세요: {sentence_input}. 자유롭게 상상력을 발휘해 주세요."
                st.write("문장을 기반으로 소설을 생성하고 있습니다...")
                novel = generate_text(prompt)
                st.write("생성된 소설:")
                st.write(novel)
                st.session_state['novel_generated'] = True
                st.session_state['current_novel'] = novel
            else:
                st.error("소설 생성을 위한 문장을 입력해주세요.")

    # 기존 소설 수정 기능은 소설이 한 번 생성된 후에만 사용 가능
    if st.session_state['novel_generated']:
        st.subheader("기존 소설 수정")
        modification_instruction = st.text_area("수정을 위한 지시 사항을 입력하세요:", "")
        if st.button("소설 수정", key="modify_novel"):
            if modification_instruction:
                prompt = f"다음 소설을 수정해 주세요:\n\n{st.session_state['current_novel']}\n\n지시 사항: {modification_instruction}"
                st.write("소설을 수정하고 있습니다...")
                modified_novel = generate_text(prompt, max_tokens=3000, temperature=0.7)
                st.write("수정된 소설:")
                st.write(modified_novel)
                st.session_state['current_novel'] = modified_novel
            else:
                st.error("수정을 위한 지시 사항을 입력해주세요.")

        # 소설 다운로드 버튼
        if st.button("소설 다운로드", key="download_novel"):
            st.download_button(
                label="다운로드",
                data=st.session_state['current_novel'],
                file_name="novel.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    main()
