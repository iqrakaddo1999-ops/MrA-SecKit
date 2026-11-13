import platform
import socket
import subprocess

COMMON_LOCAL_PORTS = [21, 22, 23, 80, 443, 8080]


def banner():
    print("=" * 50)
    print("       MrA-SecKit - Local Diagnostics")
    print("       Checks this device only")
    print("=" * 50)


def check_local_ports():
    """Check selected TCP ports on this device only (127.0.0.1)."""
    host = "127.0.0.1"
    print(f"\n--- Checking selected ports on this device ({host}) ---")
    for port in COMMON_LOCAL_PORTS:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.5)
                if sock.connect_ex((host, port)) == 0:
                    print(f"[+] Port {port}: open on this device")
                else:
                    print(f"[-] Port {port}: closed or not responding")
        except OSError as error:
            print(f"[-] Could not check port {port}: {error}")


def show_wifi_networks():
    """Display Wi-Fi networks visible to this device using OS utilities."""
    print("\n--- Wi-Fi networks visible to this device ---")
    try:
        system = platform.system()
        if system == "Windows":
            command = ["netsh", "wlan", "show", "networks", "mode=bssid"]
        elif system == "Linux":
            command = ["nmcli", "dev", "wifi"]
        else:
            print("[-] Wi-Fi listing is not configured for this operating system.")
            return

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
        print("[-] Required Wi-Fi command was not found on this device.")
    except subprocess.CalledProcessError as error:
        print(f"[-] Wi-Fi listing failed: {error.stderr.strip() or error}")
    except subprocess.TimeoutExpired:
        print("[-] Wi-Fi listing timed out.")
    except OSError as error:
        print(f"[-] Could not list Wi-Fi networks: {error}")


def main():
    banner()
    while True:
        print("\nChoose an option:")
        print("1. Check selected ports on this device")
        print("2. List Wi-Fi networks visible to this device")
        print("3. Exit")

        choice = input("\nSelect option (1-3): ").strip()
        if choice == "1":
            check_local_ports()
        elif choice == "2":
            show_wifi_networks()
        elif choice == "3":
            print("Exiting tool. Stay safe!")
            break
        else:
            print("Invalid choice; select 1, 2, or 3.")


if __name__ == "__main__":
    main()
