"""BACore documentation with FastHTML.

# App:
- `live`: Start the app with `live=True`, to reload the webpage in the browser on any code change.

# Resources:
- FastHTML uses [Pico CSS](https://picocss.com).
"""

from bacore.interfaces.fasthtml.common import (
    Documentation,
    MarkdownFT,
    NavDocs,
    doc_page,
    flexboxgrid,
)
from fasthtml.common import (
    A,
    Div,
    FastHTML,
    HighlightJS,
    Li,
    MarkdownJS,
    Nav,
    Titled,
    Ul,
    picolink,
    serve,
)
from pathlib import Path

tests_docs = Documentation(path=Path("tests"), package_root="tests")

headers = (
    flexboxgrid,
    HighlightJS(langs=["python", "html", "css"]),
    MarkdownJS(),
    picolink,
)
app = FastHTML(hdrs=headers, htmx=True, live=True)


class NavTop:
    """Top and main navigation."""

    def __ft__(self):
        return Nav(
            Ul(Li(A("Home", href="/"))),
            Ul(
                Li(A("Documentation", href="/docs")),
                Li(A("Github", href="https://github.com/bacoredev/bacore/")),
                Li(A("PyPi", href="https://pypi.org/project/bacore/")),
            ),
        )


@app.get("/")
def home():
    """The homepage for BACore."""
    return Titled(
        "BACore",
        NavTop(),
        MarkdownFT(path=Path("README.md"), skip_title=True),
        Div("Welcome to BACore website."),
    )


@app.get("/docs/{path:path}")
def docs(path: str):
    """Documentation pages."""
    return Titled(
        "Documentation",
        NavTop(),
        Div(
            NavDocs(path=Path("python/bacore"), package_root="bacore"),
            Div(
                doc_page(
                    doc_source=Documentation(path=Path("python/bacore"), package_root="bacore"),
                    url=path,
                ),
                cls="col-xs-10",
            ),
            cls="row",
        ),
    )


@app.route("/tests/{path:path}", methods="get")
def tests(path: str):
    """Test case pages."""
    return doc_page(doc_source=tests_docs, url=path)


serve(port=7001)
