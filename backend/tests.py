import tempfile
import json
from pathlib import Path
import pytest
from main import get_packages_json

# test_main.py



def test_get_packages_json_valid_package():
    with tempfile.TemporaryDirectory() as repo_dir:
        repo_path = Path(repo_dir)
        package_json = {"name": "test", "version": "1.0.0"}
        (repo_path / "package.json").write_text(json.dumps(package_json), encoding="utf-8")
        result = get_packages_json([str(repo_path)])
        assert result == [{"repo_path": str(repo_path), "package": package_json}]

def test_get_packages_json_missing_package():
    with tempfile.TemporaryDirectory() as repo_dir:
        repo_path = Path(repo_dir)
        result = get_packages_json([str(repo_path)])
        assert result == [{"repo_path": str(repo_path), "error": "package.json not found"}]

def test_get_packages_json_invalid_json():
    with tempfile.TemporaryDirectory() as repo_dir:
        repo_path = Path(repo_dir)
        (repo_path / "package.json").write_text("{invalid json}", encoding="utf-8")
        result = get_packages_json([str(repo_path)])
        assert result[0]["repo_path"] == str(repo_path)
        assert "error" in result[0]
        assert "Expecting property name enclosed in double quotes" in result[0]["error"]

def test_get_packages_json_multiple_repos():
    with tempfile.TemporaryDirectory() as repo1, tempfile.TemporaryDirectory() as repo2:
        repo_path1 = Path(repo1)
        repo_path2 = Path(repo2)
        package_json = {"name": "repo1", "version": "0.1.0"}
        (repo_path1 / "package.json").write_text(json.dumps(package_json), encoding="utf-8")
        # repo2 has no package.json
        result = get_packages_json([str(repo_path1), str(repo_path2)])
        assert result[0] == {"repo_path": str(repo_path1), "package": package_json}
        assert result[1] == {"repo_path": str(repo_path2), "error": "package.json not found"}