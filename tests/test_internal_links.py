import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_all import validate_internal_links, validate_public_text


class RepositoryTextTests(unittest.TestCase):
    def test_internal_links(self):
        validate_internal_links(ROOT)

    def test_public_text(self):
        validate_public_text(ROOT)


if __name__ == "__main__":
    unittest.main()
