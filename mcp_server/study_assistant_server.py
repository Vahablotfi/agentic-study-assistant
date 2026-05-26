from mcp.server.fastmcp import FastMCP

from rag.ask_study_assistant import retrieve_chunks, generate_answer
from rag.generate_flashcards import (
    retrieve_chunks as retrieve_flashcard_chunks,
    generate_flashcards,
    send_flashcards_to_n8n,
)
from rag.summarise_week_materials import summarise_week_materials
from graph.neo4j.query_concepts import route_graph_question

mcp = FastMCP("Agentic Study Assistant")


@mcp.tool()
def ping() -> str:
    return "MCP server is working."


@mcp.tool()
def ask_study_question(question: str) -> str:
    chunks = retrieve_chunks(question)

    if not chunks:
        return "No relevant course material was found."

    return generate_answer(question, chunks)


@mcp.tool()
def query_concept_graph(question: str) -> str:
    return route_graph_question(question)


@mcp.tool()
def send_flashcards_to_telegram(topic: str) -> str:
    chunks = retrieve_flashcard_chunks(topic)

    if not chunks:
        return f"No relevant course material was found for topic: {topic}"

    flashcards = generate_flashcards(topic, chunks)
    send_flashcards_to_n8n(topic, flashcards)

    return f"Flashcards for '{topic}' were generated and sent to Telegram through n8n."


@mcp.tool()
def summarise_week(week_number: int) -> str:
    return summarise_week_materials(week_number)


if __name__ == "__main__":
    mcp.run()


