#!/usr/bin/env python3
"""Render prepared text locally. No installs, downloads, uploads or shell eval."""
import argparse
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import wave


def run(argv, timeout, text=None):
    subprocess.run(argv, input=text, text=True, check=True, timeout=timeout,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('-i', '--input', type=Path, required=True)
    p.add_argument('-o', '--output', type=Path, required=True)
    p.add_argument('--engine', choices=['piper', 'say'], default='piper')
    p.add_argument('--model', type=Path, help='local Piper .onnx, with adjacent .onnx.json')
    p.add_argument('--voice', help='exact installed macOS voice name; unset uses system default')
    p.add_argument('--length-scale', type=float, default=1.02)
    p.add_argument('--timeout', type=float, default=300, help='seconds per subprocess')
    p.add_argument('--title', default='')
    p.add_argument('--overwrite', action='store_true')
    a = p.parse_args()
    if not math.isfinite(a.timeout) or a.timeout <= 0 or not math.isfinite(a.length_scale) or a.length_scale <= 0:
        p.error('timeout and length scale must be finite and positive')
    if a.output.suffix.lower() != '.m4a':
        p.error('output must end in .m4a')
    if a.output.exists() and not a.overwrite:
        p.error('output exists; choose another path or explicitly use --overwrite')
    # Resolve filenames so leading dashes cannot become tool options.
    a.output = a.output.resolve()
    body = a.input.read_text(encoding='utf-8').strip()
    if not body:
        p.error('input is empty')
    for tool in ['ffmpeg', 'ffprobe']:
        if not shutil.which(tool):
            p.error(f'{tool} is missing; install it separately')
    if a.engine == 'say':
        if not shutil.which('say'):
            p.error('macOS say is unavailable on this execution host')
    else:
        if a.model is None:
            p.error('--model is required; voice downloads are a separate setup step')
        a.model = a.model.resolve()
        if not a.model.is_file() or not Path(str(a.model) + '.json').is_file():
            p.error('model and adjacent .onnx.json must exist locally')
        if importlib.util.find_spec('piper') is None:
            p.error('Piper is missing in this Python environment; install it separately')
    # Put the temporary output on the destination filesystem for atomic replacement.
    with tempfile.TemporaryDirectory(prefix='audio-brief-', dir=a.output.parent) as tmp:
        work = Path(tmp)
        if a.engine == 'say':
            spoken = work / 'spoken.txt'
            spoken.write_text(body + '\n', encoding='utf-8')
            audio = work / 'speech.aiff'
            cmd = ['say', '-f', str(spoken), '-o', str(audio)]
            if a.voice:
                cmd += ['-v', a.voice]
            run(cmd, a.timeout)
        else:
            parts = []
            for i, para in enumerate(re.split(r'\n\s*\n', body)):
                wav = work / f'p{i:05d}.wav'
                run([sys.executable, '-m', 'piper', '--model', str(a.model),
                     '--length-scale', str(a.length_scale), '-f', str(wav)], a.timeout, para)
                parts.append(wav)
            audio = work / 'speech.wav'
            with wave.open(str(audio), 'wb') as out:
                params = None
                for i, wav in enumerate(parts):
                    with wave.open(str(wav), 'rb') as inp:
                        current = (inp.getnchannels(), inp.getsampwidth(), inp.getframerate())
                        if params is None:
                            params = current
                            out.setnchannels(params[0]); out.setsampwidth(params[1]); out.setframerate(params[2])
                        elif current != params:
                            raise ValueError('Piper chunks have inconsistent audio formats')
                        if i:
                            silence = 128 if params[1] == 1 else 0
                            out.writeframes(bytes([silence]) * round(params[2] * .45) * params[0] * params[1])
                        out.writeframes(inp.readframes(inp.getnframes()))
        target = work / 'result.m4a'
        cmd = ['ffmpeg', '-v', 'error', '-i', str(audio), '-c:a', 'aac', '-b:a', '96k']
        if a.title:
            cmd += ['-metadata', f'title={a.title}']
        run(cmd + [str(target)], a.timeout)
        probe = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                '-of', 'csv=p=0', str(target)], check=True, capture_output=True,
                               text=True, timeout=a.timeout)
        duration = float(probe.stdout.strip())
        if not math.isfinite(duration) or duration <= 0 or not target.stat().st_size:
            raise ValueError('rendered output has no positive duration')
        if a.overwrite:
            os.replace(target, a.output)
        else:
            # Exclusive publication also protects against another process creating it meanwhile.
            os.link(target, a.output)
        print(json.dumps({'output': str(a.output), 'engine': a.engine,
                          'duration_seconds': round(duration, 2), 'bytes': a.output.stat().st_size}))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        # Keep potentially confidential input/tool output out of error logs.
        print(f'render failed ({type(exc).__name__}); destination was not replaced', file=sys.stderr)
        sys.exit(1)
