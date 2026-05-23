import re
from pathlib import Path
from pypdf import PdfReader

PDF_FOLDER = Path("lecture-materials")
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


def clean_text(text: str) -> str:
    # Replace many spaces/tabs with one space
    text = re.sub(r"[ \t]+", " ", text)

    # Replace too many newlines with max two
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove spaces around newlines
    text = re.sub(r" *\n *", "\n", text)

    return text.strip()


def extract_week_number(path: Path) -> int | None:
    match = re.search(r"week\s*(\d+)", str(path).lower())
    if match:
        return int(match.group(1))
    return None


def extract_text_from_pdf(pdf_file: Path) -> str:
    reader = PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    return clean_text(text)


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def build_chunks():
    all_chunks = []

    for pdf_file in PDF_FOLDER.rglob("*.pdf"):
        print(f"Processing: {pdf_file}")

        text = extract_text_from_pdf(pdf_file)
        chunks = chunk_text(text)

        week_number = extract_week_number(pdf_file)

        for index, chunk in enumerate(chunks):
            all_chunks.append({
                "id": f"{pdf_file.stem.lower().replace(' ', '_')}_chunk_{index}",
                "text": chunk,
                "source_file": str(pdf_file),
                "week_number": week_number,
                "chunk_index": index,
            })

    return all_chunks


if __name__ == "__main__":
    chunks = build_chunks()

    print(f"\nCreated {len(chunks)} chunks.\n")

    for chunk in chunks[:3]:
        print("=" * 60)
        print(f"ID: {chunk['id']}")
        print(f"Source: {chunk['source_file']}")
        print(f"Week: {chunk['week_number']}")
        print(chunk["text"][:700])
        print()