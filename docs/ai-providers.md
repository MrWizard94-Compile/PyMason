# AI Providers (PyMason)

PyMason’s AI Chat supports three providers. Settings are stored **only in browser `localStorage`** (or Electron’s web storage).

## xAI Grok (default)

| Setting | Value |
|---------|--------|
| Base URL | `https://api.x.ai/v1` |
| Endpoint | `POST /chat/completions` (OpenAI-compatible) |
| Default model | `grok-4.5` |
| Key | From [console.x.ai](https://console.x.ai) |

Auth: `Authorization: Bearer <key>`

**Note:** Some browsers may block cross-origin calls; if chat fails with a network/CORS error, try another browser or a local reverse proxy. Keys never leave your machine except to xAI.

## Ollama (local)

| Setting | Value |
|---------|--------|
| Base URL | `http://127.0.0.1:11434` |
| Endpoint | `POST /api/chat` |
| Default model | `llama3.2` (pull any model you have) |
| Key | Not required |

```bash
ollama pull llama3.2
# Allow browser origins if needed:
# Windows PowerShell example:
$env:OLLAMA_ORIGINS="*"; ollama serve
```

## Claude (Anthropic)

| Setting | Value |
|---------|--------|
| Endpoint | `https://api.anthropic.com/v1/messages` |
| Default model | `claude-haiku-4-5-20251001` |
| Key | Anthropic console (`sk-ant-…`) |

Uses Anthropic’s browser access header (same as before).

## Setup in the app

1. Open **AI Chat**
2. Choose provider in the dropdown
3. Click **Setup** — set key (if needed), model, and base URL
4. Use quick actions or free-form chat

Workspace blocks + generated code are sent as **system context** with each message.
