"""Validate email addresses using a small set of common-syntax rules."""


def is_valid_email(address: str) -> bool:
    """Return whether *address* has a plausible common email format."""
    if not isinstance(address, str) or len(address) > 254:
        return False
    if any(character.isspace() for character in address):
        return False

    local, separator, domain = address.partition("@")
    if not separator or not local or not domain or "@" in domain:
        return False
    if "." not in domain or domain.startswith(".") or domain.endswith("."):
        return False
    if ".." in domain:
        return False

    return True
