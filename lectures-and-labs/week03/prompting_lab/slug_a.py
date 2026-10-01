import re
import unicodedata


def slugify(title: str) -> str:
    """Turn a blog post title into a lowercase, URL-safe slug."""
    normalized = unicodedata.normalize("NFKD", title)
    ascii_title = normalized.encode("ascii", "ignore").decode("ascii")
    words = re.sub(r"[^a-z0-9]+", "-", ascii_title.lower())
    return words.strip("-")
