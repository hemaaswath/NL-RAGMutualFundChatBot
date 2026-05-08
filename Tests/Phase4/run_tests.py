"""
Phase 4 Test Runner
Runs all Frontend UI tests
"""

import pytest
import sys
from pathlib import Path
from contextlib import redirect_stdout, redirect_stderr

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "Docs" / "src"))


def main():
    """Run all Phase 4 tests."""
    test_dir = Path(__file__).parent
    output_file = test_dir / "test_results.txt"
    
    print("=" * 80)
    print("Phase 4 Frontend UI Tests")
    print("=" * 80)
    print(f"Output will be saved to: {output_file}")
    print()
    
    with open(output_file, 'w', encoding='utf-8') as f:
        with redirect_stdout(f), redirect_stderr(f):
            exit_code = pytest.main([
                str(test_dir),
                "-v",
                "--tb=short",
                "--color=no"
            ])
    
    print()
    print("=" * 80)
    if exit_code == 0:
        print("✅ All Phase 4 tests passed!")
    else:
        print("❌ Some Phase 4 tests failed")
    print(f"📄 Results saved to: {output_file}")
    print("=" * 80)
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
