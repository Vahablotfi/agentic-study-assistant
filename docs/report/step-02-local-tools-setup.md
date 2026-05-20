# Step 02 — Local Tools Setup

The project uses Neo4j Desktop as the local graph database environment.

Neo4j will be used for:

- Vector RAG: storing document chunks and embeddings.
- Graph RAG: storing relationships between courses, lectures, concepts, requirements and study tasks.

The local Neo4j database was started and tested through Neo4j Browser.

Test query:

```cypher
RETURN "Neo4j is working" AS message;

## n8n

The project uses n8n for workflow automation.

n8n will be used to trigger study-related workflows, such as:
- saving generated flashcards,
- sending study reminders,
- creating weekly study summaries,
- logging generated study tasks.

n8n is running locally through Docker and can be accessed at:

```text
http://localhost:5678