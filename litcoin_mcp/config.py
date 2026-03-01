import os
from pydantic import BaseModel
from dotenv import load_dotenv


load_dotenv()

class Settings(BaseModel):
    neo4j_uri: str
    neo4j_user: str
    neo4j_password: str
    openai_api_key: str
    embedding_model: str = "text-embedding-3-small"
    edge_vector_index: str = "edge_embedding_index"
    node_vector_index: str = "node_embedding_index"


def get_settings() -> Settings:
    return Settings(
        neo4j_uri=os.getenv("NEO4J_URI"),
        neo4j_user=os.getenv("NEO4J_USERNAME"),
        neo4j_password=os.getenv("NEO4J_PASSWORD"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )