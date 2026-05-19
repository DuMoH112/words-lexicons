# EN license note: ESDB/SCOWL

Источник: `ESDB/SCOWL`.

Upstream:

```text
https://github.com/en-wl/wordlist
```

Upstream copyright file:

```text
https://github.com/en-wl/wordlist/blob/v2/Copyright
```

Короткое практическое решение для этого репозитория:

- код и документация `words-lexicons` лежат под MIT License;
- generated EN artifacts являются производными от `ESDB/SCOWL`;
- для EN используем American word list, size `70`, variant level `1`;
- не используем Australian spelling code `D` и region `AU`;
- не используем generated word list больше size `80`;
- в supporting documentation сохраняем attribution на upstream `ESDB/SCOWL`.

По upstream README combined work доступен под MIT-like license. Upstream
`Copyright` требует сохранять copyright notice и permission notice в supporting
documentation. Перед публичным App Store релизом лучше показать этот файл
юристу, но для технической подготовки release artifacts это достаточный
минимальный attribution contract.
