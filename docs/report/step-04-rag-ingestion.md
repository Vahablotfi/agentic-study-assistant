# Step 04 — Initial RAG Ingestion

The first step of the Vector RAG pipeline was implemented by extracting text from uploaded lecture PDFs.

A Python ingestion script scans the local lecture-materials directory and extracts text from all PDF files using the `pypdf` library.

This extracted text will later be:

- chunked into smaller segments,
- converted into embeddings,
- stored in Neo4j for Vector RAG retrieval.

## Text Cleaning and Chunking

After extracting text from PDFs, the text is lightly cleaned by normalizing whitespace and line breaks. This improves readability and helps produce more useful chunks for retrieval.

The text is then split into overlapping chunks. Chunking is necessary because full lecture documents are too large to embed and retrieve as one unit. Smaller chunks make Vector RAG more precise.

Each chunk stores metadata such as source file, week number and chunk index. This allows the system to filter or explain answers based on where the information came from.

## Embeddings and Vector Search

The processed chunks are converted into vector embeddings using OpenAI's `text-embedding-3-small` embedding model.

Each chunk embedding is stored in Neo4j together with metadata such as:

- source file,
- week number,
- chunk index.

Neo4j vector indexes are used to perform semantic similarity search. This allows the study assistant to retrieve relevant lecture content based on meaning instead of keyword matching.

The current implementation uses:

- OpenAI embeddings (1536 dimensions),
- Neo4j vector indexes,
- semantic chunk retrieval,
- lightweight paragraph-based chunking.

This creates the foundation for Retrieval-Augmented Generation (RAG), where retrieved course material can later be combined with LLM-generated study assistance.
