# Oculus - Web Application Vulnerability Scanner

A Python-based web application vulnerability scanner with both a **web interface** (Flask) and a **command-line interface** (CLI). This tool is designed for educational purposes and authorized penetration testing only.

## Features
- Detects common web vulnerabilities:
  - Reflected & Stored XSS
  - SQL Injection (SQLi)
  - Directory Traversal
  - Optional Intrusive tests (OS Command Injection)
- Web UI for starting scans, monitoring progress, and downloading reports
- CLI for automated scans
- Modular architecture for easy payload & scanner expansion
- Generates structured JSON reports for analysis
- Local vulnerable test server (`vuln_app.py`) included for safe practice

## Installation
```bash
git clone https://github.com/<your-username>/Oculus-Scanner.git
cd Oculus-Scanner
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt


Author : Keerthana N |https://www.linkedin.com/in/keerthana-n-2ofe | keerthanapalakkaparambil@gmail.com