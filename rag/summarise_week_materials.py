"""
summarise_week_materials.py

Generates a study summary for a specific course week.

Flow:
1. User provides a week number.
2. The script retrieves all chunks from Neo4j for that week.
3. The chunks are passed to an OpenAI chat model.
4. The model creates a clear study summary.

This supports the MVP tool:
summarise_week_materials(week_number)
"""

import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from openai import OpenAI

load_dotenv()

CHAT_MODEL = "gpt-4o-mini"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD")),
)


def get_week_chunks(week_number: int) -> list[dict]:
    """
    Retrieve all chunks that belong to a specific week.
    """
    query = """
    MATCH (c:Chunk)
    WHERE c.weekNumber = $week_number
    RETURN c.text AS text,
           c.sourceFile AS sourceFile,
           c.weekNumber AS weekNumber
    ORDER BY c.sourceFile, c.chunkIndex
    """

    with driver.session() as session:
        results = session.run(query, week_number=week_number)
        return [dict(record) for record in results]


def build_week_context(chunks: list[dict]) -> str:
    """
    Combine week chunks into one context string for the LLM.
    """
    context_parts = []

    for i, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"""
SOURCE {i}
File: {chunk["sourceFile"]}

{chunk["text"]}
"""
        )

    return "\n\n".join(context_parts)


def summarise_week_materials(week_number: int) -> str:
    """
    Generate a structured summary of a course week.
    """
    chunks = get_week_chunks(week_number)

    if not chunks:
        return f"No course material found for Week {week_number}."

    context = build_week_context(chunks)

    system_prompt = """
You are an AI study assistant for a computer science student.

Create a clear study summary from the provided course material.

Focus on:
- what the week was about,
- key concepts,
- new tools or technologies introduced,
- why the week matters for the exam project,
- what the student should review.

Do not invent information that is not supported by the context.
Use simple language.
"""

    user_prompt = f"""
Course week:
Week {week_number}

Course material context:
{context}

Create a useful study summary for this week.
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


def main():
    """
    Terminal test interface.
    """
    try:
        week_number = int(input("Enter week number: "))
        summary = summarise_week_materials(week_number)

        print("\nWEEK SUMMARY")
        print("=" * 80)
        print(summary)

    finally:
        driver.close()


if __name__ == "__main__":
    main()