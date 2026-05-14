# Notex - Windows version

A minimal desktop note-taking app with built-in AI assistance.
Built with PySide6 + Mistral API.

## Setup

1. Clone the repo:
```bash
   git clone https://github.com/gaspardrld/notex.git
   cd notex
```

2. Create a `.env` file in `mistral_/`:
MISTRAL_API_KEY=your_key_here

Get your key from [console.mistral.ai](https://console.mistral.ai)

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

4. Run:
```bash
   python main.py
```

## Usage

Type `/your question` in any note to get an AI response inline.

## Shortcuts

| Shortcut          | Action                          |
| ----------------- | ------------------------------- |
| `Ctrl + Space`    | Show/hide Notex (global)        |
| `Ctrl + ,`        | Open settings                   |
| `Ctrl + A`        | Open settings                   |
| `Ctrl + Q`        | Quit                            |
| `Esc`             | Hide window                     |
| `Enter`           | Save note / send AI query       |
| `Shift + Enter`   | New line                        |
| `/<prompt>` | Trigger AI response in any note |