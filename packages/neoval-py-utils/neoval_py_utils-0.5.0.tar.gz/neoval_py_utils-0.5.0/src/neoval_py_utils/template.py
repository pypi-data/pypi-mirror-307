"""Template class for rendering SQL for existing In Process databases."""

from typing import Iterable, Union, Optional
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape, TemplateNotFound
from jinja2.environment import Template


class Template:
    """A singleton class for rendering SQL templates.

    Example usage:
        template_path = Path.cwd() / "templates"
        template = Template(template_path)
        query = template.get("example.sql").render()
    """

    def __new__(cls, *args) -> None:  # noqa: ANN002
        if not hasattr(cls, "instance"):
            cls.instance = super(Template, cls).__new__(cls)  # noqa: UP008
        return cls.instance

    def __init__(self, templates_path: str | Path) -> None:
        """Initialize the class with a jinja environment."""
        if not hasattr(self, "env"):
            templates_path = Path(templates_path)

            self.env = Environment(
                loader=FileSystemLoader(templates_path),
                autoescape=select_autoescape(
                    disabled_extensions=("sql"),
                    default_for_string=False,
                    default=False,
                ),
                trim_blocks=True,
                lstrip_blocks=True,
                enable_async=True,
            )

            self.env.tests["populated"] = self._populated
            self.env.filters["listify"] = self._listify

    def get(self, name: str, db: Optional[str] = None) -> Template:
        """A method to retrieve the `Template`.

        If no database is passed, it will look for the named template in both
        subfolders. Returns a jinja `Template` object that can then be rendered.
        """
        if not db:
            try:
                for template in [f"duckdb/{name}", f"sqlite/{name}", name]:
                    return self.env.get_template(template)
            except TemplateNotFound as exc:
                raise ValueError(f"`{name}` does not exist.") from exc

        elif db not in ("duckdb", "sqlite"):
            raise ValueError(f"`{db}` is not a valid database value.")

        else:
            try:
                return self.env.get_template(f"{db}/{name}")
            except TemplateNotFound:
                try:
                    return self.env.get_template(name)
                except TemplateNotFound as exc:
                    raise ValueError(
                        f"`{name}` does not exist in `{db}` templates."
                    ) from exc

    @staticmethod
    def _populated(value: Union[Iterable, float, int, str]) -> bool:
        """A custom test.

        This is a custom test - it's designed to be used in conjunction with
        `listify` (or the like), which is below.

        ```sql
        {% if values is populated %}
        ```

        Will evaluate to `True` where:
        - `values` is a primitive value, or
        - `values` is an iterable with at least one item in it.
        """
        if isinstance(value, (float, int, str)):
            return True

        if isinstance(value, Iterable):
            return len(value) > 0

        return False

    @staticmethod
    def _listify(value: Union[Iterable, float, int, str]) -> str:
        """A custom filter to generate lists of strings.

        This is a custom filter used to generate lists of strings for use in, for
        instance, an `IN (...)` clause. It can be called from Jinja2 using something
        like:

        ```sql
        # values = ["a", "b", "c"]
        AND value IN ({{ values|listify }})

        # Results in `AND value IN ("a", "b", "c")`
        ```

        Importantly, this filter should only be used where the inputs are intended
        to be serialized as strings (and so surrounded by quotes) - it's equivalent
        to (but less verbose that) calling something like
        `{{ values|map('tojson')|join(', ') }} }}`.

        If you need an equivalent list that is not quoted, you can just called
        `{{ values|join(', ') }}`
        """
        if not isinstance(value, (str, Iterable)):
            value = [value]

        return ", ".join([f'"{v}"' for v in value])
