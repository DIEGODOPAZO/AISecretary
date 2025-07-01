# AISecretary

AISecretary is a collection of MCP servers designed to automate the tasks of a virtual secretary insede the Outlook suite. Each server handles a specific tool, such as:
- Outlook Mail
- Outlook Calendar
- Outlook Contacts
- Outlook Mailbox Settings
- Categories

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

To configure the necessary Microsoft Graph API settings, follow this setup guide:

- [Outlook](setups/Microsoft.md)

---

### Running the Server

Run the following command to start the server (replace `server.py` with your actual server file):

#### Recommended: Using Claude Desktop

If you have Claude Desktop installed:

```bash
uv run mcp install server.py
```

Other option to install your server in Claude Desktop is to edit the configuration file at:
`C:\Users\YOUR_USER\AppData\Roaming\Claude\claude_desktop_config.json`

```config
{
  "mcpServers": {
    "Server_name": {
      "command": "/Your/path/to/uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "--with",
        "msal",
        "mcp",
        "run",
        "/your/path/to/server.py"
      ]
    },
  }
}
```

If you want all the MCP servers you can just also run the script `src/claude_setup.py`.

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

## Functionalities

These are the available functionalities for each of the MCP servers:

### 📧 Email

#### Email Management
- Advanced email search  
- Retrieve conversations  
- Mark as read/unread  
- Retrieve full emails with attachments  
- Delete emails  
- Move or copy emails  
- Manage flags  

#### Email Creation and Sending
- Create or edit drafts  
- Handle attachments  
- Send drafts  
- Reply to emails  
- Forward emails  

#### Folder Organization
- View folder structure  
- Create or edit folders  
- Delete folders  
- Navigate folder hierarchy  

#### Mail Rules
- View existing rules  
- Create or edit rules  
- Delete rules  

---

### 🏷️ Categories
- View existing categories  
- Create or edit categories  
- Delete categories  
- Assign categories to emails  
- Assign categories to events  
- Use predefined colors  

---

### 📅 Calendar

#### Event Management
- Retrieve events  
- Create events  
- Update events  
- Delete events  
- Retrieve detailed event information  

#### Invitation Handling
- Accept invitations  
- Decline invitations  
- Respond tentatively  
- Cancel events  

#### Attachment Management
- Add attachments  
- Remove attachments  

#### Calendar Management
- List calendars  
- Retrieve specific calendars  
- Create calendars  
- Update calendars  
- Delete calendars  

#### Calendar Group Management
- List groups  
- Create groups  
- Update groups  
- Delete groups  

#### Availability Lookup
- Retrieve free/busy schedule  

---

### 👥 Contacts

#### Contact Folder Management
- Create folders  
- Delete folders  
- Search folders  

#### Contact Management
- Search contacts  
- Retrieve detailed contact information  
- Create contacts  
- Update contacts  
- Delete contacts  

---

### ⚙️ Mailbox Settings

#### General Settings Management
- Retrieve settings  
- Update settings  

#### Supported Settings
- Automatic replies  
- Time zone  
- Working hours  

## Adding New Servers

To add support for new tools, create a new Python file following the structure of the existing servers and register the functions you want to expose as MCP tools.

## More Information

- [Python original sdk](https://github.com/modelcontextprotocol/python-sdk): Explains how to use MCP with different models and tools.
- [OpenWebUI](https://docs.openwebui.com/openapi-servers/mcp/): Detailed guide on integrating MCP servers with OpenWebUI.
- [Anthropic](https://modelcontextprotocol.io/quickstart/user): Detailed guide on integrating MCP servers with Claude Desktop.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.