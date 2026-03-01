def register_graph_tools(mcp, neo4j_service):

    @mcp.tool()
    def get_node(node_id: str):
        query = """
        MATCH (n {id: $node_id})
        RETURN n
        """
        return neo4j_service.run_query(query, {"node_id": node_id})

    @mcp.tool()
    def get_edges(node_id: str):
        query = """
        MATCH (n {id: $node_id})-[r]-(m)
        RETURN n.id AS source,
               type(r) AS predicate,
               m.id AS target,
               properties(r) AS properties
        """
        return neo4j_service.run_query(query, {"node_id": node_id})

    @mcp.tool()
    def get_edges_between(source_id: str, target_id: str):
        query = """
        MATCH (a {id: $source_id})-[r]-(b {id: $target_id})
        RETURN type(r) AS predicate,
               properties(r) AS properties
        """
        return neo4j_service.run_query(
            query,
            {"source_id": source_id, "target_id": target_id},
        )
