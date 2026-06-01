# 📧 Email Sender Pro

A professional desktop bulk email sending application built with Python and CustomTkinter.

## Features

- **Multiple SMTP Servers** - Add and manage multiple SMTP accounts with TLS/SSL support
- **SMTP Rotation** - Automatically rotate between SMTP servers
- **SMTP Test** - Test connection before sending
- **Email Composer** - HTML and Plain Text support
- **Personalization Variables** - `{email}`, `{name}`, `{date}`, `{time}`, `{random}`
- **Recipient Management** - Manual entry or import from TXT/CSV
- **File Attachments** - Attach multiple files
- **Configurable Delay** - Min/Max delay between emails
- **Real-time Progress** - Live progress bar and detailed log
- **Stop Anytime** - Stop sending mid-process

## Installation

1. Install Python 3.8+

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run:
```bash
py -3 app.py
```

If `py` is not available, use:
```bash
python3 app.py
```

## Common SMTP Settings

| Provider | Host | Port | Encryption |
|----------|------|------|------------|
| Gmail | smtp.gmail.com | 587 | TLS |
| Outlook | smtp-mail.outlook.com | 587 | TLS |
| Yahoo | smtp.mail.yahoo.com | 587 | TLS |
| Custom | your-smtp-server.com | 465 | SSL |

> For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833).
