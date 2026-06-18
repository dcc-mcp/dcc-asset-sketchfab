from __future__ import annotations

from typing import Any

from dcc_mcp_core.skill import skill_entry, skill_exception, skill_success

from _sketchfab import download


@skill_entry
def main(uid: str, output_dir: str, format: str = "gltf", **_: Any) -> dict[str, Any]:
    try:
        result = download(uid, output_dir, format)
        return skill_success("Sketchfab model downloaded", **result)
    except Exception as exc:
        return skill_exception(exc, message="Failed to download Sketchfab model")


if __name__ == "__main__":
    from dcc_mcp_core.skill import run_main

    run_main(main)
