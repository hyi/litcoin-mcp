def register_semantic_tools(mcp, semantic_service):

    @mcp.tool()
    def get_semantic_similar_edges(query: str, top_k: int = 10, k_per_index: int = 2):
        return semantic_service.search_edges(query, top_k, k_per_index=k_per_index)

    @mcp.tool()
    def get_semantic_similar_nodes(query: str, top_k: int = 10, k_per_index: int = 2):
        return semantic_service.search_nodes(query, top_k, k_per_index=k_per_index)
