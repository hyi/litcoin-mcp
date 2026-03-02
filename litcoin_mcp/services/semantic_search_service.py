from typing import List, Dict


class SemanticSearchService:
    def __init__(self, neo4j_service, embedding_service, node_types, edge_types):
        self.neo4j = neo4j_service
        self.embedding = embedding_service
        self.node_types = node_types
        self.edge_types = edge_types

    @staticmethod
    def get_node_index(label: str) -> str:
        # label can be "Chemical:Drug" or similar
        return f"{label.replace(':', '_')}_idx"

    @staticmethod
    def get_edge_index(rel_type: str) -> str:
        return f"{rel_type.lower()}_vector_idx"

    def search_edges(self, query: str, top_k: int, k_per_index: int = 2) -> List[Dict]:
        embedding = self.embedding.embed(query)

        results = []
        ids_in_results = set()

        for rel_type in self.edge_types:
            index_name = f"{rel_type.lower()}_vector_idx"
            cypher = """
            CALL db.index.vector.queryRelationships(
                $index_name,
                $k_per_index,
                $embedding
            )
            YIELD relationship, score
            RETURN properties(relationship) as properties,
                   score,
                   startNode(relationship).id AS source_id,
                   endNode(relationship).id AS target_id,
                   type(relationship) AS predicate
            """

            records = self.neo4j.run_query(
                cypher,
                {
                    "index_name": index_name,
                    "k_per_index": k_per_index,
                    "embedding": embedding,
                },
            )

            for record in records:
                rel_dict = record["properties"] or {}
                rel_dict.pop("embedding", None)
                rel_dict.pop("semantic_text", None)

                score = record["score"]

                edge_id = rel_dict.get("id")
                if edge_id in ids_in_results:
                    continue

                ids_in_results.add(edge_id)

                results.append({
                    "id": edge_id,
                    "predicate": record["predicate"],
                    "source_id": record["source_id"],
                    "target_id": record["target_id"],
                    "score": score,
                    "properties": rel_dict,
                })

        results = sorted(
            results,
            key=lambda x: x["score"],
            reverse=True
        )

        return results[:top_k]


    def search_nodes(self, query: str, top_k: int, k_per_index: int = 2) -> List[Dict]:
        embedding = self.embedding.embed(query)

        results = []
        names_in_results = []

        for label in self.node_types:
            index_name = self.get_node_index(label)

            cypher = f"""
            CALL db.index.vector.queryNodes("{index_name}", {k_per_index}, $embedding)
            YIELD node, score
            RETURN node, score
            """

            records = self.neo4j.run_query(
                cypher,
                {
                    "embedding": embedding,
                },
            )

            for record in records:
                node = record["node"]
                score = record["score"]

                node_dict = dict(node)
                node_dict.pop("embedding", None)
                node_dict.pop("node_text", None)

                name = node_dict.get("name")
                if name in names_in_results:
                    continue

                names_in_results.append(name)

                results.append({
                    "id": node_dict.get("id"),
                    "name": name,
                    "score": score,
                    "properties": node_dict,
                })

        results = sorted(results, key=lambda x: x["score"], reverse=True)
        return results[:top_k]

