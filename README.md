# APIScanner v2 – Endpoint Discovery Tool

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat&logo=python)
![Version](https://img.shields.io/badge/Version-v2.0-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green.svg)
[![Follow on X](https://img.shields.io/badge/Follow-@spyizxa-000000?style=flat&logo=x)](https://x.com/spyizxa)
![Telegram](https://img.shields.io/badge/Contact-%40spyizxa__0day-2CA5E0?logo=telegram)


**Real endpoints only. No noise. No false positives.**

---

## Features

- **Zero-Noise Filtering** – Eliminates garbage like `px`, `400`, `lütfen giriniz`, etc.
- Deep JavaScript crawling & endpoint extraction
- Supports `/api/`, `/v1-v9/`, `/graphql`, `/admin`, `/auth`, `/rest`, Next.js `_next/data/`
- Full subdomain support (`www.`, `cdn.`, `api.`, `static.`)
- Automatic testing with `GET` & `POST`
- Live / Auth / Forbidden status detection
- Multi-threaded (12 threads by default)
- Telegram reporting for multi-scan
- Beautiful terminal UI powered by `rich`
- Single target & batch scanning (`sites.txt`)

---

## Installation

```bash
git clone https://github.com/spyizxa/APIScanner.git
cd APIScanner
pip install -r requirements.txt
python3 APIScanner.py
