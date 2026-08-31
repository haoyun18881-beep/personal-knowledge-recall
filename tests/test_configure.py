from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "configure.py"


class ConfigureScriptTests(unittest.TestCase):
    def run_script(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )

    def test_unicode_and_space_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            vault = base / "中文 知识库"
            vault.mkdir()
            output = base / "配置 文件.json"
            result = self.run_script(
                "--vault",
                str(vault),
                "--entry",
                "入口 文件.md",
                "--restricted",
                "个人 档案",
                "--output",
                str(output),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(payload["vault_root"], str(vault.resolve()))
            self.assertEqual(payload["entry_files"], ["入口 文件.md"])
            self.assertEqual(payload["restricted_paths"], ["个人 档案"])

    def test_existing_config_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            vault = base / "vault"
            vault.mkdir()
            output = base / "local-config.json"
            output.write_text("original", encoding="utf-8")
            result = self.run_script("--vault", str(vault), "--output", str(output))
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(output.read_text(encoding="utf-8"), "original")

    def test_missing_vault_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            result = self.run_script(
                "--vault",
                str(base / "missing"),
                "--output",
                str(base / "config.json"),
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("does not exist", result.stderr)

    def test_traversal_and_absolute_children_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            vault = base / "vault"
            vault.mkdir()
            unsafe_values = [
                "../outside.md",
                "/etc/passwd",
                r"C:\\private\\note.md",
                r"\\server\\share",
                "NUL.txt",
                "folder./note.md",
                "folder /note.md",
                "folder ",
                " folder/note.md",
                "wild*/note.md",
            ]
            for index, unsafe in enumerate(unsafe_values):
                with self.subTest(unsafe=unsafe):
                    result = self.run_script(
                        "--vault",
                        str(vault),
                        "--entry",
                        unsafe,
                        "--output",
                        str(base / f"config-{index}.json"),
                    )
                    self.assertNotEqual(result.returncode, 0)

    def test_force_replaces_existing_config(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            vault = base / "vault"
            vault.mkdir()
            output = base / "local-config.json"
            output.write_text("original", encoding="utf-8")
            result = self.run_script(
                "--vault",
                str(vault),
                "--output",
                str(output),
                "--qa-fallback",
                "off",
                "--force",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(payload["qa_fallback"], "off")

    def test_json_result_is_machine_readable(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            vault = base / "vault"
            vault.mkdir()
            output = base / "local-config.json"
            result = self.run_script(
                "--vault",
                str(vault),
                "--output",
                str(output),
                "--json",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["ok"])
            self.assertTrue(Path(payload["config"]).samefile(output))

    def test_existing_write_lock_prevents_clobber(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            vault = base / "vault"
            vault.mkdir()
            output = base / "local-config.json"
            lock = base / ".local-config.json.lock"
            lock.write_text("held", encoding="utf-8")
            result = self.run_script("--vault", str(vault), "--output", str(output))
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output.exists())
            self.assertEqual(lock.read_text(encoding="utf-8"), "held")

    def test_output_symlink_is_rejected_even_with_force(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            vault = base / "vault"
            vault.mkdir()
            unrelated = base / "unrelated.txt"
            unrelated.write_text("keep me", encoding="utf-8")
            output = base / "local-config.json"
            try:
                output.symlink_to(unrelated)
            except OSError:
                self.skipTest("creating file symlinks is not permitted on this host")
            result = self.run_script(
                "--vault",
                str(vault),
                "--output",
                str(output),
                "--force",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(unrelated.read_text(encoding="utf-8"), "keep me")

    @unittest.skipUnless(hasattr(Path, "symlink_to"), "symlink support unavailable")
    def test_symlink_child_is_rejected_when_supported(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            vault = base / "vault"
            target = base / "outside"
            vault.mkdir()
            target.mkdir()
            link = vault / "linked"
            try:
                link.symlink_to(target, target_is_directory=True)
            except OSError:
                self.skipTest("creating symlinks is not permitted on this host")
            result = self.run_script(
                "--vault",
                str(vault),
                "--restricted",
                "linked",
                "--output",
                str(base / "config.json"),
            )
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
