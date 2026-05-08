"""
Phase 5 Test Runner
Runs all Testing & Quality Assurance tests
"""

import pytest
import sys
from pathlib import Path
from contextlib import redirect_stdout, redirect_stderr

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "Docs" / "src"))


def main():
    """Run all Phase 5 tests."""
    test_dir = Path(__file__).parent
    
    # Setup output file
    output_file = Path(__file__).parent / "test_results.txt"
    
    print("=" * 80)
    print("Phase 5: Testing & Quality Assurance")
    print("=" * 80)
    print(f"Output will be saved to: {output_file}")
    print()
    
    # Run pytest with output to file
    with open(output_file, 'w', encoding='utf-8') as f:
        with redirect_stdout(f), redirect_stderr(f):
            exit_code = pytest.main([
                str(test_dir),
                "-v",
                "--tb=short",
                "--color=no",
                "--ignore=" + str(test_dir / "__pycache__"),
                f"--junitxml={str(test_dir / 'junit_report.xml')}"
            ])
    
    print()
    print("=" * 80)
    if exit_code == 0:
        print("✅ All Phase 5 tests passed!")
    else:
        print("❌ Some Phase 5 tests failed")
    print(f"📄 Results saved to: {output_file}")
    print("=" * 80)
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
