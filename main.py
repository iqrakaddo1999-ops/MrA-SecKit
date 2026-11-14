import json
import os
from datetime import datetime

APP_NAME = "MR-A-SECKIT GOLD"
VERSION = "3.0"
DATA_FILE = "gold_data.json"

TOOLS = [
    {"name": "Password Generator", "category": "Password", "description": "Generate secure random passwords."},
    {"name": "Password Strength Checker", "category": "Password", "description": "Check password strength locally."},
    {"name": "Hash Generator", "category": "Cryptography", "description": "Generate SHA256 hashes."},
    {"name": "Hash Identifier", "category": "Cryptography", "description": "Learn about common hash formats."},
    {"name": "IP Information", "category": "Network", "description": "View basic IP information."},
    {"name": "Port Reference", "category": "Network", "description": "Search common network port information."},
    {"name": "URL Parser", "category": "Web", "description": "Parse URL components."},
    {"name": "Base64 Encoder", "category": "Encoding", "description": "Encode text to Base64."},
    {"name": "Base64 Decoder", "category": "Encoding", "description": "Decode Base64 text."},
    {"name": "Security Tips", "category": "Learning", "description": "Learn safe cybersecurity practices."},
]


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass

    return {"usage": {}, "featured": "", "history": []}


data = load_data()


def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def header():
    print("\n" + "=" * 42)
    print(f"       👑 {APP_NAME}")
    print(f"              VERSION {VERSION}")
    print("=" * 42)


def search_tools():
    query = input("\nSearch tool: ").strip().lower()

    results = [
        t for t in TOOLS
        if query in t["name"].lower()
        or query in t["category"].lower()
    ]

    if not results:
        print("No tools found.")
        return

    for i, tool in enumerate(results, 1):
        print(f"\n{i}. {tool['name']}")
        print(f"   Category: {tool['category']}")
        print(f"   {tool['description']}")

    try:
        choice = int(input("\nOpen tool number (0 to cancel): "))
        if choice == 0:
            return
        if 1 <= choice <= len(results):
            open_tool(results[choice - 1])
    except ValueError:
        print("Invalid choice.")


def open_tool(tool):
    name = tool["name"]
    data["usage"][name] = data["usage"].get(name, 0) + 1

    data["history"].append({
        "tool": name,
        "time": datetime.now().isoformat(timespec="seconds")
    })

    data["history"] = data["history"][-100:]
    save_data()

    print("\n" + "-" * 35)
    print("TOOL:", name)
    print(tool["description"])
    print("-" * 35)

    if name == "Security Tips":
        print("1. Use unique passwords.")
        print("2. Enable two-factor authentication.")
        print("3. Keep software updated.")
        print("4. Never share verification codes.")

    elif name == "Base64 Encoder":
        import base64
        value = input("Enter text: ")
        print(base64.b64encode(value.encode()).decode())

    elif name == "Base64 Decoder":
        import base64
        value = input("Enter Base64: ")
        try:
            print(base64.b64decode(value, validate=True).decode())
        except Exception:
            print("Invalid Base64 input.")

    elif name == "Hash Generator":
        import hashlib
        value = input("Enter text: ")
        print("SHA256:", hashlib.sha256(value.encode()).hexdigest())

    elif name == "Password Generator":
        import secrets
        import string
        try:
            length = int(input("Password length (8-128): "))
            if not 8 <= length <= 128:
                print("Choose a length between 8 and 128.")
                return
            chars = string.ascii_letters + string.digits + "!@#$%^&*"
            password = ''.join(secrets.choice(chars) for _ in range(length))
            print("Generated password:", password)
        except ValueError:
            print("Invalid length.")

    elif name == "Password Strength Checker":
        password = input("Enter a password to check: ")
        score = sum([
            len(password) >= 12,
            any(c.islower() for c in password),
            any(c.isupper() for c in password),
            any(c.isdigit() for c in password),
            any(not c.isalnum() for c in password)
        ])
        print("Strength:", ["Very weak", "Weak", "Fair", "Good", "Strong", "Very strong"][score])

    elif name == "URL Parser":
        from urllib.parse import urlparse
        url = input("Enter URL: ")
        parsed = urlparse(url)
        print("Scheme:", parsed.scheme)
        print("Domain:", parsed.hostname)
        print("Path:", parsed.path)

    else:
        print("This tool is in the library.")
        print("Its full functionality will be added in a future update.")


def popular_tools():
    print("\n🏆 MOST POPULAR TOOLS")

    ranking = sorted(
        TOOLS,
        key=lambda t: data["usage"].get(t["name"], 0),
        reverse=True
    )

    for i, tool in enumerate(ranking[:10], 1):
        count = data["usage"].get(tool["name"], 0)
        print(f"{i}. {tool['name']} — {count} uses")


def featured_tool():
    name = data.get("featured", "")

    if not name:
        print("\nNo featured tool selected yet.")
        return

    tool = next((t for t in TOOLS if t["name"] == name), None)

    if tool:
        print("\n⭐ FEATURED TOOL:", name)
        open_tool(tool)


def set_featured():
    print("\nChoose a featured tool:")
    for i, tool in enumerate(TOOLS, 1):
        print(f"{i}. {tool['name']}")

    try:
        choice = int(input("Number: "))
        if 1 <= choice <= len(TOOLS):
            data["featured"] = TOOLS[choice - 1]["name"]
            save_data()
            print("Featured tool updated!")
        else:
            print("Invalid number.")
    except ValueError:
        print("Invalid choice.")


def gold_ai():
    print("\n🤖 THE GOLD AI")
    print("Offline starter assistant")
    print("Type 'exit' to return.")

    while True:
        question = input("\nYou: ").strip().lower()

        if question == "exit":
            break

        if any(word in question for word in ["hello", "hi", "hey"]):
            answer = "Hello! Welcome to THE GOLD AI."

        elif "password" in question:
            answer = "Use long, unique passwords and enable 2FA."

        elif "security" in question:
            answer = "Keep your devices updated and use trusted software."

        elif "hacking" in question:
            answer = "Learn ethical hacking in authorized lab environments."

        elif "termux" in question:
            answer = "Termux lets you run Python and Linux command-line tools on Android."

        else:
            answer = "I am an offline starter AI. My knowledge is currently limited."

        print("THE GOLD AI:", answer)


def main():
    while True:
        header()

        print("1. Search Tools")
        print("2. All Tools")
        print("3. Most Popular Tools")
        print("4. Featured Tool")
        print("5. Set Featured Tool")
        print("6. THE GOLD AI")
        print("7. Exit")

        choice = input("\nSelect option: ").strip()

        if choice == "1":
            search_tools()

        elif choice == "2":
            for tool in TOOLS:
                print(f"\n{tool['name']} [{tool['category']}]")
                print(tool["description"])

        elif choice == "3":
            popular_tools()

        elif choice == "4":
            featured_tool()

        elif choice == "5":
            set_featured()

        elif choice == "6":
            gold_ai()

        elif choice == "7":
            print("Thanks for using MR-A-SECKIT GOLD!")
            break

        else:
            print("Invalid option.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
