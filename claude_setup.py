if __name__ == "__main__":
    import subprocess

    tool_paths = [
        r".\src\outlook_calendar_mcp.py",
        r".\src\outlook_mailbox_settings_mcp.py",
        r".\src\outlook_categories_mcp.py",
        r".\src\outlook_mail_mcp.py",
        r".\src\outlook_contacts_mcp.py",
        r".\src\outlook_to_do_mcp.py"
    ]

    for path in tool_paths:
        print(f"Instaling: {path}")
        result = subprocess.run(
            ["uv", "run", "mcp", "install", path],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print("Result:", result.stderr)