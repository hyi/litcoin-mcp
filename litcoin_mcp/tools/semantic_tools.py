def register_semantic_tools(mcp, semantic_service):

    @mcp.tool()
    def get_semantic_similar_edges(query: str, top_k: int = 10):
        return semantic_service.search_edges(query, top_k)

    @mcp.tool()
    def get_semantic_similar_nodes(query: str, top_k: int = 10):
        return semantic_service.search_nodes(query, top_k)
