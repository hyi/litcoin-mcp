#!/usr/bin/env python3

from fastmcp import FastMCP
from litcoin_mcp.config import get_settings, NODE_LABELS, RELATIONSHIP_TYPES
from litcoin_mcp.services.neo4j_service import Neo4jService
from litcoin_mcp.services.embedding_service import EmbeddingService
from litcoin_mcp.services.semantic_search_service import SemanticSearchService
from litcoin_mcp.tools.graph_tools import register_graph_tools
from litcoin_mcp.tools.semantic_tools import register_semantic_tools

# Create the FastMCP server
mcp = FastMCP("litcoin", version="0.1.0")

def create_server():
    settings = get_settings()

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
        node_types=NODE_LABELS,
        edge_types=RELATIONSHIP_TYPES
    )

    register_graph_tools(mcp, neo4j_service)
    register_semantic_tools(mcp, semantic_service)

create_server()

def main():
    mcp.run()

if __name__ == "__main__":
    main()
