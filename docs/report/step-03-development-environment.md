## Node.js Update

The original Node.js version was outdated:

- Node.js: 16.14.0
- npm: 8.3.1

Node.js was updated using nvm to improve compatibility with modern AI, MCP and agent tooling.

Updated versions:

- Node.js: 24.15.0
- npm: 11.12.1
- nvm: 0.40.4

## Python Virtual Environment

A Python virtual environment was created in the project folder to isolate project dependencies from the global Python installation.

Initial Python dependencies:

- `openai` for OpenAI API access.
- `neo4j` for communicating with the Neo4j database.
- `python-dotenv` for loading environment variables safely from `.env`.

The dependency list is stored in `requirements.txt` to make the project easier to reproduce.
