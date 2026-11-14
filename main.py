import getpass
import json
import os
import hashlib
import secrets
import string
import base64
import urllib.error
import urllib.request
from urllib.parse import urlparse

APP = "MrA-SecKit GOLD"
VERSION = "3.1"
DATA = "gold_stats.json"
GEMINI_MODEL = "gemini-3.6-flash"
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/"
    f"v1beta/models/{GEMINI_MODEL}:generateContent"
)
GOLD_AI_SYSTEM_PROMPT = """
You are THE GOLD AI, assistant of MrA-SecKit.
Help with Python, Termux, coding and cybersecurity.
Explain errors step by step.
Only support authorized and defensive security work.
Never claim a tool works unless it has been tested.
Use Hindi or English according to the user's language.
""".strip()

TOOLS = [
    ("Password Generator", "Password", "Generate secure passwords"),
    ("Password Checker", "Password", "Check password strength"),
    ("SHA256 Generator", "Crypto", "Generate SHA256 hashes"),
    ("Base64 Encoder", "Encoding", "Encode text"),
    ("Base64 Decoder", "Encoding", "Decode text"),
    ("URL Parser", "Web", "Parse URL information"),
    ("IP Validator", "Network", "Validate IP addresses"),
    ("Port Reference", "Network", "Learn common port numbers"),
    ("Security Tips", "Learning", "Cybersecurity advice"),
    ("Hash Learning", "Crypto", "Learn about hashes"),
    ("THE GOLD AI", "AI", "Gemini-powered assistant"),
]


def load_stats():
    if os.path.exists(DATA):
        try:
            with open(DATA, "r") as f:
                loaded = json.load(f)
            if isinstance(loaded, dict) and isinstance(loaded.get("usage"), dict):
                return loaded
        except (OSError, ValueError):
            pass
    return {"usage": {}}


stats = load_stats()


def save():
    with open(DATA, "w") as f:
        json.dump(stats, f, indent=2)


def header():
    print("\n" + "=" * 42)
    print("       👑 " + APP)
    print("             VERSION " + VERSION)
    print("=" * 42)


def password_generator():
    try:
        n = int(input("Password length (8-128): "))
        if not 8 <= n <= 128:
            print("Choose 8 to 128.")
            return
        chars = string.ascii_letters + string.digits + "!@#$%&*"
        print("Password:", "".join(secrets.choice(chars) for _ in range(n)))
    except ValueError:
        print("Invalid length.")


def password_checker():
    p = input("Password to check: ")
    score = sum([
        len(p) >= 12,
        any(c.islower() for c in p),
        any(c.isupper() for c in p),
        any(c.isdigit() for c in p),
        any(not c.isalnum() for c in p)
    ])
    levels = ["Very weak", "Weak", "Fair", "Good", "Strong", "Very strong"]
    print("Strength:", levels[score])


def sha256():
    text = input("Text: ")
    print(hashlib.sha256(text.encode()).hexdigest())


def encode():
    text = input("Text: ")
    print(base64.b64encode(text.encode()).decode())


def decode():
    text = input("Base64: ")
    try:
        print(base64.b64decode(text, validate=True).decode())
    except Exception:
        print("Invalid Base64.")


def url_parser():
    url = input("URL: ")
    result = urlparse(url)
    print("Scheme:", result.scheme)
    print("Domain:", result.hostname)
    print("Path:", result.path)


def ip_validator():
    import ipaddress
    ip = input("IP address: ")
    try:
        print("Valid IP:", ipaddress.ip_address(ip))
    except ValueError:
        print("Invalid IP address.")


def port_reference():
    ports = {
        21: "FTP",
        22: "SSH",
        53: "DNS",
        80: "HTTP",
        443: "HTTPS",
        3306: "MySQL",
        5432: "PostgreSQL"
    }
    try:
        p = int(input("Port number: "))
        print(ports.get(p, "No entry in built-in reference"))
    except ValueError:
        print("Enter a valid number.")


def security_tips():
    tips = [
        "Use unique passwords.",
        "Enable two-factor authentication.",
        "Keep your phone updated.",
        "Never share OTP codes.",
        "Use HTTPS websites.",
        "Back up important data."
    ]
    for tip in tips:
        print("[+] " + tip)


def hash_learning():
    print("SHA256: 256-bit cryptographic hash")
    print("SHA512: 512-bit cryptographic hash")
    print("MD5: Legacy hash, not recommended for security.")


def gold_ai():
    print("\n👑 THE GOLD AI — Gemini-powered assistant")
    print("Type 'exit' to return. Your API key is requested privately and is not saved.\n")

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        try:
            api_key = getpass.getpass("Enter your Gemini API key: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAPI key input cancelled.")
            return

    if not api_key:
        print("API key is required. You can set GEMINI_API_KEY and try again.")
        return

    history = []
    while True:
        try:
            question = input("\nYOU > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nReturning to the main menu.")
            return

        if question.lower() in ("exit", "quit"):
            print("THE GOLD AI > Goodbye!")
            return
        if not question:
            continue

        history.append({"role": "user", "parts": [{"text": question}]})
        payload = {
            "system_instruction": {"parts": [{"text": GOLD_AI_SYSTEM_PROMPT}]},
            "contents": history,
            "generationConfig": {"temperature": 0.7, "maxOutputTokens": 2048},
        }
        request = urllib.request.Request(
            GEMINI_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "x-goog-api-key": api_key,
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                result = json.loads(response.read().decode("utf-8"))

            answer = result["candidates"][0]["content"]["parts"][0]["text"]
            print("\n👑 THE GOLD AI:")
            print(answer)
            history.append({"role": "model", "parts": [{"text": answer}]})
            if len(history) > 20:
                history = history[-20:]

        except urllib.error.HTTPError as error:
            details = error.read().decode("utf-8", errors="replace")
            print(f"\nAI request failed (HTTP {error.code}): {details[:1000]}")
            history.pop()
        except (urllib.error.URLError, TimeoutError) as error:
            print("Connection error:", error)
            history.pop()
        except (KeyError, IndexError, TypeError, ValueError) as error:
            print("Could not read the AI response:", error)
            history.pop()


FUNCTIONS = {
    "Password Generator": password_generator,
    "Password Checker": password_checker,
    "SHA256 Generator": sha256,
    "Base64 Encoder": encode,
    "Base64 Decoder": decode,
    "URL Parser": url_parser,
    "IP Validator": ip_validator,
    "Port Reference": port_reference,
    "Security Tips": security_tips,
    "Hash Learning": hash_learning,
    "THE GOLD AI": gold_ai,
}


def run_tool(tool):
    name = tool[0]
    stats["usage"][name] = stats["usage"].get(name, 0) + 1
    save()
    print("\n--- " + name + " ---")
    FUNCTIONS[name]()


def search():
    q = input("Search: ").lower().strip()
    found = [t for t in TOOLS if q in t[0].lower() or q in t[1].lower()]

    if not found:
        print("No matching tool found.")
        return

    for i, t in enumerate(found, 1):
        print(f"{i}. {t[0]} - {t[2]}")

    try:
        n = int(input("Select number (0 to cancel): "))
        if 1 <= n <= len(found):
            run_tool(found[n - 1])
    except ValueError:
        print("Invalid selection.")


def popular():
    ranking = sorted(
        TOOLS,
        key=lambda t: stats["usage"].get(t[0], 0),
        reverse=True
    )
    print("\n🏆 MOST POPULAR TOOLS")
    for i, t in enumerate(ranking[:10], 1):
        count = stats["usage"].get(t[0], 0)
        print(f"{i}. {t[0]} - {count} uses")


def main():
    while True:
        header()
        print("1. All Tools")
        print("2. Search Tools")
        print("3. Most Popular")
        print("4. THE GOLD AI")
        print("5. Security Tips")
        print("6. Exit")

        choice = input("\nChoose: ").strip()

        if choice == "1":
            for i, t in enumerate(TOOLS, 1):
                print(f"{i}. {t[0]} [{t[1]}]")
            try:
                n = int(input("Tool number (0 to cancel): "))
                if 1 <= n <= len(TOOLS):
                    run_tool(TOOLS[n - 1])
            except ValueError:
                print("Invalid number.")

        elif choice == "2":
            search()
        elif choice == "3":
            popular()
        elif choice == "4":
            gold_ai()
        elif choice == "5":
            security_tips()
        elif choice == "6":
            print("Goodbye from MrA-SecKit GOLD!")
            break
        else:
            print("Invalid option.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
