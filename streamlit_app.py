import streamlit as st
from PyPDF2 import PdfMerger
from io import BytesIO

# Streamlit 앱 제목
st.title("PDF 병합 앱")
st.write("드래그 앤 드롭으로 순서를 정하고 PDF 파일을 병합하세요!")

# 파일 업로드
uploaded_files = st.file_uploader("PDF 파일을 선택하세요.", type="pdf", accept_multiple_files=True)

if uploaded_files:
    # PDF 파일 순서 정렬을 위한 목록
    uploaded_files_names = [uploaded_file.name for uploaded_file in uploaded_files]
    order = st.multiselect(
        "병합 순서를 선택하세요 (드래그 앤 드롭으로 순서를 변경 가능):",
        uploaded_files_names,
        default=uploaded_files_names
    )

    # 선택된 순서대로 파일 병합
    if st.button("PDF 병합하기"):
        merger = PdfMerger()

        # 순서에 맞게 파일 병합
        for file_name in order:
            for uploaded_file in uploaded_files:
                if uploaded_file.name == file_name:
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
