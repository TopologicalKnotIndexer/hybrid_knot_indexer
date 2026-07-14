from contextlib import redirect_stdout
import io
import os
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

import test_all  # noqa: E402


RUN_FULL_INTEGRATION = os.environ.get("TKI_RUN_FULL_INTEGRATION") == "1"
SAGE_EXECUTABLE = os.environ.get("TKI_SAGE_EXECUTABLE")
JAVA_EXECUTABLE = os.environ.get("TKI_JAVA_EXECUTABLE")
JAVA_MAX_HEAP = os.environ.get("TKI_JAVA_MAX_HEAP", "1g")


@unittest.skipUnless(
    RUN_FULL_INTEGRATION and SAGE_EXECUTABLE,
    "set TKI_RUN_FULL_INTEGRATION=1 and TKI_SAGE_EXECUTABLE for the 22-sample regression",
)
class FullHybridIntegrationTests(unittest.TestCase):
    def test_all_molecular_samples_with_real_backends(self):
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = test_all.main(
                java_path=JAVA_EXECUTABLE,
                sage_path=SAGE_EXECUTABLE,
                projection_timeout=180,
                khovanov_timeout=180,
                homfly_timeout=300,
                max_heap=JAVA_MAX_HEAP,
            )
        detail = output.getvalue()
        self.assertEqual(exit_code, 0, detail)
        self.assertIn("checked 22 samples; failures=0", detail)


if __name__ == "__main__":
    unittest.main()
