from pprint import pformat

from markupsafe import Markup, escape

from plain.http import Response
from plain.views.exceptions import ResponseException


def dd(obj):
    """
    Dump and die.

    Dump the object and raise a ResponseException with the dump as the response content.
    """
    dump_str = pformat(obj)

    print(f"Dumping object:\n{dump_str}")

    response = Response()
    response.status_code = 500
    response.content = (
        Markup("<pre><code>") + escape(dump_str) + Markup("</code></pre>")
    )
    response.content_type = "text/html"
    raise ResponseException(response)
