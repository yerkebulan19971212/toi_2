"""
Jinja2-based rendering engine for invitation HTML templates.

Security:
- SandboxedEnvironment blocks __import__, OS access, attribute traversal tricks.
- autoescape=True escapes all {{ }} output — prevents XSS from user-supplied strings.
- Templates are authored only by staff; user data flows in only as context variables.
"""

from pathlib import Path

from jinja2 import FileSystemLoader, select_autoescape
from jinja2.sandbox import SandboxedEnvironment

TEMPLATES_DIR = Path(__file__).parent / 'templates_html'

_env = SandboxedEnvironment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(['html']),
    trim_blocks=True,
    lstrip_blocks=True,
)


def render_invitation(template_file: str, context: dict) -> str:
    """
    Render a Jinja2 HTML template file with the given context dict.
    template_file is the filename without .html extension (e.g. 'classic-wedding').
    Returns the rendered HTML string.
    Raises jinja2.TemplateSyntaxError if the template is malformed.
    """
    tmpl = _env.get_template(f'{template_file}.html')
    return tmpl.render(**context)
