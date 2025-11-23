# APIScanner v2 – Endpoint Discovery Tool

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat&logo=python)
![Version](https://img.shields.io/badge/Version-v2.0-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green.svg)
[![Follow on X](https://img.shields.io/badge/Follow-@spyizxa-000000?style=flat&logo=x)](https://x.com/spyizxa)
![Telegram](https://img.shields.io/badge/Contact-%40spyizxa__0day-2CA5E0?logo=telegram)


**APIScanner is an advanced reconnaissance tool designed to automatically discover API endpoints, hidden parameters, and sensitive data that are often overlooked during manual penetration testing (pentesting) of web applications. Real endpoints only. No noise. No false positives.**

---

## Features

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
git clone https://github.com/spyizxa0day/APIScanner.git
cd APIScanner
pip install -r requirements.txt
python3 APIScanner.py
