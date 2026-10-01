import re
import unicodedata


def slugify(title: str) -> str:
    """Turn a title into a lowercase, hyphen-separated URL slug."""
    title = title.lower().replace("ß", "ss").replace("'", "").replace("’", "")
    title = unicodedata.normalize("NFKD", title)
    title = title.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", title).strip("-")
    if not slug:
        raise ValueError("title must contain at least one letter or digit")
    return slug
