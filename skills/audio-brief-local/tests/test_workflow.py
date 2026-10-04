import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import wave

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


prepare = load('prepare_text')
render = load('render_local')


class PreparationTests(unittest.TestCase):
    def test_plain_divider_does_not_discard_content(self):
        text = 'Keep this sentence.\n---\nAnd this sentence.'
        self.assertEqual(prepare.split_header(text), text)
        self.assertIn('Keep this sentence.', prepare.strip_markdown(text))

    def test_explicit_header_only(self):
        text = '<!-- audio-brief: non-spoken header -->\nNotes\n---\nSpeak this.'
        self.assertEqual(prepare.split_header(text), 'Speak this.')
        with self.assertRaises(ValueError):
            prepare.split_header('<!-- audio-brief: non-spoken header -->\nNotes')

    def test_strict_does_not_replace_existing_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            source = work / 'source.md'; source.write_text('Cost: $12.\n')
            output = work / 'spoken.txt'; output.write_text('previous\n')
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/prepare_text.py'),
                                     str(source), '-o', str(output), '--strict'],
                                    capture_output=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(output.read_text(), 'previous\n')
            self.assertEqual(source.read_text(), 'Cost: $12.\n')

    def test_synthetic_examples_pass_and_source_unchanged(self):
        for source in (ROOT / 'examples').glob('*.md'):
            before = source.read_bytes()
            body = prepare.strip_markdown(prepare.split_header(source.read_text()))
            self.assertTrue(body)
            self.assertFalse(prepare.lint(body))
            self.assertEqual(source.read_bytes(), before)

    def test_symbols_and_initialisms_gate(self):
        for text in ['£one', 'fifty%', 'A&B', '12', 'ABC', 'a | b', 'https://example.org']:
            self.assertTrue(prepare.lint(text), text)


class RendererTests(unittest.TestCase):
    def invoke(self, source, out, extra=()):
        with patch.object(sys, 'argv', ['render', '-i', str(source), '-o', str(out), *extra]):
            render.main()

    def test_existing_output_protected_before_tool_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'text.txt'; source.write_text('Hello.')
            out = Path(tmp) / 'out.m4a'; out.write_bytes(b'previous')
            with patch.object(render, 'run') as runner, patch('sys.stderr', io.StringIO()):
                with self.assertRaises(SystemExit):
                    self.invoke(source, out)
                runner.assert_not_called()
            self.assertEqual(out.read_bytes(), b'previous')

    def test_timeout_keeps_old_audio_and_cleans_temporary_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            source = work / 'text.txt'; source.write_text('Hello.')
            out = work / 'out.m4a'; out.write_bytes(b'previous')
            with patch.object(render.shutil, 'which', return_value='/mock/tool'), \
                 patch.object(render, 'run', side_effect=subprocess.TimeoutExpired('say', .1)):
                with self.assertRaises(subprocess.TimeoutExpired):
                    self.invoke(source, out, ['--engine', 'say', '--overwrite'])
            self.assertEqual(out.read_bytes(), b'previous')
            self.assertEqual(set(p.name for p in work.iterdir()), {'text.txt', 'out.m4a'})

    def test_missing_local_model_does_not_run_or_download(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'text.txt'; source.write_text('Hello.')
            with patch.object(render.shutil, 'which', return_value='/mock/tool'), \
                 patch.object(render, 'run') as runner, patch('sys.stderr', io.StringIO()):
                with self.assertRaises(SystemExit):
                    self.invoke(source, Path(tmp) / 'out.m4a', ['--model', str(Path(tmp) / 'missing.onnx')])
                runner.assert_not_called()

    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'local FFmpeg required')
    def test_piper_chunk_join_real_encoding_without_synthesis(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            source = work / 'text.txt'; source.write_text('First paragraph.\n\nSecond paragraph.')
            model = work / 'voice.onnx'; model.write_bytes(b'synthetic placeholder')
            Path(str(model) + '.json').write_text('{}')
            out = work / 'audio.m4a'
            actual_run = render.run
            calls = []
            def fake_speech(argv, timeout, text=None):
                if argv[:3] == [sys.executable, '-m', 'piper']:
                    calls.append(text)
                    # Silence is synthesized by the test, never a voice recording.
                    with wave.open(argv[argv.index('-f') + 1], 'wb') as wav:
                        wav.setnchannels(1); wav.setsampwidth(2); wav.setframerate(24000)
                        wav.writeframes(bytes(4800))
                else:
                    actual_run(argv, timeout, text)
            with patch.object(render.importlib.util, 'find_spec', return_value=object()), \
                 patch.object(render, 'run', side_effect=fake_speech), patch('sys.stdout', io.StringIO()) as stdout:
                self.invoke(source, out, ['--model', str(model), '--title', 'Synthetic "title"'])
                receipt = json.loads(stdout.getvalue())
            self.assertEqual(calls, ['First paragraph.', 'Second paragraph.'])
            self.assertGreater(out.stat().st_size, 0)
            self.assertAlmostEqual(receipt['duration_seconds'], .65, delta=.1)
            self.assertFalse(list(work.glob('audio-brief-*')))


if __name__ == '__main__':
    unittest.main()
