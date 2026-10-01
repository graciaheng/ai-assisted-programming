import re
import unicodedata


def slugify(title: str) -> str:
    """Turn a blog post title into a lowercase, URL-safe slug."""
    normalized = unicodedata.normalize("NFKD", title.casefold())
    ascii_title = normalized.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", ascii_title).strip("-")
