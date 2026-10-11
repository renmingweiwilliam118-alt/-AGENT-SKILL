# Corporate-document knowledge base: upload → parse → retrieve

The pattern when a user says "我是一家培训机构，我希望上传我所有的公司资料比如 excel word pdf，
然后能够自动整理清洗，然后回答客户问题可以参考知识库的内容" — a document-ingest knowledge base
behind an LLM reply composer.

## Shape of the pipeline

```
upload (multi-select native file dialog)
  → parse_upload(path)          # per-extension text extraction
  → _clean_text(text)           # whitespace normalization
  → kb_save(name, text)         # stored as .md in the KB dir
  → kb_search(query)            # token-split fuzzy match, per recognition
  → kb_context(agent, query)    # injected into the composer prompt as 【知识库】
```

Everything after `kb_save` is format-independent: because every document becomes a `.md` file,
the existing list/get/search/delete API and the composer need no format awareness at all. The
whole feature is therefore parse + a search upgrade, not a new subsystem.

## Parsing per format

- `.txt` / `.md` / `.csv` — read as UTF-8 with `errors="ignore"`.
- `.xlsx` — `openpyxl.load_workbook(path, data_only=True, read_only=True)`; iterate
  `ws.iter_rows(values_only=True)`, skip empty cells, join the row with `" | "`, and prefix
  each sheet with `## 工作表：{ws.title}`. `data_only=True` is required or formula cells return
  the formula string instead of the value. Measured: a 2-sheet course/teacher workbook became
  ~180 chars of clean rows.
- `.docx` — `docx.Document(path)`; collect non-empty `p.text` for paragraphs AND iterate
  `d.tables` joining each row's cells with `" | "`. Paragraph-only extraction silently drops
  every table, and company documents keep their contact info and price lists in tables.
- `.pdf` — `PyPDF2.PdfReader(path)`, `pg.extract_text()` per page wrapped in `try/except`
  (some pages raise and must be skipped, not abort the whole document).

`_clean_text` is two substitutions — `[ \t]+\n → \n` and `\n{3,} → \n\n` — plus `strip()`.
Don't skip it: raw extractions carry trailing spaces and page-break runs that eat context budget.

**Parse failures must fall back, not abort the import.** Wrap `parse_upload` in `try/except` and
fall back to reading the file as text; a scanned PDF or a password-protected xlsx then imports as
garbage text instead of failing the whole multi-file selection. Report per-file successes and
failures separately (`{"imported": [...], "failed": [...]}`) so one bad file doesn't hide the
three good ones.

**Packaging**: `openpyxl`, `python-docx`, `PyPDF2` are imports inside `parse_upload`, so the
PyInstaller build needs `--hidden-import openpyxl --hidden-import docx --hidden-import PyPDF2`.
Without them the packaged app raises `ModuleNotFoundError` at the first upload while the dev
run works — the classic "works in dev, dead in the exe" split. Expect the exe to grow by the
three libraries' size (~40 MB → ~47 MB measured).

## Retrieval: exact substring match is the real bug

The default knowledge-base search is `body.count(query)` — a hit only when the customer's whole
question appears verbatim in a document. A customer never does that: "少儿编程课多少钱？" never
appears in a course table, so nothing is retrieved and the composer answers from the model's
priors (it will invent a plausible price, which the user reads as the KB working when it isn't).

**Split the query into tokens and score by how many tokens hit, not by raw frequency.** For
Chinese there are no word boundaries, so generate 2- and 3-character sliding windows over each
contiguous CJK run (plus whole ASCII words via `[a-z0-9]+`), dedupe, and count hits per token:
title hit ×3, body hit ×1, summed into a score, with a separate `hit_toks` counter. Sort by
`hit_toks` descending first, then score — ranking by token coverage first stops one long document
from monopolising the results on raw term frequency.

Measured after the change, with a course table + intro imported:

| question | retrieved |
|---|---|
| 少儿编程课多少钱？ | course table (5 tokens) + intro (2) |
| 你们有哪些课程 | course table |
| 有英语课吗 | course table |
| 联系电话是多少 | intro |

Keep the retrieval result bounded (`max_kb` ≈ 3500 chars) and log which documents were injected,
so "为什么它没参考我的资料" is answerable from the log.

## Honest note to give the user

The KB grounds the composer when a document matches; it does not stop the model answering from
priors when nothing matches. Say this plainly and offer the two mitigations: upload the complete
document set, and/or add "只依据知识库回答，没有的就说需要确认，不要编造" to the custom reply
instruction (SKILL.md rule 25).
