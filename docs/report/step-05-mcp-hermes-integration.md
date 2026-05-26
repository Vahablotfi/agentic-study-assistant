# Step 05 — MCP and Hermes Integration

Hermes Agent is used as the agent platform and orchestrator.

The agent calls tools exposed through a local MCP server. The MCP server exposes study assistant functions such as week summaries, study Q&A, graph queries and flashcard generation.

The flashcard workflow demonstrates the complete system flow:

Hermes Agent → MCP tool → Vector RAG retrieval → OpenAI generation → n8n webhook → Telegram message.

This shows that the system is more than a simple chatbot: the agent can call tools and trigger external workflows.