import getpass
import secrets
import string

SPECIAL_CHARACTERS = "!@#$%^&*()-_=+[]{};:,.?/"


def check_password_strength():
    password = getpass.getpass("Enter a password to check (input is hidden): ")
    checks = {
        "at least 12 characters": len(password) >= 12,
        "an uppercase letter": any(char.isupper() for char in password),
        "a lowercase letter": any(char.islower() for char in password),
        "a number": any(char.isdigit() for char in password),
        "a special character": any(char in SPECIAL_CHARACTERS for char in password),
    }

    score = sum(checks.values())
    print("\n--- Result ---")
    if score == len(checks):
        print("Strong by these basic checks. This is only a rough estimate.")
    elif score >= 3:
        print("Some criteria are met; consider improving the password.")
    else:
        print("This password may be easy to guess. Consider using a longer passphrase.")

    for description, passed in checks.items():
        if not passed:
            print(f"- Consider using {description}.")


def generate_password():
    try:
        length = int(input("Password length (12 or more; default 16): ").strip() or "16")
    except ValueError:
        print("Invalid length; using 16 characters.")
        length = 16

    if length < 12:
        print("Using the minimum length of 12 characters.")
        length = 12

    groups = [
        string.ascii_uppercase,
        string.ascii_lowercase,
        string.digits,
        SPECIAL_CHARACTERS,
    ]
    alphabet = "".join(groups)
    password_chars = [secrets.choice(group) for group in groups]
    password_chars.extend(secrets.choice(alphabet) for _ in range(length - len(password_chars)))
    secrets.SystemRandom().shuffle(password_chars)

    print("\nGenerated password (store it in a password manager):")
    print("".join(password_chars))


def main():
    while True:
        print("\n==============================")
        print("       MrA-SecKit")
        print("==============================")
        print("1. Check Password Strength")
        print("2. Generate Strong Password")
        print("3. Exit")

        choice = input("Select an option (1-3): ").strip()
        if choice == "1":
            check_password_strength()
        elif choice == "2":
            generate_password()
        elif choice == "3":
            print("Stay safe!")
            return
        else:
            print("Invalid choice. Select 1, 2, or 3.")


if __name__ == "__main__":
    main()
