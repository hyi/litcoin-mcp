# LitCoin MCP Server

MCP server for the LitCoin Knowledge Graph (KG) - query LitCoin knowledge graph for nodes, edges, 
relationships as well as semantic similarity search over nodes and relationships. It supports 
semantic + structural LitCoin knowledge graph access for AI agents via MCP.  

## This MCP server exposes the following tools:

- get_node(node_id: CURIE str)
  - Get information about a specific node by CURIE.
- get_node_edges(node_id: CURIE str)
  - Get all edges connected to a node.
- get_edges_between(source_id: CURIE str, target_id: CURIE str)
  - Find all edges connecting two nodes by CURIEs
- get_semantic_similar_nodes(query: str, top_k: int = 10, k_per_index: int = 2)
  - Find top_k semantically similar nodes to an input text query
- get_semantic_similar_edges(query: str, top_k: int = 10, k_per_index: int = 2)
  - Find top_k semantically similar relationships to an input text query

Note that for semantic search tools to work, this MCP server assumes Neo4j embedding vector 
indexes already exist.  

### Response Format

- All responses are JSON serializable.
- Embedding vectors stored in Neo4j are never returned to the client.
- Semantic search results are sorted by similarity score (descending).

## Recommended Usage: Use with uvx

No installation needed! Use uvx to run the server in isolated environments.

## Configuration
### Environment Variables
The following environmental variables must be configured for this LitCoin MCP Server:

- OPENAI_API_KEY - OPENAI API Key for semantic search related tools 
such as get_semantic_similar_nodes and get_semantic_similar_edges. 
the embedding vectors for nodes and edges in the LitCoin KG were created 
using the `text-embedding-3-small` model from OpenAI. It's recommended to use 
the same model to generate embeddings for input text queries to ensure 
dimensional compatibility for semantic search related tools.
- NEO4J_USERNAME - LitCoin Neo4j server authentication username.
- NEO4J_PASSWORD - LitCoin Neo4j server authentication password.
- NEO4J_URI - LitCoin Knowledge Graph endpoint (default: `bolt://litcoin-graph.apps.renci.org:7687`)

### MCP CLient (e.g., Goose, Claude Desktop) Configuration
#### Using uvx
The easiest way to use this MCP server is with uvx, which runs it in isolated environments without installation:
```
{
  "mcpServers": {
    "litcoin": {
      "command": "uvx",
      "args": ["litcoin-mcp"]
    }
  }
}
```
#### For Local Development
When running from source, use the full uv command:
```
{
  "mcpServers": {
    "robokop": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/absolute/path/to/litcoin-mcp",
        "python",
        "run_server.py"
      ]
    }
  }
}
```
**Note**: Replace /absolute/path/to/litcoin-mcp with your actual path.