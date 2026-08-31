import sys
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_all import ValidationError, extract_front_matter, validate_workspace_contract


class ContractTemplateTests(unittest.TestCase):
    def fixture(self, name):
        return ROOT / "tests" / "fixtures" / name

    def test_local_only_contract(self):
        data = extract_front_matter(self.fixture("managed-local-only/PROJECT-WORKSPACE.md"))
        validate_workspace_contract(data)
        self.assertIsNone(data["paper"])
        self.assertIsNone(data["hpc"])
        self.assertIsNone(data["sync"])

    def test_paper_extension(self):
        data = extract_front_matter(self.fixture("managed-with-paper/PROJECT-WORKSPACE.md"))
        validate_workspace_contract(data)
        self.assertEqual(data["paper"]["repository"], "paper")

    def test_hpc_extension(self):
        data = extract_front_matter(self.fixture("managed-with-hpc/PROJECT-WORKSPACE.md"))
        validate_workspace_contract(data)
        self.assertIn(".git/", data["sync"]["upload_exclude"])
        self.assertIn("paper/", data["sync"]["upload_exclude"])

    def test_malformed_contract_is_rejected(self):
        data = extract_front_matter(self.fixture("malformed-contract/PROJECT-WORKSPACE.md"))
        with self.assertRaises(ValidationError):
            validate_workspace_contract(data)

    def test_paper_link_is_explicit(self):
        path = self.fixture("nested-paper-repository/.research-workspace.yml")
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        self.assertEqual(data["workspace_kind"], "research-paper")
        self.assertEqual(data["parent_contract"], "../PROJECT-WORKSPACE.md")


if __name__ == "__main__":
    unittest.main()
