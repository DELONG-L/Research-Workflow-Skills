import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_all import validate_eval_file


class EvaluationCorpusTests(unittest.TestCase):
    def test_all_evaluation_files(self):
        paths = sorted(ROOT.glob("**/evals/*.json"))
        self.assertEqual(len(paths), 3)
        for path in paths:
            with self.subTest(path=path):
                validate_eval_file(path)


if __name__ == "__main__":
    unittest.main()
