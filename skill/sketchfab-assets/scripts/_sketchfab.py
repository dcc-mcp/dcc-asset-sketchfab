from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


BASE = "https://api.sketchfab.com/v3"
LICENSE_NOTICE = {
    "provider": "Sketchfab",
    "usage_notice": "Preserve model license, author attribution, and source link with downloaded assets.",
    "api_guidelines": "https://sketchfab.com/developers/download-api/guidelines",
}


def _headers(auth: bool = False) -> dict[str, str]:
    headers = {"User-Agent": "dcc-mcp-sketchfab/0.1"}
    token = os.environ.get("SKETCHFAB_TOKEN")
    if auth:
        if not token:
            raise RuntimeError("Set SKETCHFAB_TOKEN to a Sketchfab OAuth access token before downloading")
        headers["Authorization"] = f"Bearer {token}"
    elif token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def api(path: str, params: dict[str, Any] | None = None, auth: bool = False) -> Any:
    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v not in (None, "")})
    req = urllib.request.Request(url, headers=_headers(auth))
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def compact_model(model: dict[str, Any]) -> dict[str, Any]:
    user = model.get("user") or {}
    license_info = model.get("license") or {}
    archives = model.get("archives") or {}
    return {
        "uid": model.get("uid"),
        "name": model.get("name"),
        "viewer_url": model.get("viewerUrl"),
        "is_downloadable": model.get("isDownloadable"),
        "license": license_info,
        "author": {
            "username": user.get("username"),
            "display_name": user.get("displayName"),
            "profile_url": user.get("profileUrl"),
        },
        "archives": sorted(archives.keys()) if isinstance(archives, dict) else [],
    }


def search(query: str | None = None, license: str | None = None, limit: int = 10) -> list[dict[str, Any]]:
    params = {
        "type": "models",
        "downloadable": "true",
        "archives_flavours": "true",
        "q": query,
        "licenses": license,
    }
    data = api("/search", params)
    return [compact_model(item) for item in data.get("results", [])[:limit]]


def model(uid: str) -> dict[str, Any]:
    return api(f"/models/{uid}", {"archives_flavours": "true"})


def download(uid: str, output_dir: str, format: str = "gltf") -> dict[str, Any]:
    fmt = format.lower()
    if fmt not in {"gltf", "glb", "usdz"}:
        raise ValueError("format must be one of: gltf, glb, usdz")
    links = api(f"/models/{uid}/download", auth=True)
    entry = links.get(fmt)
    if not entry or not entry.get("url"):
        raise RuntimeError(f"Sketchfab did not return a {fmt} download URL for {uid}")
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    target = Path(output_dir) / f"{uid}-{fmt}.zip"
    req = urllib.request.Request(entry["url"], headers={"User-Agent": "dcc-mcp-sketchfab/0.1"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        target.write_bytes(resp.read())
    meta = compact_model(model(uid))
    return {"file": str(target), "format": fmt, "model": meta, **LICENSE_NOTICE}
