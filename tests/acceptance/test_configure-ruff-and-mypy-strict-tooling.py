import subprocess
import sys
from pathlib import Path

import pytest

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


@pytest.fixture(scope="module")
def pyproject_data():
    project_root = Path(__file__).parent.parent.parent
    pyproject_path = project_root / "pyproject.toml"
    if not pyproject_path.exists():
        pytest.fail("pyproject.toml not found in project root")
    with open(pyproject_path, "rb") as f:
        return tomllib.load(f)


def get_project_root():
    return Path(__file__).parent.parent.parent


def test_ruff_listed_as_dev_dependency(pyproject_data):
    """Acceptance Criterion 1: ruff is listed as a dev dependency in pyproject.toml"""
    dependencies = []
    if "tool" in pyproject_data and "poetry" in pyproject_data["tool"]:
        dev_deps = pyproject_data["tool"]["poetry"].get("group", {}).get("dev", {}).get("dependencies", {})
        dependencies.extend(dev_deps.keys())
    if "project" in pyproject_data:
        optional_deps = pyproject_data["project"].get("optional-dependencies", {})
        for group in optional_deps.values():
            dependencies.extend(group)
        if "dependency-groups" in pyproject_data:
            for group in pyproject_data["dependency-groups"].values():
                dependencies.extend(group)

    assert any(dep.startswith("ruff") for dep in dependencies), "ruff not found in dev dependencies"


def test_mypy_listed_as_dev_dependency(pyproject_data):
    """Acceptance Criterion 2: mypy is listed as a dev dependency in pyproject.toml"""
    dependencies = []
    if "tool" in pyproject_data and "poetry" in pyproject_data["tool"]:
        dev_deps = pyproject_data["tool"]["poetry"].get("group", {}).get("dev", {}).get("dependencies", {})
        dependencies.extend(dev_deps.keys())
    if "project" in pyproject_data:
        optional_deps = pyproject_data["project"].get("optional-dependencies", {})
        for group in optional_deps.values():
            dependencies.extend(group)
        if "dependency-groups" in pyproject_data:
            for group in pyproject_data["dependency-groups"].values():
                dependencies.extend(group)

    assert any(dep.startswith("mypy") for dep in dependencies), "mypy not found in dev dependencies"


def test_mypy_configured_for_strict_mode(pyproject_data):
    """Acceptance Criterion 3: mypy is configured for strict mode in pyproject.toml"""
    mypy_config = pyproject_data.get("tool", {}).get("mypy", {})
    
    strict_enabled = mypy_config.get("strict", False)
    # Alternatively, it could be enabled via command line in scripts, but usually it's in the config
    # Or as an array: strict = true
    
    assert strict_enabled is True, "mypy strict mode not enabled in pyproject.toml under [tool.mypy]"


def test_ruff_check_runs_without_config_errors(tmp_path):
    """Acceptance Criterion 4: `ruff check src/` runs without configuration errors"""
    project_root = get_project_root()
    src_dir = project_root / "src"
    
    if not src_dir.exists():
        src_dir.mkdir()

    result = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "src/"],
        cwd=project_root,
        capture_output=True,
        text=True
    )
    
    # Check that it doesn't fail specifically due to configuration errors
    config_error_indicators = ["invalid configuration", "ConfigError", "option", "unknown setting"]
    stderr_lower = result.stderr.lower()
    
    for indicator in config_error_indicators:
        assert indicator not in stderr_lower, f"Ruff configuration error detected: {result.stderr}"
        
    # Return code can be 0 (no errors) or 1 (linting errors found), but not 2 (config error usually)
    assert result.returncode in [0, 1], f"Ruff failed to run properly: {result.stdout}\n{result.stderr}"


def test_mypy_src_runs_without_config_errors(tmp_path):
    """Acceptance Criterion 5: `mypy src/` runs without configuration errors"""
    project_root = get_project_root()
    src_dir = project_root / "src"
    
    if not src_dir.exists():
        src_dir.mkdir()

    result = subprocess.run(
        [sys.executable, "-m", "mypy", "src/"],
        cwd=project_root,
        capture_output=True,
        text=True
    )
    
    config_error_indicators = ["config error", "unrecognized", "invalid"]
    stderr_lower = result.stderr.lower()
    stdout_lower = result.stdout.lower()
    
    for indicator in config_error_indicators:
        assert indicator not in stderr_lower, f"Mypy configuration error detected in stderr: {result.stderr}"
        # Mypy sometimes outputs config errors to stdout
        assert "config error" not in stdout_lower, f"Mypy configuration error detected in stdout: {result.stdout}"
        
    # Return code 0 is success, 1 is type errors found. Either is fine as long as config is valid.
    assert result.returncode in [0, 1], f"Mypy failed to run properly: {result.stdout}\n{result.stderr}"