# 🕵️‍♂️ APIScanner: Intelligent API Discovery and Vulnerability Analysis Tool

[![Made with Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Follow on X](https://img.shields.io/badge/Follow-@spyizxa-000000?style=flat&logo=x)](https://x.com/spyizxa)

APIScanner is an advanced reconnaissance tool designed to automatically discover API endpoints, hidden parameters, and sensitive data often overlooked during manual penetration testing (pentest) of web applications.

It accelerates the **Vulnerability Research (VR)** process by mapping out the entire attack surface of a target application efficiently.

---

## ✨ Key Features

* **Deep Discovery:** Parses HTML, JavaScript, and XML files, using robust regular expressions (regex) to find embedded API patterns (e.g., `/api/`, `/v1`, `/rest`, `/graphql`).
* **Parameter Analysis:** Extracts and analyzes Query Parameters from discovered URLs, flagging interesting keywords (`token`, `secret`, `key`, `id`) that may lead to information disclosure or vulnerabilities.
* **HTTP Method Testing:** Automatically tests all discovered API endpoints with critical HTTP methods (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`) to identify unhandled or insecure configurations.
* **Header Inspection:** Checks response headers for sensitive information or authentication mechanisms (`Authorization`, `X-API-KEY`, `Set-Cookie`).
* **Readability:** Utilizes the `rich` library to provide clear, professional, and visually engaging output in the terminal.

## 🛠️ Installation

You must have Python 3.x installed on your system to run APIScanner.

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/Spyizxa/APIScanner.git](https://github.com/Spyizxa/APIScanner.git)
    cd APIScanner
    ```

2.  **Install Dependencies:**
    APIScanner relies on libraries such as `requests`, `rich`, `beautifulsoup4`, and `fake-useragent`.
    ```bash
    pip install -r requirements.txt
    ```
    *Note: Ensure your requirements.txt file lists all necessary libraries.*

## 🚀 Usage

The tool runs in an easy-to-use interactive mode:

```bash
python apiscanner.py
