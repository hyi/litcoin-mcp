def register_graph_tools(mcp, neo4j_service):

    @mcp.tool()
    def get_node(node_id: str):
        query = """
        MATCH (n {id: $node_id})
        RETURN n               
        """
        results = neo4j_service.run_query(query, {"node_id": node_id})
        if not results:
            return results

        node = results[0]["n"]
        node_dict = dict(node)
        # Remove embedding if present
        node_dict.pop("embedding", None)
        node_dict.pop("node_text", None)
        return [{"n": node_dict}]

    @mcp.tool()
    def get_node_edges(node_id: str):
        query = """
        MATCH (n {id: $node_id})-[r]-(m)
        RETURN n.id AS source,
               type(r) AS predicate,
               m.id AS target,
               properties(r) AS properties
        """
        results = neo4j_service.run_query(query, {"node_id": node_id})
        cleaned_results = []

        for record in results:
            props = record["properties"] or {}
            props.pop("embedding", None)
            props.pop("semantic_text", None)

            cleaned_results.append({
                "source": record["source"],
                "predicate": record["predicate"],
                "target": record["target"],
                "properties": props
            })

        return cleaned_results

    @mcp.tool()
    def get_edges_between(source_id: str, target_id: str):
        query = """
        MATCH (a {id: $source_id})-[r]-(b {id: $target_id})
        RETURN type(r) AS predicate,
               properties(r) AS properties
        """
        results = neo4j_service.run_query(
            query,
            {"source_id": source_id, "target_id": target_id},
        )

        cleaned_results = []

        for record in results:
            props = record["properties"] or {}
            props.pop("embedding", None)
            props.pop("semantic_text", None)
            
            cleaned_results.append({
                "predicate": record["predicate"],
                "properties": props
            })

        return cleaned_results
