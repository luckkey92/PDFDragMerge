import streamlit as st
from PyPDF2 import PdfMerger
from io import BytesIO

# Streamlit 앱 제목
st.title("PDF 병합 앱")
st.write("파일을 업로드하고 병합 순서를 설정하세요!")

# 파일 업로드
uploaded_files = st.file_uploader("PDF 파일을 선택하세요.", type="pdf", accept_multiple_files=True)

if uploaded_files:
    # 업로드된 파일의 이름과 데이터 저장
    file_data = {uploaded_file.name: BytesIO(uploaded_file.read()) for uploaded_file in uploaded_files}
    
    # 파일 순서 입력을 위한 순서 지정 기능
    file_names = list(file_data.keys())
    order = st.text_area(
        "파일 병합 순서를 입력하세요 (파일 이름을 줄 단위로 나열):",
        value="\n".join(file_names)
    ).splitlines()

    if st.button("PDF 병합하기"):
        # 순서에 따라 PDF 병합
        merger = PdfMerger()
        for file_name in order:
            if file_name in file_data:
                merger.append(file_data[file_name])

        # 병합된 PDF 저장
        output_pdf = BytesIO()
        merger.write(output_pdf)
        merger.close()
        output_pdf.seek(0)

        # 다운로드 링크 제공
        st.success("PDF 병합이 완료되었습니다!")
        st.download_button(
            label="병합된 PDF 다운로드",
            data=output_pdf,
            file_name="merged.pdf",
            mime="application/pdf"
        )
    else:
        st.info("병합 순서를 확인 후 'PDF 병합하기'를 클릭하세요.")
