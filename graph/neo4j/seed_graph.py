import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(uri, auth=(username, password))


def seed_graph():
    query = """
    MERGE (w7:Week {weekNumber: 7})
    SET w7.title = "Vector RAG and Graph RAG"

    MERGE (w8:Week {weekNumber: 8})
    SET w8.title = "Model Context Protocol"

    MERGE (vector:Concept {id: "concept_vector_rag"})
    SET vector.name = "Vector RAG",
        vector.difficulty = "INTERMEDIATE",
        vector.examKeyTerm = true

    MERGE (graph:Concept {id: "concept_graph_rag"})
    SET graph.name = "Graph RAG",
        graph.difficulty = "INTERMEDIATE",
        graph.examKeyTerm = true

    MERGE (embedding:Concept {id: "concept_embedding"})
    SET embedding.name = "Embedding",
        embedding.difficulty = "BEGINNER",
        embedding.examKeyTerm = true

    MERGE (neo4j:Concept {id: "concept_neo4j"})
    SET neo4j.name = "Neo4j",
        neo4j.difficulty = "INTERMEDIATE",
        neo4j.examKeyTerm = true

    MERGE (mcp:Concept {id: "concept_mcp"})
    SET mcp.name = "Model Context Protocol",
        mcp.difficulty = "INTERMEDIATE",
        mcp.examKeyTerm = true

    MERGE (n8n:Concept {id: "concept_n8n"})
    SET n8n.name = "n8n",
        n8n.difficulty = "BEGINNER",
        n8n.examKeyTerm = true

    MERGE (w7)-[:HAS_CONCEPT]->(vector)
    MERGE (w7)-[:HAS_CONCEPT]->(graph)
    MERGE (w7)-[:HAS_CONCEPT]->(embedding)
    MERGE (w7)-[:HAS_CONCEPT]->(neo4j)

    MERGE (w8)-[:HAS_CONCEPT]->(mcp)
    MERGE (w8)-[:HAS_CONCEPT]->(n8n)

    MERGE (vector)-[:REQUIRES]->(embedding)
    MERGE (graph)-[:REQUIRES]->(vector)
    MERGE (graph)-[:RELATED_TO]->(neo4j)
    MERGE (mcp)-[:RELATED_TO]->(n8n)
    MERGE (mcp)-[:REQUIRES]->(vector)
    """
    with driver.session() as session:
        session.run(query)


if __name__ == "__main__":
    seed_graph()
    print("Graph seed completed.")
    driver.close()