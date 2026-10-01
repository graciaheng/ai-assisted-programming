import re
import unicodedata


def slugify(title: str) -> str:
    """Convert a blog post title into a lowercase, URL-safe slug."""
    normalized = unicodedata.normalize("NFKD", title)
    ascii_title = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_title.lower())
    return slug.strip("-")
