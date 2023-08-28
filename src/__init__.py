# Copyright 2023 iiPython

# Modules
from pathlib import Path

from blacksheep import Application
from blacksheep.server.responses import forbidden, not_found
from blacksheep.server.templating import use_templates
from jinja2 import FileSystemLoader

# Initialization
template_path = Path(__file__).parent / "templates"

app = Application()
view = use_templates(
    app,
    loader = FileSystemLoader(template_path),
    enable_async = True
)

# Handle page routing
@app.route("/", methods = ["GET"])
async def route_index() -> None:
    return await view("index", {})

@app.route("/{path:path}", methods = ["GET"])
async def route_page(path: str) -> None:
    fp = template_path / (path + ".html")
    if not fp.is_relative_to(template_path):
        return forbidden(f"forbidden: {path}")

    elif not fp.is_file():
        return not_found(f"not found: {path}")

    return await view(path, {})
