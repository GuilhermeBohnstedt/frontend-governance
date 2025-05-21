from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json
from typing import List

app: FastAPI = FastAPI()

# Permitir requisições do frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/repo/packages")
def get_packages_json(repo_paths: List[str]):
    """Recebe uma lista de caminhos de repositórios, lê o package.json de cada um e retorna seus conteúdos."""
    results = []
    for repo_path in repo_paths:
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
