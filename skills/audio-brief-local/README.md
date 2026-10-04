# Audio Brief Local

Turn something you have written into a file you can listen to. Use it to catch
awkward sentences in a draft, or turn a long document into a brief for a walk.
The agent prepares the words; a local speech engine makes the audio.

This is the initial public release, version 0.1.0. It includes no hosted speech integration,
credentials, model weights, recordings or external library connection.

**It does not run through ElevenLabs.** Speech is generated with macOS `say`
or a locally installed Piper model. No ElevenLabs account, API key or voice ID
is used.

## Pick the right mode

| Mode | What happens | Result |
|---|---|---|
| Literal | Wording and order stay intact; formatting and pronunciation changes are disclosed | Audio for proofreading; temporary prepared text |
| Listening brief | An agent writes a new spoken script, preserving facts and qualifications | Separate oral script and audio |

For example, ask: “Read my draft aloud so I can proofread it. Keep my wording.”
Or: “Turn this report into a five-minute listening brief. Keep the uncertainties.”
The agent should say which mode it used. It does not transcribe recordings.

## How it works

1. You provide text or a document the agent can safely extract.
2. The agent chooses literal or listening mode and resolves spoken forms of
   numbers and initialisms. The scripts do not make those judgment calls.
3. `prepare_text.py` strips simple Markdown and lints the result. Strict mode
   rejects digits, currency symbols, percent signs, ampersands, compact
   initialisms, table pipes and bare web addresses. It reports word count and
   a rough duration at 155 words per minute; actual voices vary.
4. `render_local.py` runs macOS `say` once, or Piper once per paragraph. Piper
   paragraphs are joined with 0.45 seconds of silence using the model's actual
   WAV sample rate. FFmpeg encodes an AAC `.m4a`; FFprobe measures duration.
5. Only a successful, nonempty render replaces the chosen output. Temporary
   renderer files are cleaned up. The agent delivers the file and explains
   the mode, voice and changes.

For a non-spoken oral-script header, use the explicit marker in
[walk-oral-brief.md](examples/walk-oral-brief.md). A normal Markdown divider
does not discard everything before it. The source document remains unchanged.

## Run the synthetic example

From this folder, with Python 3.9 or newer:

```sh
python3 scripts/prepare_text.py examples/walk-oral-brief.md -o spoken.txt --strict
```

Preparation needs only Python's standard library. Rendering also needs
`ffmpeg` and `ffprobe` on PATH, plus one of the engines below. Install those
tools through your normal package manager before rendering. The renderer
never installs dependencies or downloads a voice for you.

### macOS

Use an installed system voice, optionally selected with `--voice`:

```sh
python3 scripts/render_local.py -i spoken.txt -o walk.m4a --engine say
```

This uses the system default voice. To select a different installed voice,
pass its exact name with `--voice "VOICE_NAME"`. Discover voices through
system settings or `say -v '?'`; stop a hung enumeration rather than leaving
it running. macOS `say` must execute on the Mac, not inside a Linux container.
The renderer times out each subprocess after 300 seconds by default; use
`--timeout SECONDS` for a longer document. A timeout leaves prior audio intact.

### Piper

Set up a Python virtual environment and install `piper-tts` separately:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install piper-tts
```

Choose a voice whose model-card terms suit your use. Download its `.onnx` and
matching `.onnx.json` with the upstream downloader or manually, into a local
directory. See the [Piper CLI guide](https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/CLI.md).
Then run with that environment's Python:

```sh
python3 scripts/render_local.py -i spoken.txt -o walk.m4a \
  --engine piper --model /path/to/voice.onnx --length-scale 1.02
```

The companion config must be named `voice.onnx.json`. Larger length scale
means slower speech. Optional `--title "A listening brief"` sets file metadata;
use a non-sensitive title when needed. No account, API key, hosted model ID
or private voice identifier is required. Existing output is protected; use
`--overwrite` only when you intend to replace it.

## Use with an agent

The folder follows the Agent Skills format: [SKILL.md](SKILL.md) is the workflow,
with deterministic scripts beside it. Copy the entire folder, not just that
file, into your agent's supported skill directory. Claude Code commonly uses
`~/.claude/skills/`; Codex commonly uses `~/.codex/skills/`. Other agents can read
the workflow directly and run its commands if they have filesystem and shell
access. Confirm your installed agent's skill discovery rules.

For a Claude custom-skill upload, the companion `.skill` archive has `SKILL.md`
at its root. An upload makes instructions available; it does not guarantee a
speech engine, network permission, persistent output or shell execution.
On web/mobile or a sandbox, use Piper only if the environment can install and
run it and return the file. If those capabilities are absent, prepare the
script and explain how to render on a suitable host. Desktop bridges are
optional; no particular bridge or file-delivery tool is assumed.

## Privacy, cost and limits

Speech synthesis runs on the execution host after setup. This does **not** mean
the entire workflow is offline: an agent may already have sent your document
to its model provider. Review that provider and the host's storage policy
before giving it confidential text. A fully offline path uses local preparation
and a local model for any rewriting, or no rewriting at all. Dependency and
voice downloads contact public package/model hosts during setup, not during
this renderer's synthesis path. The package performs no publishing.

There is no hosted TTS character charge in these scripts. Agent subscriptions,
model inference, hardware and storage have their own costs. Longer documents
take longer; each Piper paragraph reloads the voice. The default timeout is
per subprocess, not a total job deadline. Available memory/disk, voice model
compatibility and execution-host restrictions determine practical limits.

The Markdown stripper is deliberately small, not a complete document parser.
It removes images, fenced code and link destinations; inspect its output and
disclose omissions in literal mode. Speech lint can flag ordinary uppercase
words and miss unfamiliar pronunciations. It does not prove semantic accuracy.
Strict lint failure leaves any previous prepared file intact, so only continue
after a successful preparation command. Voice quality and pronunciation still
need a listening check. No automatic fallback uploads text to another provider.

## Tests and review prompts

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

Tests use synthetic text, mocked speech processes and a real local FFmpeg
encoding check when available. They never download models or call paid APIs.
[evals/evals.json](evals/evals.json) contains prompts for later agent review;
they are not a measured triggering benchmark. This release has not had a real
Piper voice render or cross-platform listening evaluation.

## License and provenance

The scripts and documentation are MIT licensed; see [LICENSE](LICENSE).
The preparation script and two-mode workflow were adapted from an existing
MIT-licensed Audio Brief skill (v1.5.1); the portable renderer is new.
The copyright attribution is retained as required by that license.

Dependencies retain their own terms: current
[Piper](https://github.com/OHF-Voice/piper1-gpl) is GPL-3.0, FFmpeg builds have
their own LGPL/GPL conditions, and system voices are governed by the operating
system's terms. Voice models have separate model cards; the model repository's
general license is not enough to decide every voice's rights. For example,
[Alan's card](https://huggingface.co/rhasspy/piper-voices/blob/main/en/en_GB/alan/medium/MODEL_CARD)
refers to another dataset for its license, while
[Cori's card](https://huggingface.co/rhasspy/piper-voices/blob/main/en/en_GB/cori/high/MODEL_CARD)
describes a public-domain dataset. This package redistributes neither engine,
voice weights nor voice recordings. Review separate terms before bundling
dependencies or models, or publishing generated audio.
