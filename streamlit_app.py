import streamlit as st
from PyPDF2 import PdfMerger
from streamlit_sortables import sort_items
import tempfile

# Streamlit 앱 제목
st.title("PDF 병합 앱")

# 파일 업로드 섹션
uploaded_files = st.file_uploader(
    "병합할 PDF 파일을 업로드하세요. (여러 파일 선택 가능)",
    type="pdf",
    accept_multiple_files=True
)

if uploaded_files:
    # 사용자에게 파일 이름 순서를 정렬하도록 제공
    file_names = [file.name for file in uploaded_files]
    st.write("파일 순서를 변경하려면 아래 리스트를 드래그 앤 드롭하세요.")
    sorted_files = sort_items(file_names)

    # 사용자가 정렬한 순서를 보여줌
    st.write("현재 정렬 순서:")
    for index, file_name in enumerate(sorted_files, start=1):
        st.write(f"{index}. {file_name}")

    # PDF 병합 버튼
    if st.button("PDF 병합"):
        try:
            merger = PdfMerger()
            sorted_uploaded_files = [
                next(file for file in uploaded_files if file.name == name)
                for name in sorted_files
            ]

            for pdf_file in sorted_uploaded_files:
                merger.append(pdf_file)

            # 병합된 PDF 임시 저장
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                merger.write(temp_file.name)
                merger.close()

                # 병합된 파일 다운로드 제공
                with open(temp_file.name, "rb") as merged_pdf:
                    st.download_button(
                        label="병합된 PDF 다운로드",
                        data=merged_pdf,
                        file_name="merged.pdf",
                        mime="application/pdf"
                    )

        except Exception as e:
            st.error(f"PDF 병합 중 오류가 발생했습니다: {e}")
