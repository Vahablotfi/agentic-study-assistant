from pathlib import Path
from pypdf import PdfReader

PDF_FOLDER = Path("lecture-materials")


def extract_text_from_pdfs():
    all_text = []

    for pdf_file in PDF_FOLDER.rglob("*.pdf"):
        print(f"Reading: {pdf_file}")

        reader = PdfReader(pdf_file)
        text = ""

        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

        all_text.append({
            "file": str(pdf_file),
            "text": text
        })

    return all_text


if __name__ == "__main__":
    documents = extract_text_from_pdfs()

    for doc in documents:
        print("\n====================")
        print(f"FILE: {doc['file']}")
        print(doc["text"][:1000])