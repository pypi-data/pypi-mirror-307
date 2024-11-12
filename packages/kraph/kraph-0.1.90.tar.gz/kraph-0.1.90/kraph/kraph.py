from koil.composition import Composition
from pydantic import Field

from kraph.rath import KraphRath


class Kraph(Composition):
    rath: KraphRath = Field(default_factory=KraphRath)

    def _repr_html_inline_(self):
        return f"""<p>Kraph </p>"""
