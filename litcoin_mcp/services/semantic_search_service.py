from typing import List, Dict


class SemanticSearchService:
    def __init__(self, neo4j_service, embedding_service, edge_index, node_index):
        self.neo4j = neo4j_service
        self.embedding = embedding_service
        self.edge_index = edge_index
        self.node_index = node_index

    def search_edges(self, query: str, top_k: int) -> List[Dict]:
        embedding = self.embedding.embed(query)

        cypher = """
        CALL db.index.vector.queryNodes(
            $index_name,
            $top_k,
            $embedding
        )
        YIELD node, score
        RETURN node.id AS edge_id,
               node.source AS source_id,
               node.target AS target_id,
               node.predicate AS predicate,
               score
        """

        return self.neo4j.run_query(
            cypher,
            {
                "index_name": self.edge_index,
                "top_k": top_k,
                "embedding": embedding,
            },
        )

    def search_nodes(self, query: str, top_k: int) -> List[Dict]:
        embedding = self.embedding.embed(query)

        cypher = """
        CALL db.index.vector.queryNodes(
            $index_name,
            $top_k,
            $embedding
        )
        YIELD node, score
        RETURN node.id AS node_id,
               node.name AS name,
               labels(node) AS labels,
               score
        """

        return self.neo4j.run_query(
            cypher,
            {
                "index_name": self.node_index,
                "top_k": top_k,
                "embedding": embedding,
            },
        )
