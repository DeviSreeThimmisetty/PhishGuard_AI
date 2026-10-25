import ipaddress
import re
from urllib.parse import urlparse


SUSPICIOUS_KEYWORDS = [
    "login",
    "verify",
    "update",
    "secure",
    "account",
    "password",
    "signin",
    "banking",
    "confirm",
    "wallet",
    "suspend",
    "authenticate",
]


def extract_features(url):
    """Extract numerical features from a URL for phishing detection."""

    url = str(url).strip()

    # Add a default scheme when the URL has no scheme.
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", url):
        url = "http://" + url

    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    path = parsed.path or ""
    query = parsed.query or ""

    # Check whether the hostname is an IP address.
    try:
        ipaddress.ip_address(hostname)
        has_ip_address = 1
    except ValueError:
        has_ip_address = 0

    # Count subdomain labels using a simple hostname heuristic.
    hostname_parts = hostname.split(".") if hostname else []
    subdomain_count = max(0, len(hostname_parts) - 2)

    # Count suspicious keywords.
    url_lower = url.lower()
    suspicious_keyword_count = sum(
        keyword in url_lower for keyword in SUSPICIOUS_KEYWORDS
    )

    # Count path levels.
    path_depth = len([part for part in path.split("/") if part])

    # Check whether the URL specifies a port.
    try:
        port = parsed.port
        has_nonstandard_port = int(port is not None and port not in (80, 443))
    except ValueError:
        has_nonstandard_port = 1

    # Count query parameters.
    query_parameter_count = len(
        [part for part in query.split("&") if part]
    )

    # Return features in a consistent dictionary.
    features = {
        "url_length": len(url),
        "hostname_length": len(hostname),
        "path_length": len(path),
        "query_length": len(query),
        "digit_count": sum(character.isdigit() for character in url),
        "letter_count": sum(character.isalpha() for character in url),
        "https": int(parsed.scheme.lower() == "https"),
        "has_ip_address": has_ip_address,
        "subdomain_count": subdomain_count,
        "suspicious_keyword_count": suspicious_keyword_count,
        "path_depth": path_depth,
        "has_nonstandard_port": has_nonstandard_port,
        "double_slash_in_path": int("//" in path),
        "percent_count": url.count("%"),
        "at_symbol_count": url.count("@"),
        "hyphen_count": url.count("-"),
        "dot_count": url.count("."),
        "query_parameter_count": query_parameter_count,
        "has_fragment": int(bool(parsed.fragment)),
        "equals_count": url.count("="),
    }

    return features