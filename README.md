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

Run the following command for each server you want to start (replace `server.py` with the actual server file):

```
uvx mcpo --port 9000 -- python server.py
```

Then, open OpenWebUI on your machine and go to **Settings > Tools > +**. Enter the following URL:

```
http://127.0.0.1:9000
```

Now you can interact with AISecretary from the OpenWebUI interface.

## Adding New Servers

To add support for new tools, create a new Python file following the structure of the existing servers and register the functions you want to expose as MCP tools.

## More Information

- [Python original sdk](https://github.com/modelcontextprotocol/python-sdk): Explains how to use MCP with different models and tools.
- [OpenWebUI](https://docs.openwebui.com/openapi-servers/mcp/): Detailed guide on integrating MCP servers with OpenWebUI.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.