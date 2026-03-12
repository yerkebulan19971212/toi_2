"""
Jinja2-based rendering engine for invitation HTML templates.

Security:
- SandboxedEnvironment blocks __import__, OS access, attribute traversal tricks.
- autoescape=True escapes all {{ }} output — prevents XSS from user-supplied strings.
- Templates are authored only by staff; user data flows in only as context variables.
"""

from jinja2.sandbox import SandboxedEnvironment
from jinja2 import BaseLoader, select_autoescape

_env = SandboxedEnvironment(
    loader=BaseLoader(),
    autoescape=select_autoescape(['html', 'xml']),
    trim_blocks=True,
    lstrip_blocks=True,
)


def render_invitation(html_template: str, context: dict) -> str:
    """
    Render a Jinja2 HTML template string with the given context dict.
    Returns the rendered HTML string.
    Raises jinja2.TemplateSyntaxError if the template is malformed.
    """
    tmpl = _env.from_string(html_template)
    return tmpl.render(**context)
