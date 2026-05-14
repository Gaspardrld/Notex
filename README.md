# Notex

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
   pip install PySide6 mistralai
```

4. Run:
```bash
   python main.py
```

## Usage

Type `/notex your question` in any note to get an AI response inline.