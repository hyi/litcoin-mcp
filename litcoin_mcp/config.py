import os
from pydantic import BaseModel
from dotenv import load_dotenv


load_dotenv()

NODE_LABELS = [
        "biolink:Disease",
        "biolink:Drug",
        "biolink:PhenotypicFeature",
        "biolink:Gene",
        "biolink:Protein",
        "biolink:ChemicalOrDrugOrTreatment",
    ]

RELATIONSHIP_TYPES = [
    "biolink:related_to",
    "biolink:associated_with",
    "biolink:correlated_with",
    "biolink:positively_correlated_with",
    "biolink:genetically_associated_with",
    "biolink:contributes_to",
    "biolink:causes",
    "biolink:affects",
    "biolink:regulates",

    "biolink:treats",
    "biolink:studied_to_treat",
    "biolink:treats_or_applied_or_studied_to_treat",
    "biolink:ameliorates_condition",
    "biolink:exacerbates_condition",
    "biolink:preventative_for_condition",

    "biolink:affects_response_to",
    "biolink:increases_response_to",
    "biolink:decreases_response_to",
    "biolink:associated_with_resistance_to"
]


class Settings(BaseModel):
    neo4j_uri: str
    neo4j_user: str
    neo4j_password: str
    openai_api_key: str
    embedding_model: str = "text-embedding-3-small"

def get_settings() -> Settings:
    return Settings(
        neo4j_uri=os.getenv("NEO4J_URI"),
        neo4j_user=os.getenv("NEO4J_USERNAME"),
        neo4j_password=os.getenv("NEO4J_PASSWORD"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )
