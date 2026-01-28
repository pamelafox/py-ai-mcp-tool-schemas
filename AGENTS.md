# Instructions for coding agents

## Markdown files

Always check for markdownlint issues and resolve them.

## Updating Python dependencies

When updating or adding Python dependencies:

1. Edit `pyproject.toml` with the new or updated version constraints.
2. Run `uv lock` to re-resolve dependencies (use `uv lock -P <package>` to upgrade only a specific package).
3. Run `uv sync` to install the updated lockfile into the virtual environment.
