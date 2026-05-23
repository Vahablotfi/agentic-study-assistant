# Graph Model

## Purpose

The graph model supports an agentic study assistant that helps students retrieve course content, understand concept relationships, generate flashcards and track study progress.

## Node Types

- `Week`: represents a course week.
- `Concept`: represents a key idea from the course.
- `Chunk`: represents a text chunk used for Vector RAG.
- `Flashcard`: represents a generated study card.
- `User`: represents the student using the assistant.

## Relationships

- `Week HAS_CONCEPT Concept`
- `Concept REQUIRES Concept`
- `Concept RELATED_TO Concept`
- `Chunk BELONGS_TO_WEEK Week`
- `Chunk MENTIONS Concept`
- `Flashcard TESTS Concept`
- `User HAS_PROGRESS Concept`
