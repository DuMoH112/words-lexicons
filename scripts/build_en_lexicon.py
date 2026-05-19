#!/usr/bin/env python3
import gzip
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


OWNER_REPO = "DuMoH112/words-lexicons"
LANGUAGE_CODE = "EN"
SOURCE_NAME = "ESDB/SCOWL"
SOURCE_URL = "https://github.com/en-wl/wordlist"
SOURCE_LICENSE = "ESDB MIT-like notice"


def is_game_safe_word(word):
    if len(word) < 3:
        return False

    for char in word:
        if char < "a" or char > "z":
            return False

    return True


def read_plain_wordlist(path):
    with path.open("r", encoding="utf-8") as file:
        return file.readlines()


def read_esdb_wordlist(source_dir):
    db_path = source_dir / "scowl.db"

    if not db_path.exists():
        subprocess.run(["make"], cwd=source_dir, check=True)

    result = subprocess.run(
        [
            "./scowl",
            "--db",
            "scowl.db",
            "word-list",
            "70",
            "A",
            "1",
            "--deaccent",
            "--categories=",
            "--wo-poses=abbr",
        ],
        cwd=source_dir,
        check=True,
        text=True,
        capture_output=True,
    )

    return result.stdout.splitlines()


def build_words(raw_words):
    words = set()

    for raw_word in raw_words:
        word = raw_word.strip()

        if word != word.lower():
            continue

        if is_game_safe_word(word):
            words.add(word)

    return sorted(words)


def write_gzip(text_path, gzip_path):
    data = text_path.read_bytes()

    with gzip_path.open("wb") as output:
        with gzip.GzipFile(filename="", mode="wb", fileobj=output, mtime=0) as file:
            file.write(data)


def sha256(path):
    digest = hashlib.sha256()

    with path.open("rb") as file:
        while True:
            chunk = file.read(1024 * 1024)

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest()


def write_manifest(output_dir, version, word_count, archive_path):
    tag = f"v{version}"
    archive_name = archive_path.name
    generated_at = (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )

    manifest = [
        {
            "language_code": LANGUAGE_CODE,
            "version": version,
            "download_url": f"https://github.com/{OWNER_REPO}/releases/download/{tag}/{archive_name}",
            "sha256": sha256(archive_path),
            "byte_size": archive_path.stat().st_size,
            "word_count": word_count,
            "source_name": SOURCE_NAME,
            "source_url": SOURCE_URL,
            "source_license": SOURCE_LICENSE,
            "generated_at": generated_at,
        }
    ]

    manifest_path = output_dir / "lexicons_manifest.json"
    manifest_json = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    manifest_path.write_text(manifest_json, encoding="utf-8")

    return manifest_path


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: scripts/build_en_lexicon.py "
            "<source-file-or-en-wl-checkout> [output-dir] [version]"
        )
        return 2

    source_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("dist")
    version = int(sys.argv[3]) if len(sys.argv) > 3 else 1

    output_dir.mkdir(parents=True, exist_ok=True)

    if source_path.is_dir():
        raw_words = read_esdb_wordlist(source_path)
    else:
        raw_words = read_plain_wordlist(source_path)

    words = build_words(raw_words)

    text_path = output_dir / "en_words.txt"
    archive_path = output_dir / "en_words.txt.gz"

    text_path.write_text("\n".join(words) + "\n", encoding="utf-8")
    write_gzip(text_path, archive_path)
    manifest_path = write_manifest(output_dir, version, len(words), archive_path)

    print(f"words: {len(words)}")
    print(f"text: {text_path}")
    print(f"archive: {archive_path}")
    print(f"manifest: {manifest_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
