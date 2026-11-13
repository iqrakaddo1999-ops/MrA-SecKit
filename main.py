import getpass
import platform
import secrets
import socket
import string
import subprocess

SPECIAL_CHARACTERS = "!@#$%^&*()-_=+[]{};:,.?/~"
LOCAL_PORTS = (21, 22, 23, 80, 443, 8080)


def check_password_strength(password):
    checks = {
        "At least 12 characters": len(password) >= 12,
        "Uppercase letter": any(char.isupper() for char in password),
        "Lowercase letter": any(char.islower() for char in password),
        "Number": any(char.isdigit() for char in password),
        "Symbol": any(char in SPECIAL_CHARACTERS for char in password),
    }
    score = sum(checks.values())
    strength = "Strong" if score == len(checks) else "Moderate" if score >= 3 else "Weak"

    print(f"\nPassword strength: {strength} ({score}/{len(checks)} checks passed)")
    for description, passed in checks.items():
        print(f"- {description}: {'OK' if passed else 'Missing'}")


def generate_password(length=16):
    length = max(12, length)
    alphabet = string.ascii_letters + string.digits + SPECIAL_CHARACTERS
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    print("\nGenerated password (save it somewhere safe):")
    print(password)


def check_local_ports():
    host = "127.0.0.1"
    print(f"\nChecking selected ports on this device ({host})...")
    for port in LOCAL_PORTS:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.5)
                status = sock.connect_ex((host, port))
            print(f"Port {port}: {'open' if status == 0 else 'closed or not responding'}")
        except OSError as error:
            print(f"Port {port}: check failed ({error})")


def list_visible_wifi_networks():
    print("\nWi-Fi networks visible to this device:")
    system = platform.system()
    if system == "Windows":
        command = ["netsh", "wlan", "show", "networks", "mode=bssid"]
    elif system == "Linux":
        command = ["nmcli", "dev", "wifi"]
    else:
        print("Wi-Fi listing is not configured for this operating system.")
        return

    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
        print(result.stdout or "No networks were listed.")
    except FileNotFoundError:
        print("Required Wi-Fi command was not found on this device.")
    except subprocess.CalledProcessError as error:
        print(error.stderr.strip() or "Wi-Fi listing failed.")
    except subprocess.TimeoutExpired:
        print("Wi-Fi listing timed out.")
    except OSError as error:
        print(f"Could not list Wi-Fi networks: {error}")


def main():
    while True:
        print("\n=== MrA-SecKit: Safe Local Toolkit ===")
        print("1. Check password strength")
        print("2. Generate a strong password")
        print("3. Check selected ports on this device")
        print("4. List visible Wi-Fi networks")
        print("5. Exit")
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            check_password_strength(getpass.getpass("Enter password (input is hidden): "))
        elif choice == "2":
            raw_length = input("Password length (default 16): ").strip()
            try:
                length = int(raw_length) if raw_length else 16
                if length < 1:
                    raise ValueError
            except ValueError:
                print("Please enter a positive whole number.")
                continue
            generate_password(length)
        elif choice == "3":
            check_local_ports()
        elif choice == "4":
            list_visible_wifi_networks()
        elif choice == "5":
            print("Bye!")
            break
        else:
            print("Invalid choice. Choose a number from 1 to 5.")


if __name__ == "__main__":
    main()
