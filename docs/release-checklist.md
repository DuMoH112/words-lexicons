# Release checklist

## Перед сборкой

- Зафиксирован source словаря и его лицензия.
- Для языка есть note в `sources/`.
- Для языка есть license note в `licenses/`.
- Выбрана новая версия словаря.

## Сборка artifacts

- Сгенерирован `<language>_words.txt`.
- Output отсортирован.
- Output дедуплицирован.
- Output содержит одну lemma на строку.
- Для языка применена нужная нормализация.
- Сгенерирован `<language>_words.txt.gz`.
- Посчитан `sha256` по `.gz` архиву.
- Посчитан `byte_size` `.gz` архива.
- Посчитан `word_count` распакованного словаря.
- Сформирован `lexicons_manifest.json`.

## GitHub Release

- Создан tag release, например `v1`.
- В release загружен `lexicons_manifest.json`.
- В release загружены все `<language>_words.txt.gz`.
- `download_url` в manifest указывает на этот release tag.
- Latest release содержит актуальный manifest.
- В release notes есть ссылка на `licenses/en.md` для EN artifacts.

## Проверка

- Manifest скачивается по latest URL.
- Все `download_url` из manifest открываются.
- `sha256` совпадает с uploaded `.gz`.
- Архив распаковывается локально.
- `word_count` совпадает с количеством строк.
- В словаре нет переводов, описаний и данных учебных паков.
- Для каждого языка сохранена source/license attribution.
