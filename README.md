# MrA-SecKit

An educational Python toolkit for basic password strength checks and secure password generation. Network scanning features are not included.

## Features
- Password strength checker (input is hidden while entered)
- Password generator using Python's `secrets` module

## Run
Python 3 is required. No third-party packages are needed.

```bash
python main.py
```

## Privacy and limitations
- The password checker evaluates a password locally and does not send it over the network. Avoid reusing important passwords for testing; use a sample instead.
- Strength checks are a simple guide, not a guarantee of security.
- Generated passwords are displayed in the terminal. Store them securely, such as in a trusted password manager.
- This project does not scan networks, hosts, or ports.
