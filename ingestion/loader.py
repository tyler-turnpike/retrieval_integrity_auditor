from typing import List, Dict
import fitz  # PyMuPDF


def load_uploaded_pdf(uploaded_file) -> List[Dict]:
    """
    Load PDF uploaded via Streamlit and extract text page-wise.
    """
    documents = []

    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    file_name = uploaded_file.name

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text().strip()

        if text:
            documents.append({
                "text": text,
                "metadata": {
                    "source": file_name,
                    "page": page_num + 1
                }
            })

    return documents
