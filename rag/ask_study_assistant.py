"""
ask_study_assistant.py

This script is the first complete Vector RAG prototype for the project.

Flow:
1. The user asks a study question.
2. The question is converted into an embedding.
3. Neo4j vector search retrieves the most relevant course chunks.
4. The retrieved chunks are passed to an OpenAI chat model.
5. The model generates a study-focused answer based on the retrieved material.

This script proves the core RAG flow:
Question → Retrieval → Context → Generation → Answer
"""

import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from openai import OpenAI

# Load environment variables from .env
# This keeps API keys and database credentials out of the source code.
load_dotenv()

# Embedding model used for vector search.
# This must match the model used in ingest_to_neo4j.py.
EMBEDDING_MODEL = "text-embedding-3-small"

# Chat model used to generate the final study answer.
CHAT_MODEL = "gpt-4o-mini"

# Name of the Neo4j vector index created during ingestion.
VECTOR_INDEX_NAME = "chunk_embedding_index"

# Create OpenAI client.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create Neo4j database driver.
driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD")),
)


def create_embedding(text: str) -> list[float]:
    """
    Convert input text into a vector embedding.

    The same embedding model must be used for:
    - storing document chunks in Neo4j
    - embedding the user's question

    Otherwise, vector similarity search will not work correctly.

    Args:
        text: The text to embed.

    Returns:
        A list of floating point numbers representing the embedding.
    """
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )
    return response.data[0].embedding


def retrieve_chunks(question: str, top_k: int = 5) -> list[dict]:
    """
    Retrieve the most relevant course chunks from Neo4j using vector search.

    Steps:
    1. Convert the user's question into an embedding.
    2. Query Neo4j's vector index.
    3. Return the most similar chunks with source metadata.

    Args:
        question: The user's study question.
        top_k: Number of chunks to retrieve.

    Returns:
        A list of dictionaries containing chunk text, source file, week number and score.
    """
    question_embedding = create_embedding(question)

    cypher = """
    CALL db.index.vector.queryNodes($index_name, $top_k, $embedding)
    YIELD node, score
    RETURN node.text AS text,
    node.sourceFile AS sourceFile,
    node.weekNumber AS weekNumber,
    score
    ORDER BY score DESC
    """

    with driver.session() as session:
        results = session.run(
            cypher,
            index_name=VECTOR_INDEX_NAME,
            top_k=top_k,
            embedding=question_embedding,
        )

        return [dict(record) for record in results]


def build_context(chunks: list[dict]) -> str:
    """
    Convert retrieved chunks into a single context string for the LLM.

    The LLM receives this context together with the user's question.
    Source metadata is included so the model can mention where the answer is based.

    Args:
        chunks: Retrieved chunks from Neo4j.

    Returns:
        A formatted context string.
    """
    context_parts = []

    for i, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"""
SOURCE {i}
Week: {chunk["weekNumber"]}
File: {chunk["sourceFile"]}
Relevance score: {chunk["score"]}

{chunk["text"]}
"""
        )

    return "\n\n".join(context_parts)


def generate_answer(question: str, chunks: list[dict]) -> str:
    """
    Generate a study-focused answer using retrieved course material.

    This is the 'generation' part of RAG.
    The model is instructed to answer only from the provided context and avoid inventing
    unsupported course-specific details.

    Args:
        question: The user's study question.
        chunks: Relevant chunks retrieved from Neo4j.

    Returns:
        The generated answer as text.
    """
    context = build_context(chunks)

    system_prompt = """
You are an AI study assistant for a computer science student.

Use the provided course material context to answer the student's question.
Explain concepts clearly and simply.
Focus on exam understanding.

Important rules:
- Base your answer on the provided context.
- Do not invent course-specific details.
- If the context does not contain enough information, say so.
- When useful, mention which week or source the answer is mainly based on.
"""

    user_prompt = f"""
Question:
{question}

Course material context:
{context}

Answer:
"""

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


def print_sources(chunks: list[dict]) -> None:
    """
    Print the retrieved sources used for the answer.

    This helps debugging and makes the RAG process transparent.
    """
    print("\nSOURCES")
    print("=" * 80)

    for chunk in chunks:
        print(
            f"- Week {chunk['weekNumber']} | "
            f"{chunk['sourceFile']} | "
            f"score: {chunk['score']:.3f}"
        )


def ask(question: str) -> None:
    """
    Main study assistant function.

    This function connects the full RAG flow:
    question → retrieve chunks → generate answer → print answer and sources.
    """
    chunks = retrieve_chunks(question)

    if not chunks:
        print("No relevant chunks were found.")
        return

    answer = generate_answer(question, chunks)

    print("\nANSWER")
    print("=" * 80)
    print(answer)

    print_sources(chunks)


if __name__ == "__main__":
    try:
        question = input("Ask a study question: ")
        ask(question)
    finally:
        # Always close the Neo4j driver when the script finishes.
        driver.close()