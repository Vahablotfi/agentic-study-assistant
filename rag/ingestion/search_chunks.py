import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD")),
)

EMBEDDING_MODEL = "text-embedding-3-small"


def create_embedding(text: str):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )
    return response.data[0].embedding


def search(query_text: str, top_k: int = 5):
    query_embedding = create_embedding(query_text)

    cypher = """
    CALL db.index.vector.queryNodes('chunk_embedding_index', $top_k, $embedding)
    YIELD node, score
    RETURN node.text AS text,
    node.sourceFile AS sourceFile,
    node.weekNumber AS weekNumber,
    score
    ORDER BY score DESC
    """

    with driver.session() as session:
        results = session.run(
            cypher,
            top_k=top_k,
            embedding=query_embedding,
        )

        for record in results:
            print("=" * 80)
            print(f"Score: {record['score']}")
            print(f"Week: {record['weekNumber']}")
            print(f"Source: {record['sourceFile']}")
            print(record["text"])
            print()


if __name__ == "__main__":
    user_query = input("Ask a study question: ")
    search(user_query)
    driver.close()