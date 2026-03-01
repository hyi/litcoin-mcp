#!/usr/bin/env python3

from fastmcp import FastMCP
from litcoin_mcp.config import get_settings
from litcoin_mcp.services.neo4j_service import Neo4jService
from litcoin_mcp.services.embedding_service import EmbeddingService
from litcoin_mcp.services.semantic_search_service import SemanticSearchService
from litcoin_mcp.tools.graph_tools import register_graph_tools
from litcoin_mcp.tools.semantic_tools import register_semantic_tools


def create_server():
    settings = get_settings()

    mcp = FastMCP("litcoin", version="0.1.0")

    neo4j_service = Neo4jService(
        settings.neo4j_uri,
        settings.neo4j_user,
        settings.neo4j_password,
    )

    embedding_service = EmbeddingService(
        settings.openai_api_key,
        settings.embedding_model,
    )

    semantic_service = SemanticSearchService(
        neo4j_service,
        embedding_service,
        settings.edge_vector_index,
        settings.node_vector_index,
    )

    register_graph_tools(mcp, neo4j_service)
    register_semantic_tools(mcp, semantic_service)

    return mcp


def main():
    server = create_server()
    server.run()


if __name__ == "__main__":
    main()
