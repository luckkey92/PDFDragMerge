import streamlit as st
from PyPDF2 import PdfMerger
from io import BytesIO

# 제목 설정
st.title("PDF 병합 앱")
st.write("여러 PDF 파일을 드래그 앤 드롭하여 순서를 선택하고 병합하세요.")

# PDF 파일 업로드
uploaded_files = st.file_uploader("PDF 파일을 업로드하세요", accept_multiple_files=True, type="pdf")

if uploaded_files:
    st.write("파일 순서를 조정하려면 목록을 클릭하여 순서를 변경하세요:")

    # 파일 이름 표시 및 순서 변경
    filenames = [file.name for file in uploaded_files]
    reordered_filenames = st.multiselect(
        "파일 순서 지정", options=filenames, default=filenames
    )

    if len(reordered_filenames) != len(filenames):
        st.error("모든 파일을 선택해야 합니다.")
    elif st.button("병합 시작"):
        # 순서대로 파일 병합
        merger = PdfMerger()
        for filename in reordered_filenames:
            for file in uploaded_files:
                if file.name == filename:
                    merger.append(file)

        # 병합된 PDF 저장
        output = BytesIO()
        merger.write(output)
        merger.close()
        output.seek(0)

        # 다운로드 링크 제공
        st.success("PDF 병합이 완료되었습니다!")
        st.download_button(
            label="병합된 PDF 다운로드",
            data=output,
            file_name="merged.pdf",
            mime="application/pdf"
        )
