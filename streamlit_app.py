import streamlit as st
from PyPDF2 import PdfMerger
from io import BytesIO

# Streamlit 앱 제목
st.title("PDF 병합 앱")
st.write("파일을 업로드하고 드래그 앤 드롭으로 병합 순서를 설정하세요!")

# 파일 업로드
uploaded_files = st.file_uploader("PDF 파일을 선택하세요.", type="pdf", accept_multiple_files=True)

if uploaded_files:
    # 업로드된 파일의 이름과 데이터 저장
    file_data = {uploaded_file.name: BytesIO(uploaded_file.read()) for uploaded_file in uploaded_files}
    
    # 드래그 앤 드롭 순서 설정
    file_names = list(file_data.keys())
    order = st.experimental_data_editor(
        {"파일 이름": file_names},
        use_container_width=True
    )

    if st.button("PDF 병합하기"):
        # 순서에 따라 PDF 병합
        merger = PdfMerger()
        for file_name in order["파일 이름"]:
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
        st.info("드래그 앤 드롭으로 순서를 조정한 후 'PDF 병합하기'를 클릭하세요.")
