import streamlit as st
from PyPDF2 import PdfMerger
from io import BytesIO

# Streamlit 앱 제목
st.title("PDF 병합 앱")
st.write("여러 PDF 파일을 드래그 앤 드롭으로 선택하고 하나로 병합하세요!")

# 파일 업로드
uploaded_files = st.file_uploader(
    "PDF 파일을 드래그 앤 드롭하세요.", 
    type="pdf", 
    accept_multiple_files=True
)

if uploaded_files:
    # PDF 병합 버튼
    if st.button("PDF 병합하기"):
        merger = PdfMerger()
        
        for uploaded_file in uploaded_files:
            # 파일을 BytesIO 객체로 읽기
            pdf_data = BytesIO(uploaded_file.read())
            merger.append(pdf_data)

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
