# Words Lexicons

Репозиторий для публикации runtime-словарей валидности приложения Words.

Приложение скачивает отсюда только заранее подготовленные release artifacts:

- `lexicons_manifest.json`
- `<language>_words.txt.gz`

Код и документация этого репозитория распространяются под MIT License. Данные
словарей наследуют условия своих upstream-источников; для `EN` они описаны в
`licenses/en.md`.

Репозиторий не является источником учебного контента. В нем не должно быть
переводов, описаний, категорий, уровней, paid-pack данных и пользовательского
прогресса.

## Назначение

`Global Lexicon` отвечает только на вопрос: существует ли lemma в выбранном
языке обучения.

Учебные данные остаются в `Learning Packs` внутри приложения или будущей системы
паков. Эти два слоя нельзя смешивать.

## GitHub Releases contract

Runtime URL приложения должен указывать на latest release:

```text
https://github.com/<owner>/words-lexicons/releases/latest/download/lexicons_manifest.json
```

Каждый release должен содержать:

- `lexicons_manifest.json`
- один или несколько словарных архивов, например `en_words.txt.gz`

Архив словаря:

- формат: `txt.gz`
- кодировка распакованного `.txt`: `UTF-8`
- содержимое: одна нормализованная lemma на строку
- без метаданных паков и учебных описаний

`sha256` в manifest считается по `.gz` архиву, а не по распакованному `.txt`.

## Manifest

Минимальная запись в `lexicons_manifest.json`:

```json
{
  "language_code": "EN",
  "version": 1,
  "download_url": "https://github.com/DuMoH112/words-lexicons/releases/download/v1/en_words.txt.gz",
  "sha256": "<archive-sha256>",
  "byte_size": 123456,
  "word_count": 155000,
  "source_name": "ESDB/SCOWL",
  "source_url": "https://github.com/en-wl/wordlist",
  "source_license": "ESDB MIT-like notice",
  "generated_at": "2026-05-19T00:00:00Z"
}
```

Пример полного файла лежит в `examples/lexicons_manifest.example.json`.

## Рекомендуемая структура

```text
docs/release-checklist.md
examples/lexicons_manifest.example.json
licenses/<language>.md
scripts/build_en_lexicon.py
sources/<language>.md
```

Сгенерированные `.txt`, `.txt.gz` и рабочие source-checkout директории лучше не
коммитить в git. Их нужно прикладывать к GitHub Release как assets.

## Первый язык

Первая версия планируется для `EN`.

Для `EN` первая нормализация:

- только lowercase `a-z`
- длина от 3 символов
- слова, которые upstream отдал с заглавными буквами, исключаются
- без дефисов
- без апострофов
- без точек
- без цифр
- без спецсимволов

## Сборка EN artifacts

Скрипт не скачивает upstream-данные сам. Перед запуском нужен локальный checkout
`en-wl/wordlist` или уже подготовленный plain word list.

Пример с checkout:

```sh
git clone https://github.com/en-wl/wordlist.git checkouts/en-wl-wordlist
scripts/build_en_lexicon.py checkouts/en-wl-wordlist dist 1
```

Пример с готовым plain word list:

```sh
scripts/build_en_lexicon.py /path/to/words.txt dist 1
```

Output:

- `dist/en_words.txt`
- `dist/en_words.txt.gz`
- `dist/lexicons_manifest.json`
