import io
import subprocess
import unittest
from unittest.mock import patch

from scripts import bot_github


def result(stdout="", returncode=0):
    return subprocess.CompletedProcess([], returncode, stdout=stdout, stderr="")


class BotGithubTests(unittest.TestCase):
    @patch.dict("os.environ", {"GH_TOKEN": "personal-token", "GITHUB_TOKEN": "other-token"})
    @patch("scripts.bot_github.subprocess.run")
    def test_explicit_bot_credential_replaces_inherited_tokens(self, run):
        run.side_effect = [result("bot-token\n"), result('{"login":"humanifest-bot"}')]
        environment = bot_github.bot_environment()
        self.assertEqual(run.call_args_list[0].args[0][-2:], ["--user", "humanifest-bot"])
        lookup_environment = run.call_args_list[0].kwargs["env"]
        self.assertNotIn("GH_TOKEN", lookup_environment)
        self.assertNotIn("GITHUB_TOKEN", lookup_environment)
        self.assertEqual(environment["GH_TOKEN"], "bot-token")
        self.assertEqual(run.call_args_list[1].kwargs["env"]["GH_TOKEN"], "bot-token")

    @patch("scripts.bot_github.subprocess.run")
    def test_wrong_identity_stops_before_external_command(self, run):
        run.side_effect = [result("wrong-token"), result('{"login":"roryscot"}')]
        with patch("sys.argv", ["bot_github", "issue", "comment", "10155"]), patch("sys.stderr", new_callable=io.StringIO) as output:
            self.assertEqual(bot_github.main(), 1)
        self.assertEqual(run.call_count, 2)
        self.assertNotIn("wrong-token", output.getvalue())
        self.assertIn("Refusing command", output.getvalue())

    @patch("scripts.bot_github.subprocess.run")
    def test_unavailable_or_invalid_identity_fails_closed(self, run):
        for identity in [result(returncode=1), result("not json"), result("[]"), result("{}")]:
            with self.subTest(identity=identity):
                run.side_effect = [result("bot-token"), identity]
                with self.assertRaises(RuntimeError):
                    bot_github.bot_environment()

    @patch("scripts.bot_github.subprocess.run")
    def test_no_credential_stops_before_api_access(self, run):
        run.return_value = result(returncode=1)
        with self.assertRaises(RuntimeError):
            bot_github.bot_environment()
        self.assertEqual(run.call_count, 1)
