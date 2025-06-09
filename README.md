# AISecretary

AISecretary is a collection of MCP servers designed to automate the tasks of a virtual secretary. Each server handles a specific tool, such as:
- Outlook Mail

## Features

- **Modular:** Each tool runs as an independent server, so you can start only the ones you need.
- **Easy integration:** Compatible with OpenWebUI and other platforms supporting MCP.
- **Extensible:** Easily add new servers for additional tools or services.
- **Automation:** Handles repetitive tasks like checking emails, managing calendars, and more.

## Prerequisites

- [uv](https://github.com/astral-sh/uv) installed (Python environment and dependency manager).
- Python 3.11 or higher.

## Getting Started

Follow the instructions below to configure and run the server:

### Service Setup

Refer to the appropriate setup guide for your service:

- [Outlook](setups/Microsoft.md)

---

### Running the Server

Run the following command to start the server (replace `server.py` with your actual server file):

#### Recommended: Using Claude Desktop

If you have Claude Desktop installed:

```bash
uv run mcp install server.py
```

#### Alternative: Running with OpenWebUI

If you're using platforms like OpenWebUI:

```bash
uvx mcpo --port 9000 -- uv run mcp run server.py
```

Then open **OpenWebUI**, go to:

```
Settings > Tools > [+]
```

Add the following URL:

```
http://127.0.0.1:9000
```

You can now interact with **AISecretary** through the OpenWebUI interface.


## Adding New Servers

To add support for new tools, create a new Python file following the structure of the existing servers and register the functions you want to expose as MCP tools.

## More Information

- [Python original sdk](https://github.com/modelcontextprotocol/python-sdk): Explains how to use MCP with different models and tools.
- [OpenWebUI](https://docs.openwebui.com/openapi-servers/mcp/): Detailed guide on integrating MCP servers with OpenWebUI.
- [Anthropic](https://modelcontextprotocol.io/quickstart/user): Detailed guide on integrating MCP servers with Claude Desktop.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.