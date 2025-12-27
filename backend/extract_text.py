import io
import pdfplumber

def extract_text_from_file(filename: str, content: bytes) -> str:
    filename = filename.lower()

    if filename.endswith(".pdf"):
        text = ""
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()

    elif filename.endswith(".txt"):
        return content.decode("utf-8", errors="ignore")

    else:
        raise ValueError("Unsupported file type")
