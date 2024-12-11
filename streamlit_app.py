import streamlit as st
from PyPDF2 import PdfMerger
from io import BytesIO

# 제목 설정
st.title("PDF 병합 앱")
st.write("여러 PDF 파일을 드래그 앤 드롭하여 순서를 선택하고 병합하세요.")

# PDF 파일 업로드
uploaded_files = st.file_uploader("PDF 파일을 업로드하세요", accept_multiple_files=True, type="pdf")

if uploaded_files:
    st.write("파일 순서를 조정하려면 드래그 앤 드롭하세요:")

    # 파일 순서 조정 가능하게 리스트 출력
    filenames = [file.name for file in uploaded_files]
    reordered_filenames = st.experimental_data_editor(
        filenames, 
        key="reorder",
        use_container_width=True
    )

    if st.button("병합 시작"):
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
