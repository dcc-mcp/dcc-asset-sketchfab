# DCC-MCP Sketchfab Assets

Sketchfab free/downloadable model search and download tools for DCC-MCP.

This skill uses Sketchfab's official Data and Download APIs. It does not import
files into a DCC scene.

## Install

```bash
dcc-mcp-cli marketplace add dcc-mcp/dcc-asset-sketchfab
dcc-mcp-cli marketplace install dcc-asset-sketchfab
```

## Requirements

- Search uses the public API.
- Download requires a Sketchfab OAuth access token in `SKETCHFAB_TOKEN`.

## Tools

- `search_sketchfab_models`
- `get_sketchfab_model`
- `download_sketchfab_model`

## License Notes

This wrapper is MIT licensed. Sketchfab model licenses vary. Downloaded models
must keep their Creative Commons license, author attribution, and source link
where required by Sketchfab's API guidelines.
