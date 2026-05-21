import gzip
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT_DIR / "scripts" / "build_en_lexicon.py"


def load_generator():
    spec = importlib.util.spec_from_file_location("build_en_lexicon", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class BuildEnLexiconTests(unittest.TestCase):
    def testEnglishLexiconFilterKeepsOnlyGameSafeWords(self):
        """Проверяет EN-фильтр: остаются только lowercase a-z lemma длиной от 3."""
        generator = load_generator()

        words = generator.build_words(
            [
                "apple",
                "Apple",
                "cat",
                "cat",
                "co-op",
                "can't",
                "ab",
                "milk2",
                "tea",
                "zoo",
                "DOG",
            ]
        )

        self.assertEqual(words, ["apple", "cat", "tea", "zoo"])

    def testBuildLexiconWordsCreatesReleaseManifestAndCompressedArtifact(self):
        """Проверяет создание txt, txt.gz и manifest из локального plain fixture."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            source_path = temp_path / "words.txt"
            output_dir = temp_path / "dist"
            source_path.write_text(
                "\n".join(
                    [
                        "banana",
                        "Apple",
                        "cat",
                        "cat",
                        "co-op",
                        "tea",
                        "ab",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), str(source_path), str(output_dir), "7"],
                check=True,
                text=True,
                capture_output=True,
            )

            self.assertIn("words: 3", result.stdout)

            text_path = output_dir / "en_words.txt"
            archive_path = output_dir / "en_words.txt.gz"
            manifest_path = output_dir / "lexicons_manifest.json"

            self.assertEqual(text_path.read_text(encoding="utf-8"), "banana\ncat\ntea\n")

            with gzip.open(archive_path, "rt", encoding="utf-8") as file:
                self.assertEqual(file.read(), "banana\ncat\ntea\n")

            archive_hash = hashlib.sha256(archive_path.read_bytes()).hexdigest()
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

            self.assertEqual(len(manifest), 1)
            self.assertEqual(manifest[0]["language_code"], "EN")
            self.assertEqual(manifest[0]["version"], 7)
            self.assertEqual(
                manifest[0]["download_url"],
                "https://github.com/DuMoH112/words-lexicons/releases/download/v7/en_words.txt.gz",
            )
            self.assertEqual(manifest[0]["sha256"], archive_hash)
            self.assertEqual(manifest[0]["byte_size"], archive_path.stat().st_size)
            self.assertEqual(manifest[0]["word_count"], 3)
            self.assertEqual(manifest[0]["source_name"], "ESDB/SCOWL")
            self.assertEqual(manifest[0]["source_url"], "https://github.com/en-wl/wordlist")
            self.assertEqual(manifest[0]["source_license"], "ESDB MIT-like notice")
            self.assertTrue(manifest[0]["generated_at"].endswith("Z"))


if __name__ == "__main__":
    unittest.main()
