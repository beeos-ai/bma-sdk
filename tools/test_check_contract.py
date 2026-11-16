import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import check_contract


class ContractLockTests(unittest.TestCase):
    def test_active_snapshot_matches_its_lock(self):
        self.assertEqual(self.check_snapshot(b"active snapshot\n"), [])

    def test_changed_active_snapshot_is_rejected(self):
        failures = self.check_snapshot(b"changed snapshot\n")
        self.assertEqual(len(failures), 1)
        self.assertIn("contracts/bma/v3/extensions.openapi.yaml sha256", failures[0])

    def check_snapshot(self, content):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            contracts = root / "contracts/bma"
            (contracts / "v3").mkdir(parents=True)
            (contracts / "rest.openapi.yaml").write_bytes(b"frozen snapshot\n")
            (contracts / "v3/extensions.openapi.yaml").write_bytes(content)
            source = {"source_repository": "example/source", "source_commit": "a" * 40}
            frozen = {**source, "rest": {
                "contract": "contracts/bma/rest.openapi.yaml",
                "sha256": hashlib.sha256(b"frozen snapshot\n").hexdigest(),
            }}
            active = {**source, "contract": "contracts/bma/v3/extensions.openapi.yaml",
                      "sha256": hashlib.sha256(b"active snapshot\n").hexdigest()}
            (contracts / "v3/lock.json").write_text(json.dumps(active))
            report = check_contract.Report()
            with patch.object(check_contract, "ROOT", root), patch.object(check_contract, "CONTRACTS", contracts):
                check_contract.check_lock(report, frozen)
            return report.failures


if __name__ == "__main__":
    unittest.main()
