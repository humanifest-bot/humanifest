"""Run gh with an explicitly selected and verified Humanifest bot credential.

Usage: python3 -m scripts.bot_github api user --jq .login
This verifies identity only; callers must still check authorization and scope.
Credentials stay in memory and the child environment, never in files or argv.
"""

import json
import os
import subprocess
import sys


BOT_LOGIN = "humanifest-bot"


def bot_environment() -> dict[str, str]:
    environment = os.environ.copy()
    # Inherited tokens must not override the account-specific Keychain lookup.
    environment.pop("GH_TOKEN", None)
    environment.pop("GITHUB_TOKEN", None)
    environment["GH_HOST"] = "github.com"
    credential = subprocess.run(
        ["gh", "auth", "token", "--hostname", "github.com", "--user", BOT_LOGIN],
        env=environment.copy(), capture_output=True, text=True,
    )
    if credential.returncode or not credential.stdout.strip():
        raise RuntimeError("Could not retrieve the Humanifest bot credential.")
    environment["GH_TOKEN"] = credential.stdout.strip()
    identity = subprocess.run(
        ["gh", "api", "--hostname", "github.com", "user"],
        env=environment, capture_output=True, text=True,
    )
    if identity.returncode:
        raise RuntimeError("Could not verify the Humanifest bot identity.")
    try:
        login = json.loads(identity.stdout)["login"]
    except (ValueError, KeyError, TypeError):
        raise RuntimeError("GitHub returned an invalid identity response.") from None
    if login != BOT_LOGIN:
        raise RuntimeError("Refusing command: credential does not identify humanifest-bot.")
    return environment


def main() -> int:
    if not sys.argv[1:]:
        print("Usage: python3 -m scripts.bot_github <gh arguments>", file=sys.stderr)
        return 2
    try:
        environment = bot_environment()
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        return 1
    return subprocess.run(["gh", *sys.argv[1:]], env=environment).returncode


if __name__ == "__main__":
    raise SystemExit(main())
