"""
query_concepts.py

Small GraphRAG helper script.

Purpose:
- Query concept relationships from Neo4j.
- Show how graph structure can support study questions.
- Demonstrate meaningful Graph RAG separate from Vector RAG.

Examples:
- What should I study before Graph RAG?
- What concepts are related to MCP?
- What concepts were introduced in Week 7?
"""

import os
import re
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD")),
)


def get_required_concepts(concept_name: str) -> list[str]:
    """
    Return prerequisite concepts for a given concept.

    Example:
    Graph RAG -> requires -> Vector RAG
    Vector RAG -> requires -> Embedding
    """
    query = """
    MATCH (c:Concept)-[:REQUIRES]->(required:Concept)
    WHERE toLower(c.name) CONTAINS toLower($concept_name)
    RETURN required.name AS name
    """

    with driver.session() as session:
        result = session.run(query, concept_name=concept_name)
        return [record["name"] for record in result]


def get_related_concepts(concept_name: str) -> list[str]:
    """
    Return concepts directly related to the requested concept.
    """
    query = """
    MATCH (c:Concept)-[:RELATED_TO]-(related:Concept)
    WHERE toLower(c.name) CONTAINS toLower($concept_name)
    RETURN related.name AS name
    """

    with driver.session() as session:
        result = session.run(query, concept_name=concept_name)
        return [record["name"] for record in result]


def get_week_concepts(week_number: int) -> list[str]:
    """
    Return concepts connected to a specific course week.
    """
    query = """
    MATCH (w:Week {weekNumber: $week_number})-[:HAS_CONCEPT]->(concept:Concept)
    RETURN concept.name AS name
    ORDER BY concept.name
    """

    with driver.session() as session:
        result = session.run(query, week_number=week_number)
        return [record["name"] for record in result]


def extract_week_number(question: str) -> int | None:
    """
    Extract week number from questions like:
    - What did we learn in week 7?
    - Summarize Week 8
    """
    match = re.search(r"week\s*(\d+)", question.lower())
    if match:
        return int(match.group(1))
    return None


def extract_known_concept(question: str) -> str:
    """
    Simple concept detection.

    This is intentionally basic for the prototype.
    Later, the agent can use an LLM/tool router for smarter intent detection.
    """
    known_concepts = [
        "Graph RAG",
        "Vector RAG",
        "Embedding",
        "Neo4j",
        "Model Context Protocol",
        "MCP",
        "n8n",
        "AI Agent",
        "LLM",
        "Workflow Automation",
    ]

    question_lower = question.lower()

    for concept in known_concepts:
        if concept.lower() in question_lower:
            return concept

    return question


def route_graph_question(question: str) -> str:
    """
    Decide which graph function to call based on the question.

    This is a simple rule-based router:
    - prerequisite questions call get_required_concepts()
    - related/connected questions call get_related_concepts()
    - week questions call get_week_concepts()
    """
    question_lower = question.lower()

    week_number = extract_week_number(question)
    concept = extract_known_concept(question)

    if week_number and any(word in question_lower for word in ["week", "learn", "covered", "introduced"]):
        concepts = get_week_concepts(week_number)
        return f"Concepts introduced in Week {week_number}: {', '.join(concepts)}"

    if any(phrase in question_lower for phrase in ["before", "prerequisite", "requires", "need to know"]):
        concepts = get_required_concepts(concept)
        if not concepts:
            return f"No prerequisite concepts found for {concept}."
        return f"To understand {concept}, you should first understand: {', '.join(concepts)}"

    if any(word in question_lower for word in ["related", "connected", "connection", "relationship"]):
        concepts = get_related_concepts(concept)
        if not concepts:
            return f"No related concepts found for {concept}."
        return f"Concepts related to {concept}: {', '.join(concepts)}"

    return "I could not identify a graph-based query. Try asking about prerequisites, related concepts, or a specific week."


if __name__ == "__main__":
    try:
        question = input("Ask a graph study question: ")
        answer = route_graph_question(question)
        print("\nGRAPH ANSWER")
        print("=" * 80)
        print(answer)
    finally:
        driver.close()