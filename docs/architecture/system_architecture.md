# System Architecture

## Overview

The Agentic Study Assistant is an AI-powered study system built around Hermes Agent, MCP, Vector RAG, GraphRAG, n8n workflows and Telegram integration.

The system allows users to interact with course materials using natural language through Telegram. Hermes acts as the orchestration layer and selects the appropriate MCP tools depending on the user request.

## High-Level Architecture

Telegram User
        │
        ▼
Hermes Gateway
        │
        ▼
Hermes Agent (gpt-5-mini)
        │
        ▼
MCP Server
        │
 ┌──────┼───────────────────────┐───────────────────────┐
 │                              │                       |
 ▼                              ▼                       ▼
Vector RAG               GraphRAG               n8n Workflow
(Neo4j Vector)           (Neo4j Graph)          Telegram Flashcards
 │                        │
 ▼                        ▼
OpenAI Embeddings     Concept Relationships
&
LLM Responses

## Main Components

### Telegram Interface

Telegram is the main user-facing interface. The student interacts with the assistant by sending natural language messages such as “summarise week 3” or “make flashcards about MCP”. Telegram was chosen because it provides a simple real-world chat interface without requiring a custom frontend.

### Hermes Gateway

Hermes Gateway connects Telegram messages to the Hermes Agent. It receives incoming Telegram messages and sends the agent’s responses back to the user. This makes the system usable as a real conversational assistant.

### Hermes Agent

Hermes Agent is the orchestration layer. It interprets the user’s request, decides which tool is needed, and calls the appropriate MCP tool. This is what makes the system more agentic than a simple LLM chatbot.

### MCP Server

The MCP server exposes the study assistant functions as tools. The main tools include study question answering, week summarisation, concept graph queries and flashcard generation. MCP separates the agent’s reasoning from the concrete implementation of tools.

### Vector RAG

Vector RAG is used to retrieve relevant chunks from uploaded course materials. Lecture PDFs are extracted, cleaned, chunked, embedded and stored in Neo4j. When the user asks a study question, semantic search retrieves the most relevant course content.

### GraphRAG

GraphRAG is used to represent relationships between course concepts. Neo4j stores nodes such as Week, Concept, Chunk and Flashcard, with relationships such as HAS_CONCEPT, REQUIRES, RELATED_TO and MENTIONS. This supports questions about prerequisites, related concepts and course structure.

### n8n Workflow

n8n is used for workflow automation. In the current prototype, generated flashcards are sent through an n8n webhook and delivered to the user via Telegram. This demonstrates how the agent can trigger external automations, not only return text.

### OpenAI APIs

OpenAI is used for embeddings and language generation. The embedding model converts course chunks and user questions into vectors for semantic search. The chat model generates study answers, summaries and flashcards from retrieved course material.

## Example Request Flow

Example: “make flashcards about MCP”

1. The user sends a message in Telegram.
2. Hermes Gateway forwards the message to Hermes Agent.
3. Hermes Agent identifies that the user wants flashcards.
4. Hermes calls the MCP tool `send_flashcards_to_telegram`.
5. The MCP tool retrieves relevant chunks from Neo4j using Vector RAG.
6. OpenAI generates flashcards from the retrieved course material.
7. The MCP tool sends the generated flashcards to the n8n webhook.
8. n8n delivers the flashcards back to the user through Telegram.

## Design Decisions

- Telegram was selected as the primary user interface because it provides a lightweight conversational experience.
- Hermes Agent was used to provide tool orchestration and natural language routing.
- MCP was used to expose tools in a standardized way.
- Neo4j was selected because it supports both Vector RAG and GraphRAG in a single database system.
- n8n was used for workflow automation and Telegram delivery.