"""
generate_flashcards.py

This script generates study flashcards using Vector RAG.

Flow:
1. User requests flashcards for a topic.
2. Relevant chunks are retrieved from Neo4j.
3. Retrieved context is sent to OpenAI.
4. The LLM generates question-answer flashcards.

This demonstrates:
- Retrieval-Augmented Generation (RAG)
- educational AI assistance
- practical use of retrieved course material
"""

import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from openai import OpenAI
import requests

load_dotenv()

# Models
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"

# Neo4j vector index
VECTOR_INDEX_NAME = "chunk_embedding_index"

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Neo4j connection
driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD")),
)


def create_embedding(text: str) -> list[float]:
    """
    Convert text into embedding vector.
    """
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )

    return response.data[0].embedding


def retrieve_chunks(topic: str, top_k: int = 5) -> list[dict]:
    """
    Retrieve relevant course chunks related to the requested topic.
    """
    topic_embedding = create_embedding(topic)

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
            embedding=topic_embedding,
        )

        return [dict(record) for record in results]


def build_context(chunks: list[dict]) -> str:
    """
    Combine retrieved chunks into one context string.
    """
    context_parts = []

    for chunk in chunks:
        context_parts.append(
            f"""
Week: {chunk["weekNumber"]}
Source: {chunk["sourceFile"]}

{chunk["text"]}
"""
        )

    return "\n\n".join(context_parts)


def generate_flashcards(topic: str, chunks: list[dict]) -> str:
    """
    Generate flashcards from retrieved course material.
    """
    context = build_context(chunks)

    system_prompt = """
You are an AI study assistant.

Generate clear and useful flashcards from the provided course material.

Rules:
- Focus on important exam concepts.
- Keep answers concise but informative.
- Avoid inventing information not present in the context.
- Create flashcards useful for computer science students.
- Format output clearly.

Use this format:

FLASHCARD 1
Question:
...

Answer:
...

FLASHCARD 2
...
"""

    user_prompt = f"""
Topic:
{topic}

Course material context:
{context}

Generate 5 high-quality study flashcards.
"""

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content


def send_flashcards_to_n8n(topic: str, flashcards: str) -> None:
    """
    Send generated flashcards to an n8n webhook.

    This demonstrates workflow automation:
    Python/RAG generates study material, then n8n receives it and can forward,
    save, or process it.
    """
    webhook_url = os.getenv("N8N_FLASHCARD_WEBHOOK_URL")

    if not webhook_url:
        print("N8N_FLASHCARD_WEBHOOK_URL is not set. Skipping n8n send.")
        return

    payload = {
        "topic": topic,
        "flashcards": flashcards,
        "source": "agentic-study-assistant",
    }

    response = requests.post(webhook_url, json=payload, timeout=10)
    response.raise_for_status()

    print("Flashcards sent to n8n successfully.")

def main():
    """
    Main flashcard generation workflow.
    """
    try:
        topic = input("Enter flashcard topic: ")

        print("\nRetrieving relevant course material...\n")

        chunks = retrieve_chunks(topic)

        if not chunks:
            print("No relevant chunks found.")
            return

        print("Generating flashcards...\n")

        flashcards = generate_flashcards(topic, chunks)

        print("=" * 80)
        print("FLASHCARDS")
        print("=" * 80)

        print(flashcards)
        send_flashcards_to_n8n(topic, flashcards)

    finally:
        driver.close()


if __name__ == "__main__":
    main()