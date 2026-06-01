# 📬 omnisend-pro — Professional desktop bulk email sender built with Python & CustomTkinter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/zougar99/omnisend-pro/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/zougar99/omnisend-pro?style=social)](https://github.com/zougar99/omnisend-pro)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-blue)](https://github.com/zougar99/omnisend-pro)

> Professional desktop bulk email sender built with Python & CustomTkinter. Multi-SMTP rotation, HTML templates, CSV import, and detailed delivery reports.

---

## 📖 Table of Contents
- [Features](#-features)
- [How It Works](#-how-it-works)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage Guide](#-usage-guide)
- [Screenshots](#-screenshots)
- [Roadmap](#-roadmap)
- [FAQ](#-faq)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features
- ✔ **Bulk Sending** — Send thousands of emails with multi-SMTP rotation
- ✔ **HTML Templates** — Built-in editor with responsive templates
- ✔ **CSV Import** — Import recipients with custom fields for personalization
- ✔ **SMTP Rotation** — Rotate between unlimited SMTP servers
- ✔ **Delivery Reports** — Sent, failed, bounced — per-recipient tracking
- ✔ **Rate Limiting** — Configurable emails per hour per SMTP
- ✔ **Personalization** — {{name}}, {{company}}, custom field merging

---

## 🔮 How It Works

```
  Input ──► Processing Pipeline ──► Output
  ┌────────┐   ┌────────┐   ┌────────┐
  │ Data   │──►│ Engine │──►│ Result │
  │ Source │   │ Logic  │   │        │
  └────────┘   └────────┘   └────────┘
```

1. **Input** — Load data from file, API, or user input
2. **Process** — Core engine applies logic/analysis/transformation
3. **Output** — Results displayed in UI, saved to file, or sent via API

---

## 💻 Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.10+ |
| UI | CustomTkinter |
| Email | smtplib + Jinja2 |
| Storage | SQLite |
| Platform | Windows / Linux |

---

## 🚀 Installation

```bash
git clone https://github.com/zougar99/omnisend-pro.git
cd omnisend-pro
pip install -r requirements.txt
```

---

## 📄 Configuration

Create a `config.yaml` or `.env` file in the project root:

```yaml
# Application settings
debug: false
port: 8080
theme: dark
language: en
```

---

## 🧰 Usage Guide

1. Launch: `python main.py`
2. Add SMTP servers in Settings
3. Import CSV with recipient data
4. Design email template
5. Configure rate limits
6. Click **Send**

---

## 🖼 Screenshots

> *(Screenshots coming soon. PRs welcome!)*

---

## 🔄 Roadmap

- 🟢 Web dashboard
- 🟡 Mobile companion app
- ⚫ API access
- ⚫ Plugin system
- ⚫ Multi-language support

---

## ❓ FAQ

### How many emails can I send per day?
Depends on your SMTP limits. The app manages rotation to respect each SMTP's limits.

### Does it support attachments?
Yes — you can attach files to campaigns.

---

## 🚧 Troubleshooting

| Problem | Solution |
|---------|----------|
| **App won't start** | Check Python version (3.10+); run `pip install -r requirements.txt` |
| **No output** | Check logs in `logs/` folder; enable debug mode in config |
| **Performance issues** | Close other applications; reduce batch size in config |
| **Dependency errors** | Create fresh venv: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt` |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📐 License
Distributed under the **MIT License**. See [`LICENSE`](https://github.com/zougar99/omnisend-pro/blob/main/LICENSE) for more information.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/zougar99">zougar99</a>
</p>
