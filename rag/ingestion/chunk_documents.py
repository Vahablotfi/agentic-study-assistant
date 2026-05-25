import re
from pathlib import Path
from pypdf import PdfReader

PDF_FOLDER = Path("lecture-materials")
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 0


def clean_text(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)

    # Fix excessive single-word line breaks from PDF extraction
    text = re.sub(r"\n([a-zA-Z])\n", r" \1 ", text)

    # Keep paragraph breaks, but remove too many empty lines
    text = re.sub(r"\n{3,}", "\n\n", text)

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
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) <= chunk_size:
            current_chunk += paragraph + "\n\n"
        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())

            # Start new chunk with overlap from previous chunk
            if overlap > 0 and chunks:
                previous = chunks[-1]
                overlap_text = previous[-overlap:]
                current_chunk = overlap_text + "\n\n" + paragraph + "\n\n"
            else:
                current_chunk = paragraph + "\n\n"

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

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