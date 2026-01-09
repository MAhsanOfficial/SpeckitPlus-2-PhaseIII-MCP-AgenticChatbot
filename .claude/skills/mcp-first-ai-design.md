# MCP-First AI Design

## Rules
- AI agent NEVER touches database directly
- All actions go through MCP tools
- Tools are deterministic and stateless

## Analysis
This skill enforces a clean separation between AI reasoning and database operations. By routing all data interactions through MCP (Model Context Protocol) tools, the system maintains predictability and testability. Tools are designed to be stateless and deterministic, meaning the same input always produces the same output, making the AI's behavior predictable and auditable.
