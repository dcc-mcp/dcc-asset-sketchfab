from __future__ import annotations

from typing import Any

from dcc_mcp_core.skill import skill_entry, skill_exception, skill_success

from _sketchfab import LICENSE_NOTICE, compact_model, model


@skill_entry
def main(uid: str, **_: Any) -> dict[str, Any]:
    try:
        data = model(uid)
        return skill_success("Sketchfab model loaded", model=compact_model(data), raw=data, license=LICENSE_NOTICE)
    except Exception as exc:
        return skill_exception(exc, message="Failed to load Sketchfab model")


if __name__ == "__main__":
    from dcc_mcp_core.skill import run_main

    run_main(main)
