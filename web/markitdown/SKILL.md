---
name: markitdown
description: Convert PDF/Word/Excel/PowerPoint/HTML/images/audio/CSV/ZIP/Youtube to clean Markdown for LLM/RAG with Microsoft MarkItDown (installed, markitdown[all], Python 3.14). Use when the user wants to turn a document into markdown, extract text from office files/PDFs, batch-convert many files into an LLM-ready corpus, or pre-process docs before feeding a model.
license: MIT (MarkItDown)
---

# MarkItDown

Microsoft's tool for converting many file formats to **Markdown** — ideal for feeding LLMs / RAG. Installed on this machine with the `all` extra (so it covers PDF, PPTX, DOCX, XLSX, HTML, images w/ OCR, audio w/ transcription, CSV/JSON/XML, ZIP, YouTube).

## 本机已装
- `markitdown 0.1.8` + all plugins（含 onnxruntime OCR、speechrecognition、pypdfium2 等），Python 3.14。
- 解释器：`/c/Users/mwr_w/AppData/Local/hermes/tools/python-3.14.7+20260901-win32-x64/python.exe`
- CLI：`python -m markitdown 文件.docx -o 输出.md`；批量：`python -m markitdown dir/ -o out.md`

## 基本用法
```python
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert("report.docx")   # or .pdf/.xlsx/.pptx/.html/.jpg/.mp3
print(result.text_content)
# result.get_document() 拿底层 document 对象；convert_local()/convert_stream() 更细粒度
```

## 什么时候用哪个
| 需求 | 选 |
|---|---|
| 文档 → markdown（喂 LLM/RAG） | **MarkItDown** |
| 单个 PDF 要精读/OCR | 也可用我的 `pdf` 技能；MarkItDown 适合批量 |
| Excel 表格 | MarkItDown 能转，但要看结构用 `xlsx` 技能 |
| 网页 → markdown | 用 `web_extract` / Crawl4AI / Scrapling（MarkItDown 不抓网页） |

## 坑
- 音频转写/图片 OCR 依赖 onnx 模型，首次跑会下载模型（走代理时可能慢）。
- 高保真"给人看"的排版转换不是它强项；它的目标是 LLM 友好，不是印刷级。
