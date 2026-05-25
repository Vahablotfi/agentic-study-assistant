import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from openai import OpenAI

from chunk_documents import build_chunks

load_dotenv()

EMBEDDING_MODEL = "text-embedding-3-small"
VECTOR_INDEX_NAME = "chunk_embedding_index"
VECTOR_DIMENSIONS = 1536

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD")),
)


def create_embedding(text: str):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )
    return response.data[0].embedding


def create_vector_index():
    query = f"""
    CREATE VECTOR INDEX {VECTOR_INDEX_NAME} IF NOT EXISTS
    FOR (c:Chunk) ON (c.embedding)
    OPTIONS {{
      indexConfig: {{
        `vector.dimensions`: {VECTOR_DIMENSIONS},
        `vector.similarity_function`: 'cosine'
      }}
    }}
    """
    with driver.session() as session:
        session.run(query)
        print(f"Vector index creation requested: {VECTOR_INDEX_NAME}")


def verify_vector_index():
    query = """
    SHOW INDEXES
    YIELD name, type, state, labelsOrTypes, properties
    WHERE name = $index_name
    RETURN name, type, state, labelsOrTypes, properties
    """
    with driver.session() as session:
        result = session.run(query, index_name=VECTOR_INDEX_NAME)
        record = result.single()

        if record is None:
            raise RuntimeError(
                f"Vector index '{VECTOR_INDEX_NAME}' was not found after creation."
            )

        print("Vector index found:")
        print(f"- name: {record['name']}")
        print(f"- type: {record['type']}")
        print(f"- state: {record['state']}")
        print(f"- labels/types: {record['labelsOrTypes']}")
        print(f"- properties: {record['properties']}")


def store_chunk(chunk, embedding):
    query = """
    MERGE (c:Chunk {id: $id})
    SET c.text = $text,
        c.sourceFile = $source_file,
        c.weekNumber = $week_number,
        c.chunkIndex = $chunk_index,
        c.embedding = $embedding

    WITH c
    MERGE (w:Week {weekNumber: $week_number})
    MERGE (c)-[:BELONGS_TO_WEEK]->(w)
    """
    with driver.session() as session:
        session.run(
            query,
            id=chunk["id"],
            text=chunk["text"],
            source_file=chunk["source_file"],
            week_number=chunk["week_number"],
            chunk_index=chunk["chunk_index"],
            embedding=embedding,
        )


def verify_chunks():
    query = """
    MATCH (c:Chunk)
    RETURN count(c) AS chunk_count,
           count(c.embedding) AS chunks_with_embeddings
    """
    with driver.session() as session:
        record = session.run(query).single()

        print("Chunk verification:")
        print(f"- chunks: {record['chunk_count']}")
        print(f"- chunks with embeddings: {record['chunks_with_embeddings']}")


def ingest():
    chunks = build_chunks()
    print(f"Found {len(chunks)} chunks.")

    create_vector_index()
    verify_vector_index()

    for i, chunk in enumerate(chunks, start=1):
        print(f"Embedding chunk {i}/{len(chunks)}: {chunk['id']}")
        embedding = create_embedding(chunk["text"])

        if len(embedding) != VECTOR_DIMENSIONS:
            raise ValueError(
                f"Expected embedding dimension {VECTOR_DIMENSIONS}, got {len(embedding)}"
            )

        store_chunk(chunk, embedding)

    verify_chunks()
    print("Ingestion completed.")


if __name__ == "__main__":
    try:
        ingest()
    finally:
        driver.close()