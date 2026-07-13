from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

import che_file_to_knot_name  # noqa: E402
import hom_inter  # noqa: E402
import hybrid_indexer  # noqa: E402
import kho_inter  # noqa: E402
import spa_inter  # noqa: E402
from timer_process import run_subprocess_with_time_limit  # noqa: E402


TREFOIL = [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]
TRIANGLE_DATA = """LAMMPS data file

3 atoms
3 bonds

Atoms

1 0 0 0
2 1 0 0
3 0 1 0

Bonds

1 1 1 2
2 1 2 3
3 1 3 1
"""


class HybridIndexerTests(unittest.TestCase):
    def test_merge_is_strict_deduplicated_intersection(self):
        self.assertEqual(
            hybrid_indexer.merge_name_list(["K3a1", "K4a1", "K4a1"], ["K4a1", "K5a1"]),
            ["K4a1"],
        )
        self.assertEqual(hybrid_indexer.merge_name_list([], ["K3a1"]), [])

    def test_unique_and_empty_khovanov_results_short_circuit(self):
        for candidates in (["K3a1"], []):
            with (
                patch("hybrid_indexer.kho_inter.to_knotname", return_value=candidates),
                patch("hybrid_indexer.hom_inter.to_knotname") as homfly,
            ):
                self.assertEqual(hybrid_indexer.hybrid_indexer(TREFOIL), candidates)
            homfly.assert_not_called()

    def test_ambiguous_result_uses_homfly_intersection(self):
        with (
            patch("hybrid_indexer.kho_inter.to_knotname", return_value=["K3a1", "K5a1"]),
            patch("hybrid_indexer.hom_inter.to_knotname", return_value=["K3a1", "K4a1"]),
        ):
            self.assertEqual(hybrid_indexer.hybrid_indexer(TREFOIL), ["K3a1"])

    def test_interface_failures_are_not_silenced(self):
        failed = subprocess.CompletedProcess([], 2, "", "backend failed")
        with patch("kho_inter.subprocess.run", return_value=failed):
            with self.assertRaisesRegex(RuntimeError, "backend failed"):
                kho_inter.to_knotname(TREFOIL)
        with patch("hom_inter.subprocess.run", return_value=failed):
            with self.assertRaisesRegex(RuntimeError, "backend failed"):
                hom_inter.to_knotname(TREFOIL)

    def test_real_trefoil_khovanov_short_circuit(self):
        self.assertEqual(
            hybrid_indexer.hybrid_indexer(TREFOIL, khovanov_timeout=30, max_heap="1g"),
            ["K3a1"],
        )

    def test_real_spatial_and_molecular_unknot_paths(self):
        self.assertEqual(spa_inter.to_pdcode([[0, 0, 0], [1, 0, 0], [0, 1, 0]]), [])
        with TemporaryDirectory() as directory:
            path = Path(directory) / "triangle.data"
            path.write_text(TRIANGLE_DATA, encoding="utf-8")
            self.assertEqual(
                che_file_to_knot_name.che_file_to_knot_name(
                    str(path), projection_timeout=60, khovanov_timeout=60, max_heap="1g"
                ),
                ["K0a1"],
            )

    def test_timeout_runner(self):
        self.assertEqual(
            run_subprocess_with_time_limit([sys.executable, "-c", "raise SystemExit(3)"], 5),
            3,
        )

    def test_cli_missing_file(self):
        completed = subprocess.run(
            [sys.executable, str(SRC / "main.py"), "--che", "missing.data"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 2)
        self.assertIn("missing.data", completed.stderr)


if __name__ == "__main__":
    unittest.main()
