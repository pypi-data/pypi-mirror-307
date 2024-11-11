import unittest
import sys
from io import StringIO
from gptcmd.console import parse_args

class TestParseMethods(unittest.TestCase):
    def test_missing_prompt_argument(self):
        # Capture stdout and stderr to suppress argparse's output
        saved_stdout = sys.stdout
        saved_stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()

        # Test that parse_args raises SystemExit when required args are missing
        with self.assertRaises(SystemExit) as cm:
            parse_args()
        
        # Check that the exit code is 2 (commonly used for argument errors in argparse)
        self.assertEqual(cm.exception.code, 2)

        # Restore stdout and stderr
        sys.stdout = saved_stdout
        sys.stderr = saved_stderr
        
    def test_working_prompt_argument(self):
        sys.argv = ["console.py", "hello"]
        args = parse_args()
        self.assertEqual(args.prompt, "hello")

if __name__ == "__main__":
    unittest.main()
