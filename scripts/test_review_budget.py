"""Exercise the actual hosted entrypoint with fake orchestration and no credentials."""

import os
import runpy
import unittest
from unittest.mock import patch

import independent_review as reviewer
from test_independent_review import Repository


class HostedBudget(unittest.TestCase):
    def test_entrypoint_accepts_more_text_but_preserves_boundaries(self):
        self.assertEqual(reviewer.MAX_CONTEXT, 600000)

        def exercise():
            self.assertEqual(reviewer.MAX_CONTEXT, 1200000)
            repo = Repository()
            repo.head_files.update({f"{n}.txt": chr(65 + n) * reviewer.MAX_FILE for n in range(9)})
            task = reviewer.context(repo, reviewer.metadata(repo, repo, 9))
            self.assertGreater(len(reviewer.model_content(task)[0]["text"].encode()), 600000)
            repo.head_files["too-large.txt"] = "x" * (reviewer.MAX_FILE + 1)
            with self.assertRaises(ValueError):
                reviewer.context(repo, reviewer.metadata(repo, repo, 9))
            repo = Repository()
            repo.pr["body"] = "m" * 650000
            reviewer.context(repo, reviewer.metadata(repo, repo, 9))
            boundary = {"source": ""}
            boundary["source"] = "x" * (reviewer.MAX_CONTEXT - len(reviewer.compact(boundary).encode()))
            self.assertEqual(len(reviewer.model_content(boundary)[0]["text"].encode()), 1200000)
            boundary["source"] += "x"
            with patch("independent_review.urlopen") as network, self.assertRaises(ValueError):
                reviewer.ask_model(boundary)
            network.assert_not_called()

        with patch.dict(os.environ, {"OPENAI_API_KEY": "fake"}, clear=True), \
                patch.object(reviewer, "MAX_CONTEXT", 600000), patch.object(reviewer, "main", side_effect=exercise) as main:
            runpy.run_path(str(reviewer.ROOT / "scripts/hosted_independent_review.py"), run_name="__main__")
        main.assert_called_once_with()
        self.assertEqual(reviewer.MAX_CONTEXT, 600000)


if __name__ == "__main__":
    unittest.main()
