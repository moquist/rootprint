"""Exact compact task/label accounting; source and PNG transport remain inline."""

import json
import os
import unittest
from unittest.mock import MagicMock, patch

import independent_review as reviewer
from test_independent_review import Repository, answer, png, source_text


class CompactTransport(unittest.TestCase):
    def test_exact_utf8_transport_and_budget_include_every_image_label(self):
        repo = Repository()
        text = 'café ☃\r\n  "quoted" \\ end\n'
        repo.head_files.update({"exact.txt": text, "café.png": png()})
        task = reviewer.context(repo, reviewer.metadata(repo, repo, 9))
        self.assertEqual(source_text(task, "head_files", "exact.txt"), text)
        response = {"status": "completed", "output": [
            {"type": "message", "role": "assistant", "status": "completed", "content": [
                {"type": "output_text", "text": json.dumps(answer())}]}]}
        transport = MagicMock()
        transport.__enter__.return_value.read.return_value = json.dumps(response).encode()
        with patch.dict(os.environ, {"OPENAI_API_KEY": "fake"}, clear=True), \
                patch("independent_review.urlopen", return_value=transport) as network:
            reviewer.ask_model(task)
        raw = network.call_args.args[0].data
        payload = json.loads(raw)
        self.assertEqual(raw, reviewer.compact(payload).encode())
        content = payload["input"][0]["content"]
        self.assertEqual(content, reviewer.model_content(task))
        self.assertEqual(json.loads(content[0]["text"])["pr"], task["pr"])
        self.assertIn("café", content[0]["text"])
        size = sum(len(c["text"].encode()) for c in content if c["type"] == "input_text")
        self.assertGreater(size, len(content[0]["text"].encode()))
        with patch.object(reviewer, "MAX_CONTEXT", size):
            reviewer.context(repo, reviewer.metadata(repo, repo, 9))
        with patch.object(reviewer, "MAX_CONTEXT", size - 1), \
                patch.dict(os.environ, {"OPENAI_API_KEY": "fake"}, clear=True), patch("independent_review.urlopen") as network:
            with self.assertRaises(ValueError):
                reviewer.context(repo, reviewer.metadata(repo, repo, 9))
            with self.assertRaises(ValueError):
                reviewer.ask_model(task)
        network.assert_not_called()


if __name__ == "__main__":
    unittest.main()
