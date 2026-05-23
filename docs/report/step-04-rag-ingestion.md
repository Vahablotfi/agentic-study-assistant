# Step 04 — Initial RAG Ingestion

The first step of the Vector RAG pipeline was implemented by extracting text from uploaded lecture PDFs.

A Python ingestion script scans the local lecture-materials directory and extracts text from all PDF files using the `pypdf` library.

This extracted text will later be:

- chunked into smaller segments,
- converted into embeddings,
- stored in Neo4j for Vector RAG retrieval.
