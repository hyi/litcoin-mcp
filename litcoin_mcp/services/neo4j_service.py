from neo4j import GraphDatabase
from typing import Any, Dict, List


class Neo4jService:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def run_query(self, query: str, parameters: Dict[str, Any]) -> List[Dict[str, Any]]:
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record.data() for record in result]

    def close(self):
        self.driver.close()
