from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware  # type: ignore
from pathlib import Path
from pydantic import BaseModel
import json
from typing import List, Any, Dict

app = FastAPI() # type: ignore

# Permitir requisições do frontend local
app.add_middleware( # type: ignore
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RepoPaths(BaseModel):
    paths: List[str]

@app.post("/repo/packages") # type: ignore
async def get_packages_json(repo_paths: RepoPaths) -> List[Dict[str, Any]]:
    """Receives a list of repository paths, reads the package.json from each one, and returns their contents."""
    results: List[Dict[str, Any]] = []
    for repo_path in repo_paths.paths:
        package_file = Path(repo_path) / "package.json"
        if not package_file.exists():
            results.append({"repo_path": repo_path, "error": "package.json not found"})
            continue
        try:
            with open(package_file, encoding="utf-8") as f:
                data = json.load(f)
            results.append({"repo_path": repo_path, "package": data})
        except Exception as e:
            results.append({"repo_path": repo_path, "error": str(e)})
    return results
