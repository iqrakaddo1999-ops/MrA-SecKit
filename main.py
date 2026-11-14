import time


class MrASecKitShell:
    def __init__(self):
        self.modules = {}
        self.load_tool_database()

    def load_tool_database(self):
        self.tool_database = {
            "nmap": "Network mapper and port scanner utility",
            "metasploit": "Penetration testing framework simulation",
            "wireshark": "Network packet analyzer tool",
            "hydra": "Login cracker supporting various protocols",
            "john": "Password security auditing and cracking tool",
            "aircrack-ng": "802.11 WEP/WPA-PSK cracking utility",
            "sqlmap": "Automatic SQL injection and database takeover tool",
            "hashcat": "Advanced password recovery utility",
            "setoolkit": "Social-engineering toolkit framework",
            "nikto": "Web server vulnerability scanner",
        }

    def register_module(self, name, func, description):
        self.modules[name] = {"func": func, "desc": description}

    def banner(self):
        print("=" * 55)
        print("      MrA-SecKit v2.2 - Advanced Tool Search      ")
        print(f"      Database Index: {len(self.tool_database)} Tools Registered")
        print("=" * 55)
        print("Type 'help' for commands, 'search <tool>' to find tools, or 'learn' to study.\n")

    def cmd_help(self):
        print("\n--- Built-in Core Commands ---")
        for name, info in self.modules.items():
            print(f"  {name:<15} - {info['desc']}")
        print("  search <name>   - Search from the tool index")
        print("  exit            - Exit MrA-SecKit")
        print()

    def cmd_search(self, query):
        if not query:
            print("[-] Please provide a tool name to search. Example: search nmap")
            return

        print(f"\n[🔍] Searching for '{query}' in database...")
        time.sleep(0.5)

        found = False
        for tool, desc in self.tool_database.items():
            if query.lower() in tool.lower():
                print(f"  [+] Found -> {tool} : {desc}")
                found = True

        if not found:
            print(f"[-] '{query}' not found in the database.")
        print()

    def cmd_learn(self):
        print("\n" + "=" * 40)
        print("      MrA-SecKit : Ethical Hacking Guide      ")
        print("=" * 40)
        print("1. What are Network Ports?")
        print("2. What is Password Brute-force?")
        print("3. Wi-Fi Security Basics")
        print("4. Back to Main Menu")

        choice = input("\nSelect a topic to study (1-4): ").strip()
        if choice == "1":
            print("\n[📚 Lesson: Network Ports]")
            print("- Computers have ports from 0 to 65535 (e.g., Port 80 for HTTP).\n")
        elif choice == "2":
            print("\n[📚 Lesson: Password Brute-force]")
            print("- This means trying password guesses repeatedly. Only assess systems you own or have explicit permission to test.\n")
        elif choice == "3":
            print("\n[📚 Lesson: Wi-Fi Security Basics]")
            print("- Use WPA2-AES or WPA3, a unique strong password, and updated router firmware.\n")
        else:
            print("Returning to main menu...\n")

    def run(self):
        self.banner()
        while True:
            try:
                user_input = input("MrA-SecKit> ").strip()
                if not user_input:
                    continue

                parts = user_input.split(" ", 1)
                command = parts[0].lower()
                arg = parts[1] if len(parts) > 1 else ""

                if command == "exit":
                    print("Exiting MrA-SecKit... Goodbye!")
                    break
                elif command == "help":
                    self.cmd_help()
                elif command == "search":
                    self.cmd_search(arg)
                elif command == "learn":
                    self.cmd_learn()
                elif command in self.modules:
                    self.modules[command]["func"]()
                else:
                    print(f"[-] Unknown command: '{command}'. Type 'help' for options.")

            except KeyboardInterrupt:
                print("\nUse 'exit' to properly close the tool.")
            except Exception as error:
                print(f"[-] Error: {error}")


if __name__ == "__main__":
    kit = MrASecKitShell()
    kit.register_module("learn", kit.cmd_learn, "Built-in security tutorials")
    kit.run()
