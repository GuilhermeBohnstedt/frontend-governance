import tempfile
import json
from pathlib import Path
from main import get_packages_json, RepoPaths
import pytest

# backend/test_main.py
@pytest.mark.asyncio  # type: ignore
async def test_get_packages_json_valid_package() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)
        package_json = {"name": "testpkg", "version": "1.0.0"}
        (repo_path / "package.json").write_text(json.dumps(package_json), encoding="utf-8")
        repopaths = RepoPaths(paths=[str(repo_path)])
        result = await get_packages_json(repopaths)
        assert len(result) == 1
        assert result[0]["repo_path"] == str(repo_path)
        assert result[0]["package"] == package_json

@pytest.mark.asyncio  # type: ignore
async def test_get_packages_json_missing_package() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)
        repopaths = RepoPaths(paths=[str(repo_path)])
        result = await get_packages_json(repopaths)
        assert len(result) == 1
        assert result[0]["repo_path"] == str(repo_path)
        assert "error" in result[0]
        assert result[0]["error"] == "package.json not found"

@pytest.mark.asyncio  # type: ignore
async def test_get_packages_json_invalid_json() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)
        (repo_path / "package.json").write_text("{ invalid json }", encoding="utf-8")
        repopaths = RepoPaths(paths=[str(repo_path)])
        result = await get_packages_json(repopaths)
        assert len(result) == 1
        assert result[0]["repo_path"] == str(repo_path)
        assert "error" in result[0]
        assert "Expecting property name" in result[0]["error"]

@pytest.mark.asyncio  # type: ignore
async def test_get_packages_json_multiple_repos() -> None:
    with tempfile.TemporaryDirectory() as tmpdir1, tempfile.TemporaryDirectory() as tmpdir2:
        repo1 = Path(tmpdir1)
        repo2 = Path(tmpdir2)
        (repo1 / "package.json").write_text(json.dumps({"name": "repo1"}), encoding="utf-8")
        # repo2 has no package.json
        repopaths = RepoPaths(paths=[str(repo1), str(repo2)])
        result = await get_packages_json(repopaths)
        assert len(result) == 2
        # Find by repo_path
        res1 = next(r for r in result if r["repo_path"] == str(repo1))
        res2 = next(r for r in result if r["repo_path"] == str(repo2))
        assert res1["package"] == {"name": "repo1"}
        assert "error" in res2 and res2["error"] == "package.json not found"