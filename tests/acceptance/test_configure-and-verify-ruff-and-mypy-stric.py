"""Acceptance tests for configuring and verifying ruff and mypy --strict compliance.

These tests validate that:
1. ruff check src/ produces no errors
2. mypy --strict src/ produces no errors
3. All four functions in src/ pass mypy --strict type checking
4. Configuration for ruff and mypy is present in pyproject.toml or dedicated config files
"""

import re
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"


def run_command(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    """Run a command and return the completed process."""
    return subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )


def test_ruff_check_src_produces_no_errors() -> None:
    """Acceptance criterion 1: ruff check src/ produces no errors."""
    result = run_command([sys.executable, "-m", "ruff", "check", "src/"])
    assert result.returncode == 0, (
        f"ruff check src/ failed with exit code {result.returncode}.\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


def test_mypy_strict_src_produces_no_errors() -> None:
    """Acceptance criterion 2: mypy --strict src/ produces no errors."""
    result = run_command([sys.executable, "-m", "mypy", "--strict", "src/"])
    assert result.returncode == 0, (
        f"mypy --strict src/ failed with exit code {result.returncode}.\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


def _find_public_functions(src_dir: Path) -> list[str]:
    """Find all non-dunder function definitions in Python files under src/."""
    functions: list[str] = []
    for py_file in src_dir.rglob("*.py"):
        content = py_file.read_text()
        matches = re.findall(
            r"^\s*(?:async\s+)?def\s+(\w+)\s*\(", content, re.MULTILINE
        )
        for func_name in matches:
            if not func_name.startswith("__"):
                functions.append(func_name)
    return functions


def test_all_four_functions_pass_mypy_strict() -> None:
    """Acceptance criterion 3: All four functions pass mypy --strict type checking."""
    functions = _find_public_functions(SRC_DIR)

    assert len(functions) == 4, (
        f"Expected exactly 4 public functions in src/, but found "
        f"{len(functions)}: {functions}"
    )

    result = run_command([sys.executable, "-m", "mypy", "--strict", "src/"])
    assert result.returncode == 0, (
        f"mypy --strict src/ failed with exit code {result.returncode}.\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


def test_ruff_configuration_present() -> None:
    """Acceptance criterion 4a: Ruff configuration exists in pyproject.toml or a dedicated file."""
    pyproject = PROJECT_ROOT / "pyproject.toml"
    dedicated_files = [
        PROJECT_ROOT / "ruff.toml",
        PROJECT_ROOT / ".ruff.toml",
    ]

    if pyproject.exists():
        content = pyproject.read_text()
        if "[tool.ruff" in content:
            return

    for config_file in dedicated_files:
        if config_file.exists():
            return

    pytest.fail(
        "No ruff configuration found. Expected [tool.ruff] in pyproject.toml, "
        "or a ruff.toml / .ruff.toml file in the project root."
    )


def test_mypy_configuration_present() -> None:
    """Acceptance criterion 4b: Mypy configuration exists in pyproject.toml or a dedicated file."""
    pyproject = PROJECT_ROOT / "pyproject.toml"

    if pyproject.exists():
        content = pyproject.read_text()
        if "[tool.mypy" in content:
            return

    mypy_ini = PROJECT_ROOT / "mypy.ini"
    if mypy_ini.exists():
        return

    dot_mypy_ini = PROJECT_ROOT / ".mypy.ini"
    if dot_mypy_ini.exists():
        return

    setup_cfg = PROJECT_ROOT / "setup.cfg"
    if setup_cfg.exists():
        content = setup_cfg.read_text()
        if "[mypy]" in content:
            return

    pytest.fail(
        "No mypy configuration found. Expected [tool.mypy] in pyproject.toml, "
        "or a mypy.ini / .mypy.ini file, or a [mypy] section in setup.cfg."
    )