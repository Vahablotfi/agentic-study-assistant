# Agentic Study Assistant

An AI-powered study assistant built with Hermes Agent, MCP, Neo4j, Vector RAG, GraphRAG, n8n, and Telegram integration.

The project was developed as the final project for the AI Agents and Automation course.

---

## Features

* Study question answering using Vector RAG
* Concept relationship retrieval using GraphRAG
* Week material summarisation
* Flashcard generation
* Telegram conversational interface
* Hermes Agent orchestration
* MCP-based tool exposure
* n8n workflow automation

---

## Example User Interactions

Users can interact naturally through Telegram:

* `summarise week 3`
* `make flashcards about MCP`
* `what is the difference between an LLM and an AI agent?`
* `what should I learn before GraphRAG?`

The agent automatically selects the correct MCP tool and returns responses through Telegram.

---

## System Architecture

`Telegram User`
↓
`Hermes Gateway`
↓
`Hermes Agent (gpt-5-mini)`
↓
`MCP Server`
↓
`Vector RAG / GraphRAG / n8n Workflow`
↓
`Neo4j / OpenAI / Telegram automation`

---

## Main Technologies

| Technology   | Purpose                   |
| ------------ | ------------------------- |
| Hermes Agent | Agent orchestration       |
| MCP          | Tool interface layer      |
| Neo4j        | Vector and graph database |
| OpenAI API   | Embeddings and generation |
| n8n          | Workflow automation       |
| Telegram     | User interface            |
| Python       | Backend logic             |

---

## Main Components

### Vector RAG

Lecture materials are extracted from PDFs, cleaned, chunked, embedded with OpenAI embeddings, and stored in Neo4j.

Semantic search retrieves relevant chunks for answering study questions.

### GraphRAG

Concepts and relationships are stored in Neo4j as graph structures.

This allows the assistant to answer questions about prerequisites, related concepts, and course structure.

### MCP Server

The MCP server exposes the study assistant functions as tools.

Main MCP tools include:

* `ask_study_question`
* `send_flashcards_to_telegram`
* `summarise_week`
* `query_concept_graph`

### Hermes Agent

Hermes acts as the reasoning and orchestration layer.

It interprets user requests and decides which MCP tool should be used.

### Telegram Interface

Telegram is used as the conversational user interface.

The user can ask natural language questions and receive answers directly in Telegram.

### n8n Workflow

n8n is used for workflow automation.

In the current prototype, generated flashcards are sent through an n8n webhook and delivered to the user via Telegram.

---

## Setup

### Clone repository

`git clone <repo-url>`

`cd agentic-study-assistant`

### Create virtual environment

`python -m venv .venv`

`source .venv/bin/activate`

### Install dependencies

`pip install -r requirements.txt`

### Required Services

* Neo4j Desktop
* n8n
* OpenAI API key
* Hermes Agent
* Telegram bot

---

## Example Workflow

Example user message:

`make flashcards about MCP`

Flow:

1. Telegram receives the message.
2. Hermes Gateway forwards the message to Hermes Agent.
3. Hermes Agent selects the flashcard MCP tool.
4. Vector RAG retrieves relevant course chunks from Neo4j.
5. OpenAI generates flashcards.
6. n8n sends the flashcards back through Telegram.

---

## Project Structure

* `docs/` — architecture notes, report notes, and project documentation
* `graph/` — Neo4j graph scripts and concept queries
* `mcp_server/` — MCP server exposing study assistant tools
* `rag/` — ingestion, retrieval, summarisation, and flashcard generation
* `workflows/` — n8n workflow exports
* `prompts/` — prompts and skills used in the project
* `telegram/` — Telegram-related integration notes or scripts

---

## Future Improvements

* Better GraphRAG topic extraction
* User-uploaded documents
* Persistent user memory
* Multi-user support
* Improved natural language routing
* Local LLM support
* Advanced study planning
* Better progress tracking

---

## Project Status

Working MVP completed:

* Vector RAG
* GraphRAG
* MCP integration
* Hermes integration
* Telegram interface
* n8n automation
* Flashcard workflow
