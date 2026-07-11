# Local LLM with Ollama on Apple Silicon

> Your complete guide to installing, running, and configuring local AI models on Apple Silicon Macs using Ollama — from first install to API endpoints and custom model configurations.

**Applies to:** macOS, Apple Silicon (M1–M5), Ollama, local AI inference
**Last updated:** 2026-04-06
**Version:** 2.1

---

## Table of Contents

- [What This Guide Covers](#what-this-guide-covers)
- [Quick Start (5 Minutes)](#quick-start-5-minutes)
- [Your First Conversation](#your-first-conversation)
- [Choosing a Model](#choosing-a-model)
- [Running Ollama: On-Demand vs. Persistent](#running-ollama-on-demand-vs-persistent)
- [The API: Connecting Other Apps](#the-api-connecting-other-apps)
- [GUI Frontends](#gui-frontends)
- [Configuration and Tuning](#configuration-and-tuning)
- [Custom Modelfiles](#custom-modelfiles)
- [Common Mistakes](#common-mistakes)
- [Troubleshooting](#troubleshooting)
- [Alternatives to Ollama](#alternatives-to-ollama)
- [Resources](#resources)

---

## What This Guide Covers

Ollama is the simplest way to run open-source AI models locally on your Mac. Instead of sending your prompts to a cloud service like ChatGPT or Claude, you download a model to your machine and run it entirely offline. Your data never leaves your computer.

This guide walks you through two paths to get running:

- **Desktop App (recommended for most people):** Download, install, double-click. The app runs in the background and handles everything for you, including the command-line tools and the API server.
- **CLI-only (Homebrew):** Better if you prefer not to run a menu-bar app, want to manage Ollama as a background service yourself, run a headless Mac (e.g., a Mac Mini server), or are already comfortable in the terminal.

Both paths give you the same capabilities. The desktop app is just the CLI + a lightweight menu-bar wrapper that auto-starts the server for you.

### What you'll need

- A Mac with Apple Silicon (M1 or later) — this guide is written for a MacBook with 24GB of unified memory, but the model tables cover 16GB through 48GB+
- A few GB of free disk space per model (most models are 4–10GB)
- Basic comfort with Terminal (for anything beyond the Quick Start)

---

## Quick Start (5 Minutes)

### Path A: Desktop App (Recommended)

1. Download the macOS app from [ollama.com/download](https://ollama.com/download)
2. Open the `.dmg` and drag Ollama to Applications
3. Launch Ollama — it will appear in your menu bar (the llama icon)
4. Open Terminal and run:

```bash
ollama run qwen3.5:9b
```

That's it. Ollama downloads the model (~7GB) and drops you into a chat. Type a message and hit Enter.

### Path B: CLI via Homebrew

Use this if you don't want a menu-bar app, or you're setting up a headless server.

```bash
brew install ollama
```

Unlike the desktop app, the Homebrew install doesn't run a background server automatically. You need to start it yourself before you can use any `ollama` commands:

```bash
ollama serve &           # start the server in the background
ollama run qwen3.5:9b      # pull and chat
```

> **Why would I choose CLI-only?** If you're running Ollama on a Mac Mini as a home server, scripting model management in automation, or you simply don't like menu-bar apps. For casual use on a laptop, the desktop app is easier.

### Verify your install

```bash
ollama --version        # confirm installed version
ollama list             # see downloaded models
ollama ps               # see running models and memory usage
```

---

## Your First Conversation

After `ollama run qwen3.5:9b`, you're in an interactive chat session. It looks like this:

```
>>> What's the capital of France?
The capital of France is Paris. It's the country's largest city and serves as
the political, economic, and cultural center of France.

>>> Tell me something surprising about it
One surprising fact: Paris has only one stop sign in the entire city. Traffic
flow is managed almost entirely through priority-to-the-right rules and traffic
lights.

>>> /bye
```

**Key commands inside a chat session:**

| Command | What it does |
|---------|-------------|
| `/bye` or Ctrl+D | Exit the conversation |
| `/help` | Show all available commands |
| `/set parameter temperature 0.3` | Adjust a parameter on the fly |
| `/show info` | Show current model details |
| `/clear` | Clear conversation history |

### Useful CLI commands outside of chat

```bash
ollama list                    # list downloaded models
ollama show qwen3.5:9b           # inspect model details (parameters, quantization, etc.)
ollama ps                        # see what's loaded in memory and how much RAM it's using
ollama stop qwen3.5:9b           # unload a model from memory
ollama rm qwen3.5:9b             # delete a model from disk
ollama pull deepseek-r1:14b      # download a model without starting a chat
ollama cp qwen3.5:9b my-qwen     # copy/rename a model
```

---

## Choosing a Model

Models come in different sizes, measured in **parameters** (e.g., 8B = 8 billion parameters). Bigger models are generally smarter but use more memory and run slower. The tables below show what fits comfortably at each RAM tier.

**Quantization** is how models are compressed to fit in less memory. Think of it like JPEG compression for AI — a Q4 model uses roughly half the memory of the original with only a small quality loss. When you `ollama pull` a model, you almost always get a Q4 version by default, which is the right choice for local use.

**Multimodal models** can process images (and sometimes audio) in addition to text — you can ask them to describe a photo, read a screenshot, or analyze a diagram. Models marked with 📷 in the tables below support image input. Most text-only models do not.

### 16GB RAM

| Model | Command | RAM Used | Best for |
|-------|---------|----------|----------|
| Qwen 3.5 9B 📷 | `ollama run qwen3.5:9b` | ~7GB | General purpose (top pick) — multimodal, 256K context, thinking mode |
| Qwen 3 8B | `ollama run qwen3:8b` | ~5GB | General purpose — lighter alternative if RAM is tight |
| Gemma 4 E4B 📷 | `ollama run gemma4:e4b` | ~10GB | General purpose + image understanding |
| Gemma 4 E2B 📷 | `ollama run gemma4:e2b` | ~7GB | Lightweight multimodal (images + audio) |
| Llama 3.3 8B | `ollama run llama3.3:8b` | ~5GB | All-rounder |
| Mistral 7B | `ollama run mistral` | ~5GB | Fast responses |

### 24GB RAM

| Model | Command | RAM Used | Best for |
|-------|---------|----------|----------|
| Qwen 3.5 9B 📷 | `ollama run qwen3.5:9b` | ~7GB | General purpose (top pick) — multimodal, 256K context, thinking mode |
| Gemma 4 E4B 📷 | `ollama run gemma4:e4b` | ~10GB | General purpose + image understanding |
| Qwen 2.5 Coder 14B | `ollama run qwen2.5-coder:14b` | ~10GB | Coding (top local coding model) |
| DeepSeek R1 14B | `ollama run deepseek-r1:14b` | ~10GB | Reasoning, chain-of-thought |
| Gemma 4 26B MoE 📷 | `ollama run gemma4:26b` | ~18GB | High quality at small-model speed (tight fit — see note) |
| Qwen 3.5 27B 📷 | `ollama run qwen3.5:27b` | ~18GB | Best general quality at this tier (tight fit at 24GB) |
| Mistral Small 3 | `ollama run mistral-small` | ~8GB | Fast, good quality |

### 32GB+ RAM

| Model | Command | RAM Used | Best for |
|-------|---------|----------|----------|
| Gemma 4 26B MoE 📷 | `ollama run gemma4:26b` | ~18GB | High quality at small-model speed — comfortably fits at 32GB |
| Qwen 3.5 27B 📷 | `ollama run qwen3.5:27b` | ~18GB | Strong general quality, multimodal, 256K context |
| Gemma 4 31B Dense 📷 | `ollama run gemma4:31b` | ~20GB | Top-tier quality, multimodal (#3 on Arena leaderboard) |
| Qwen 3 32B | `ollama run qwen3:32b` | ~22GB | Strong all-round text performance |
| DeepSeek R1 32B | `ollama run deepseek-r1:32b` | ~22GB | Complex reasoning |
| Llama 3.3 70B (Q4) | `ollama run llama3.3:70b` | ~40GB | Needs 48GB+ — near cloud quality |

### Quantization Options

If you see a model offered in multiple quantization levels:

| Tag suffix | Memory | Quality | When to use |
|------------|--------|---------|-------------|
| (default / Q4_K_M) | Lowest | Very good | Default for most users — just `ollama pull model:size` |
| Q5_K_M | ~25% more | Slightly better | If you have RAM headroom |
| Q8_0 | ~2x of Q4 | Near-original | Only if it still fits comfortably in your RAM |
| FP16 | ~4x of Q4 | Original | Almost never locally — use cloud APIs instead |

> **Rule of thumb:** If a model's RAM usage is more than ~75% of your total RAM, it will run slowly or cause your system to swap. Pick a smaller model or a more aggressive quantization.

### A note on Gemma 4 and Mixture-of-Experts (MoE)

The Gemma 4 26B model uses a technique called **Mixture-of-Experts**. Despite having 25.2 billion total parameters, it only activates 3.8 billion on each token — the rest sit idle. This means it downloads like a large model (~18GB) but runs at speeds closer to a small model, while delivering quality closer to a large one. It's a genuinely different tradeoff from the other models listed above.

The catch: it still needs enough RAM to hold all 25.2B parameters in memory, even though only a fraction are active at any moment. On 24GB this is a tight fit (close to the 75% guideline); on 32GB it runs comfortably.

The **Gemma 4 31B Dense** model, by contrast, uses all its parameters on every token — higher quality ceiling, but proportionally more RAM and slower inference.

Both Gemma 4 models are **multimodal**: they accept images as input, so you can ask them to describe a photo, read text from a screenshot, or analyze a chart. The smaller E2B and E4B variants also accept audio. This is something the text-only models (Qwen, Llama, DeepSeek, Mistral) in the tables above cannot do.

### Disk space

Each model takes 4–25GB+ on disk. Check your available space before downloading several:

```bash
df -h ~                    # check disk space
ollama list                # see size of each downloaded model
ollama rm model-name       # delete a model you no longer need
```

---

## Running Ollama: On-Demand vs. Persistent

There are two ways to think about running Ollama, and it's important to understand the difference:

**The Ollama server** is the background process that loads models and serves requests. **A model** is loaded into the server's memory when you use it.

### On-demand (default behavior)

If you installed the desktop app and it's running (llama icon visible in your menu bar), the server is already active. Just open Terminal and run commands:

```bash
ollama run qwen3.5:9b     # loads model, starts chat — model stays in memory after you exit
```

By default, a model stays loaded in memory for 5 minutes after your last interaction, then unloads itself to free RAM. You can change this timeout:

```bash
# Keep model loaded for 1 hour
ollama run qwen3.5:9b --keepalive 1h

# Keep model loaded indefinitely (until you manually stop it)
ollama run qwen3.5:9b --keepalive -1

# Unload immediately when you exit
ollama run qwen3.5:9b --keepalive 0
```

### Persistent (always-on server)

If you want Ollama available at all times — say, for other apps to call its API — you have two options.

**Option 1: Desktop app with "Launch at Login"**

Click the Ollama menu-bar icon → Settings → toggle "Launch at Login." Ollama starts when you log in and runs in the background. This is the easiest approach for a personal laptop.

**Option 2: LaunchAgent (CLI install, or for a headless server)**

Create a LaunchAgent so macOS automatically starts `ollama serve` at login:

```bash
mkdir -p ~/Library/LaunchAgents

cat <<'EOF' > ~/Library/LaunchAgents/com.ollama.serve.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ollama.serve</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/ollama</string>
        <string>serve</string>
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>OLLAMA_MAX_LOADED_MODELS</key>
        <string>1</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/ollama.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/ollama.err.log</string>
</dict>
</plist>
EOF

# Load the service
launchctl load ~/Library/LaunchAgents/com.ollama.serve.plist
```

To stop or unload:

```bash
launchctl unload ~/Library/LaunchAgents/com.ollama.serve.plist
```

> **Why use a LaunchAgent?** The desktop app handles this for you with the "Launch at Login" toggle. Use a LaunchAgent when you need to set environment variables (like `OLLAMA_HOST` for network access) that the desktop app doesn't expose, or when running on a headless system with no GUI.

---

## The API: Connecting Other Apps

Whenever Ollama is running (whether via the desktop app or `ollama serve`), it exposes a REST API at `http://localhost:11434`. This is how other applications — coding assistants, chat UIs, automation scripts — talk to your local models.

### Check that the server is running

```bash
curl http://localhost:11434
# Should return: Ollama is running
```

### Generate a completion (one-shot)

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "qwen3.5:9b",
  "prompt": "Explain quantum computing in one paragraph.",
  "stream": false
}'
```

Set `"stream": false` to get the full response in a single JSON object. Without it, you'll get a stream of partial responses (useful for building chat UIs, less useful for scripting).

### Chat with message history

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "qwen3.5:9b",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant. Be concise."},
    {"role": "user", "content": "What is the tallest mountain on Earth?"}
  ],
  "stream": false
}'
```

### Key API endpoints

| Endpoint | Method | What it does |
|----------|--------|-------------|
| `/api/generate` | POST | Text completion from a prompt |
| `/api/chat` | POST | Chat completion with message history |
| `/api/embeddings` | POST | Generate vector embeddings |
| `/api/tags` | GET | List downloaded models |
| `/api/show` | POST | Show model details |
| `/api/pull` | POST | Download a model |
| `/api/delete` | DELETE | Remove a model |
| `/api/ps` | GET | List models currently loaded in memory |
| `/api/version` | GET | Show Ollama version |

### Making Ollama accessible from other devices

By default, Ollama only listens on `localhost` (127.0.0.1) — other devices on your network can't reach it. To change this:

```bash
# Listen on all network interfaces
export OLLAMA_HOST=0.0.0.0

# Or a specific IP
export OLLAMA_HOST=192.168.1.100
```

Add this to your `~/.zshrc` to persist it, or include it in your LaunchAgent plist (see the persistent server section above).

> **Security note:** Ollama has no built-in authentication. If you bind to `0.0.0.0`, anyone on your network can use your models and your machine's resources. Only do this on a trusted home or office network.

### Apps that work with Ollama's API

Many tools can connect to Ollama out of the box by pointing them at `http://localhost:11434`:

- **Open WebUI** — ChatGPT-like web interface for local models
- **Continue** (VS Code / JetBrains) — AI coding assistant using local models
- **Cline** (VS Code) — autonomous coding agent
- **LangChain / LlamaIndex** — Python frameworks for building AI applications

---

## GUI Frontends

If you'd rather chat through a browser interface than the terminal, **Open WebUI** is the most popular option. It gives you a ChatGPT-like experience running entirely on your machine:

```bash
# Requires Docker
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway \
  --name open-webui ghcr.io/open-webui/open-webui:main
```

Then open `http://localhost:3000` in your browser. Open WebUI auto-detects your Ollama instance and lists all your downloaded models.

> **No Docker?** LM Studio is a standalone desktop app that includes its own model runner and a built-in chat UI. It doesn't need Ollama at all, but it also can't share models with Ollama.

---

## Configuration and Tuning

> **For beginners:** The defaults work well. Skip this section until you have a specific reason to change something — then come back.

### Environment variables

Add these to `~/.zshrc` to persist across sessions:

```bash
# Limit to one model loaded at a time — prevents memory contention
export OLLAMA_MAX_LOADED_MODELS=1

# Change where models are stored (default: ~/.ollama/models)
export OLLAMA_MODELS=/path/to/external/drive/ollama/models

# Bind to all interfaces for network access (default: 127.0.0.1)
export OLLAMA_HOST=0.0.0.0
```

> **Note on Metal GPU acceleration:** Ollama automatically uses Apple's Metal framework for GPU acceleration on all Apple Silicon Macs. You don't need to set any environment variable to enable this — it just works.

### Runtime parameters

These control how a model behaves. You can set them in a Modelfile (see next section), via the API, or on the fly during a chat session with `/set parameter`.

| Parameter | Default | What it does |
|-----------|---------|-------------|
| `num_ctx` | 2048 | **Context window** — how many tokens of conversation the model can "see." Higher values let it handle longer conversations but use more RAM. Start with 4096; go to 8192 if you need longer context. |
| `temperature` | 0.8 | **Creativity.** Lower (0.1–0.3) = more precise and deterministic. Higher (0.8–1.0) = more creative and varied. Use low for code/facts, higher for creative writing. |
| `num_predict` | 128 | **Max response length** in tokens. Set to -1 for unlimited. |
| `top_p` | 0.9 | **Nucleus sampling.** Controls the diversity of word choices. Lower = more focused. Most users never need to change this. |
| `top_k` | 40 | **Top-K sampling.** Limits choices to the top K most likely tokens. Lower = less random. |
| `repeat_penalty` | 1.1 | **Repetition penalty.** Values above 1.0 discourage the model from repeating itself. |
| `num_gpu` | auto | **GPU layers.** How many model layers run on the GPU. Set to 99 to force all layers onto GPU. Auto is correct for almost everyone. |
| `num_batch` | 512 | **Batch size** for prompt processing. Higher = faster prompt ingestion, more memory. |

### Memory-constrained tips (24GB or less)

- Only load one model at a time (`OLLAMA_MAX_LOADED_MODELS=1`)
- Start with `num_ctx` at 4096; only increase if you actually need longer context
- Close memory-heavy apps (browsers with many tabs, IDEs) when running 14B+ models
- Monitor with `ollama ps` to check actual memory consumption
- If your system feels sluggish, check Activity Monitor for "Memory Pressure" — yellow or red means you need a smaller model or lower context

---

## Custom Modelfiles

A **Modelfile** is a simple text file that creates a customized version of any model. Think of it like a saved configuration: you pick a base model, set your preferred parameters, and give it a system prompt — then save it as a new model you can run by name.

This is one of Ollama's most powerful features. Instead of passing parameters every time, you bake them into a named model you can reuse.

### Anatomy of a Modelfile

```dockerfile
# Every Modelfile starts with FROM — the base model
FROM qwen3.5:9b

# Set parameters (optional — overrides defaults)
PARAMETER num_ctx 8192
PARAMETER temperature 0.7

# Set a system prompt (optional — shapes the model's personality/behavior)
SYSTEM """You are a helpful assistant. Be concise and direct.
When you don't know something, say so."""
```

### All Modelfile instructions

| Instruction | Required? | What it does |
|-------------|-----------|-------------|
| `FROM` | Yes | Base model to build on — e.g., `qwen3.5:9b`, `deepseek-r1:14b` |
| `PARAMETER` | No | Set any runtime parameter (see the table in Configuration) |
| `SYSTEM` | No | System prompt — shapes the model's behavior and personality |
| `TEMPLATE` | No | Override the prompt template (advanced — uses Go template syntax) |
| `ADAPTER` | No | Apply a fine-tuned LoRA adapter (advanced) |
| `MESSAGE` | No | Pre-seed conversation with example messages to guide behavior |
| `LICENSE` | No | Attach a license string |

### Example: General-purpose assistant

```bash
cat <<'EOF' > ~/.ollama/modelfiles/assistant.modelfile
FROM qwen3.5:9b

PARAMETER num_ctx 8192
PARAMETER temperature 0.7
PARAMETER repeat_penalty 1.1

SYSTEM """You are a knowledgeable assistant. Provide clear, accurate answers.
Be concise — avoid unnecessary preamble. When uncertain, say so."""
EOF

ollama create assistant -f ~/.ollama/modelfiles/assistant.modelfile
ollama run assistant
```

### Example: Coding assistant

```bash
cat <<'EOF' > ~/.ollama/modelfiles/coder.modelfile
FROM qwen2.5-coder:14b

PARAMETER num_ctx 8192
PARAMETER temperature 0.2
PARAMETER repeat_penalty 1.1
PARAMETER num_predict -1

SYSTEM """You are a senior software engineer. Write clean, efficient,
well-commented code. Provide only code unless the user asks for an explanation.
Follow the conventions of whatever language the user is working in."""
EOF

ollama create coder -f ~/.ollama/modelfiles/coder.modelfile
ollama run coder
```

### Example: Reasoning / analysis

```bash
cat <<'EOF' > ~/.ollama/modelfiles/reasoner.modelfile
FROM deepseek-r1:14b

PARAMETER num_ctx 8192
PARAMETER temperature 0.3

SYSTEM """You are an analytical assistant. Think step by step.
Consider multiple perspectives before reaching a conclusion.
Show your reasoning process."""
EOF

ollama create reasoner -f ~/.ollama/modelfiles/reasoner.modelfile
ollama run reasoner
```

### Example: Using MESSAGE for few-shot prompting

The `MESSAGE` instruction lets you pre-seed a conversation with examples, teaching the model your preferred response style:

```bash
cat <<'EOF' > ~/.ollama/modelfiles/concise.modelfile
FROM qwen3.5:9b

PARAMETER temperature 0.5

SYSTEM "Answer questions directly and concisely."

MESSAGE user "What is Docker?"
MESSAGE assistant "A platform for running applications in isolated containers — lightweight, portable, and consistent across environments."

MESSAGE user "What is Kubernetes?"
MESSAGE assistant "An orchestration system for managing containerized applications at scale — handles deployment, scaling, and networking across clusters."
EOF

ollama create concise -f ~/.ollama/modelfiles/concise.modelfile
ollama run concise
```

### Where Modelfiles live (and how to manage them)

This is an important concept that trips people up: **Ollama doesn't look for Modelfiles in any special directory.** A Modelfile is just a plain text file you write — it has no required location, no required extension, and no special format beyond the instructions described above.

You only use a Modelfile once, when you run `ollama create`. That command reads your text file, bakes the configuration into Ollama's internal model storage (`~/.ollama/models/`), and never references the file again. After creation, your Modelfile is just a backup and reference copy for you — Ollama doesn't know or care where it is, or even if it still exists.

This means **you** are responsible for keeping your Modelfiles somewhere you can find and edit them. If you lose one, you can reconstruct it (see below), but it's easier to just stay organized from the start.

**Recommended location:** `~/.ollama/modelfiles/`

This keeps your Modelfiles alongside Ollama's own data directory (`~/.ollama/models/`), and the naming makes the relationship obvious. You can use any location you prefer — the important thing is to pick one and be consistent.

**Recommended workflow:**

```bash
# 1. Create a dedicated directory for your Modelfiles
mkdir -p ~/.ollama/modelfiles

# 2. Create or edit a Modelfile with any text editor
nano ~/.ollama/modelfiles/coder.modelfile
# Or: code ~/.ollama/modelfiles/coder.modelfile   (VS Code)
# Or: open -a TextEdit ~/.ollama/modelfiles/coder.modelfile

# 3. Build the model from it
ollama create coder -f ~/.ollama/modelfiles/coder.modelfile

# 4. When you want to change something, edit the file and rebuild
nano ~/.ollama/modelfiles/coder.modelfile
ollama create coder -f ~/.ollama/modelfiles/coder.modelfile   # overwrites the previous version
```

**Recovering a Modelfile you've lost:**

If you already created a model but no longer have the source Modelfile, you can reconstruct it:

```bash
# Print a reconstructed Modelfile to the terminal
ollama show --modelfile coder

# Save it to a file so you can edit and rebuild from it
ollama show --modelfile coder > ~/.ollama/modelfiles/coder.modelfile
```

The reconstructed file won't be identical to your original (comments are lost, formatting may differ), but it captures all the functional settings: base model, parameters, system prompt, and template.

### Managing your custom models

```bash
ollama list                    # see all models including your custom ones
ollama show assistant          # inspect parameters and system prompt
ollama show --modelfile assistant  # print the reconstructed Modelfile
ollama cp assistant assistant-v2   # duplicate before modifying
ollama rm assistant            # delete a custom model
```

### Tips for effective Modelfiles

- **Temperature for the task:** 0.1–0.3 for code and factual work, 0.5–0.7 for general assistance, 0.8–1.0 for creative writing.
- **System prompts matter a lot.** A good system prompt shapes the model's behavior more than any parameter. Be specific about what you want and don't want.
- **Keep system prompts short.** Long, elaborate system prompts eat into your context window. 2–4 sentences is usually enough.
- **Use MESSAGE sparingly.** A couple of examples is effective; a dozen wastes context on examples instead of leaving room for your actual conversation.
- **Version your Modelfiles.** Save them to a directory (e.g., `~/.ollama/modelfiles/`) and treat them like config files. This makes it easy to recreate your models after an Ollama update.

---

## Common Mistakes

### Loading multiple large models at the same time

On 24GB of RAM, loading two 14B models simultaneously causes memory swapping and makes everything crawl. Set `OLLAMA_MAX_LOADED_MODELS=1`, or manually stop a model before loading another: `ollama stop model-name`.

### Setting the context window too high

Setting `num_ctx` to 32768 on a 14B model with 24GB RAM will exhaust memory. Context window directly trades RAM for conversation length. Start at 4096 and increase only when you actually need longer conversations.

### Running a model that's too big for your RAM

If a model's RAM usage (shown by `ollama ps`) is close to or exceeds your total RAM, your system will swap to disk and inference will be painfully slow. Pick a smaller model or a more aggressive quantization — the speed difference is dramatic while the quality difference is subtle.

### Downloading FP16 (unquantized) models

Full-precision models use roughly 4x the memory of Q4 quantized versions with minimal quality gain for interactive use. Always use quantized versions locally. The defaults from `ollama pull` are already quantized.

### Not checking disk space

It's easy to accumulate dozens of GB in models without noticing. Run `ollama list` periodically and `ollama rm` anything you're not using.

---

## Troubleshooting

### Slow generation or system feels sluggish

**Cause:** The model is too large for your available RAM, causing disk swapping.

```bash
ollama ps                        # check memory usage
ollama stop model-name           # unload it
ollama run smaller-model         # switch to something that fits
```

Also check Activity Monitor → Memory tab. If "Memory Pressure" is yellow or red, you need to free up RAM (close apps, use a smaller model, or reduce `num_ctx`).

### "ollama" command not found

**Cause:** CLI not in your PATH.

```bash
# Desktop app installs the CLI to /usr/local/bin/ollama
# If not found, restart your terminal. If still missing:
export PATH="/usr/local/bin:$PATH"
# Add the line above to ~/.zshrc to make it permanent
```

### "Error: could not connect to Ollama server"

**Cause:** The Ollama server isn't running.

```bash
# If you use the desktop app: make sure the llama icon is in your menu bar
# If you use Homebrew: start the server manually
ollama serve
```

### Model downloads fail or stall

**Cause:** Network issues or insufficient disk space.

```bash
df -h ~                              # check disk space
ollama pull model-name               # retry — Ollama resumes partial downloads
```

### Context window errors or "out of memory"

**Cause:** `num_ctx` is set higher than your RAM can support for that model.

**Fix:** Reduce `num_ctx` in your Modelfile, or use a smaller model. As a rough guide, doubling `num_ctx` adds ~1–2GB of RAM usage for a 7–8B model and more for larger models.

---

## Alternatives to Ollama

| Tool | Best for | Notes |
|------|----------|-------|
| **Ollama** | Default choice — lowest friction, CLI + API | What this guide covers |
| **LM Studio** | GUI for browsing, testing, and chatting with models | Standalone app — doesn't need Ollama |
| **MLX (direct)** | Maximum raw performance or fine-tuning on Apple Silicon | `pip install mlx-lm` — 20–30% faster inference than llama.cpp but no built-in API server |

---

## MLX Preview (Ollama 0.19+)

As of late March 2026, Ollama 0.19 introduced a preview of native MLX support — Apple's own machine learning framework, purpose-built for Apple Silicon's unified memory architecture. In benchmarks, it showed ~1.6x faster prompt processing and ~2x faster token generation versus Ollama 0.18.

**Current status (April 2026):** MLX support is in preview, not yet the default backend. It currently supports a limited number of models (notably Qwen3.5-35B-A3B in NVFP4 format) and requires 32GB+ RAM. The full release is expected in Q2 2026 with broader model support. Most users should stick with the default llama.cpp + Metal backend for now — it's stable and performant. MLX is worth watching if you have 32GB+ RAM and want to experiment with cutting-edge performance.

---

## Resources

- [Ollama Official Site](https://ollama.com)
- [Ollama Model Library](https://ollama.com/library) — browse all available models
- [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Ollama Modelfile Reference](https://docs.ollama.com/modelfile)
- [Ollama MLX Blog Post](https://ollama.com/blog/mlx) — MLX preview announcement and benchmarks
- [Open WebUI](https://github.com/open-webui/open-webui) — ChatGPT-like frontend for Ollama
- [Best Local LLMs for Apple Silicon 2026](https://apxml.com/posts/best-local-llms-apple-silicon-mac)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-04-06 | Initial release |
| 2.0 | 2026-04-06 | Major rewrite: beginner-focused structure, API documentation, persistent server setup, expanded Modelfiles section, accuracy corrections |
| 2.1 | 2026-04-07 | Added Gemma 4 models (E2B, E4B, 26B MoE, 31B Dense) and Qwen 3.5 (9B, 27B) to all RAM tiers; Qwen 3.5 9B replaces Qwen 3 8B as default recommendation; MoE explainer, multimodal notes |

---

**Protocol version**: 2.1
**Last updated**: 2026-04-07
**Original source**: Research and configuration for MacBook M5 (24GB) setup
