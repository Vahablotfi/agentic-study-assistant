# Step 06 — Hermes Skill for Natural Language Routing

A custom Hermes skill was created to improve the user experience of the Telegram study assistant.

Without the skill, users had to explicitly reference MCP tools using technical prompts such as:

"Use the study_assistant MCP server to summarise week 3."

The custom skill allows users to interact more naturally with the system using prompts like:

- "summarise week 3"
- "make flashcards about MCP"
- "what is the difference between an LLM and an AI agent?"

The skill provides routing instructions to Hermes so it can automatically select the correct MCP tool based on user intent.

## Tool Routing Rules

- Week summaries → `mcp_study_assistant_summarise_week`
- Flashcard generation → `mcp_study_assistant_send_flashcards_to_telegram`
- General study questions → `mcp_study_assistant_ask_study_question`
- Relationship/prerequisite questions → `mcp_study_assistant_query_concept_graph`

The skill also improves Telegram response formatting by encouraging concise summaries, bullet points and exam-focused explanations.

This improves the overall agentic behavior of the system because the user no longer needs to know the internal tool architecture.