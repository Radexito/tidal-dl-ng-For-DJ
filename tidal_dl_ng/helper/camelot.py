"""Helper module for Camelot wheel conversions.

The Camelot wheel is the standard harmonic-mixing map used by DJ software
(Mixed In Key, Serato, Rekordbox, Traktor). Every musical key maps to a
Camelot wheel position, and the two spellings in this module are:

- Camelot code (wheel position): 8B, 6A, 11A   (1-12 + A minor / B major)
- Musical-key notation:           C, Am, F#m   (letter spelling of the key)

Conversions are bidirectional; this module only converts between the two
spellings, it never detects keys.
"""

from enum import StrEnum


class KeyScale(StrEnum):
    """Musical key scale types."""

    MAJOR = "MAJOR"
    MINOR = "MINOR"


class CamelotFormat(StrEnum):
    """Camelot wheel output formats."""

    MUSICAL = "musical"  # musical-key notation: C, Am, F#m, Gb
    CAMELOT = "camelot"  # Camelot wheel codes: 8B, 6A, 11A


# Mapping: (key, scale) -> Camelot code
_KEY_TO_CAMELOT: dict[tuple[str, KeyScale], str] = {
    # Minor keys (A)
    ("Ab", KeyScale.MINOR): "1A",
    ("Eb", KeyScale.MINOR): "2A",
    ("Bb", KeyScale.MINOR): "3A",
    ("F", KeyScale.MINOR): "4A",
    ("C", KeyScale.MINOR): "5A",
    ("G", KeyScale.MINOR): "6A",
    ("D", KeyScale.MINOR): "7A",
    ("A", KeyScale.MINOR): "8A",
    ("E", KeyScale.MINOR): "9A",
    ("B", KeyScale.MINOR): "10A",
    ("FSharp", KeyScale.MINOR): "11A",
    ("Db", KeyScale.MINOR): "12A",
    # Major keys (B)
    ("B", KeyScale.MAJOR): "1B",
    ("FSharp", KeyScale.MAJOR): "2B",
    ("Db", KeyScale.MAJOR): "3B",
    ("Ab", KeyScale.MAJOR): "4B",
    ("Eb", KeyScale.MAJOR): "5B",
    ("Bb", KeyScale.MAJOR): "6B",
    ("F", KeyScale.MAJOR): "7B",
    ("C", KeyScale.MAJOR): "8B",
    ("G", KeyScale.MAJOR): "9B",
    ("D", KeyScale.MAJOR): "10B",
    ("A", KeyScale.MAJOR): "11B",
    ("E", KeyScale.MAJOR): "12B",
}

# Reverse mapping: Camelot code -> (key, scale)
_CAMELOT_TO_KEY: dict[str, tuple[str, KeyScale]] = {v: k for k, v in _KEY_TO_CAMELOT.items()}

# Musical-key notation display mapping
_KEY_TO_MUSICAL: dict[tuple[str, KeyScale], str] = {
    # Minor keys
    ("Ab", KeyScale.MINOR): "Abm",
    ("Eb", KeyScale.MINOR): "Ebm",
    ("Bb", KeyScale.MINOR): "Bbm",
    ("F", KeyScale.MINOR): "Fm",
    ("C", KeyScale.MINOR): "Cm",
    ("G", KeyScale.MINOR): "Gm",
    ("D", KeyScale.MINOR): "Dm",
    ("A", KeyScale.MINOR): "Am",
    ("E", KeyScale.MINOR): "Em",
    ("B", KeyScale.MINOR): "Bm",
    ("FSharp", KeyScale.MINOR): "F#m",
    ("Db", KeyScale.MINOR): "Dbm",
    # Major keys
    ("B", KeyScale.MAJOR): "B",
    ("FSharp", KeyScale.MAJOR): "Gb",
    ("Db", KeyScale.MAJOR): "Db",
    ("Ab", KeyScale.MAJOR): "Ab",
    ("Eb", KeyScale.MAJOR): "Eb",
    ("Bb", KeyScale.MAJOR): "Bb",
    ("F", KeyScale.MAJOR): "F",
    ("C", KeyScale.MAJOR): "C",
    ("G", KeyScale.MAJOR): "G",
    ("D", KeyScale.MAJOR): "D",
    ("A", KeyScale.MAJOR): "A",
    ("E", KeyScale.MAJOR): "E",
}

# Reverse mapping: musical-key notation -> (key, scale)
_MUSICAL_TO_KEY: dict[str, tuple[str, KeyScale]] = {v: k for k, v in _KEY_TO_MUSICAL.items()}


def key_to_camelot(key: str, key_scale: KeyScale | str) -> str | None:
    """Convert key and scale to Camelot code.

    Args:
        key (str): Musical key (e.g., 'C', 'Eb', 'FSharp').
        key_scale (KeyScale | str): Scale type ('MAJOR' or 'MINOR').

    Returns:
        str | None: Camelot code (e.g., "8B", "6A", "11A") or None if invalid.

    Example:
        >>> key_to_camelot("C", KeyScale.MAJOR)
        '8B'
        >>> key_to_camelot("G", "MINOR")
        '6A'
        >>> key_to_camelot("FSharp", KeyScale.MAJOR)
        '2B'
    """
    # Normalize key_scale to enum
    if isinstance(key_scale, str):
        try:
            key_scale = KeyScale(key_scale.upper())
        except ValueError:
            return None

    # Normalize key input
    normalized_key = _normalize_key_input(key)

    return _KEY_TO_CAMELOT.get((normalized_key, key_scale))


def key_to_musical(key: str, key_scale: KeyScale | str) -> str | None:
    """Convert key and scale to musical-key notation.

    Args:
        key (str): Musical key (e.g., 'C', 'Eb', 'FSharp').
        key_scale (KeyScale | str): Scale type ('MAJOR' or 'MINOR').

    Returns:
        str | None: Musical-key notation (e.g., "C", "Gm", "Gb") or None if invalid.

    Example:
        >>> key_to_musical("C", KeyScale.MAJOR)
        'C'
        >>> key_to_musical("G", "MINOR")
        'Gm'
        >>> key_to_musical("FSharp", KeyScale.MINOR)
        'F#m'
    """
    # Normalize key_scale to enum
    if isinstance(key_scale, str):
        try:
            key_scale = KeyScale(key_scale.upper())
        except ValueError:
            return None

    # Normalize key input (handle variations)
    normalized_key = _normalize_key_input(key)

    return _KEY_TO_MUSICAL.get((normalized_key, key_scale))


def musical_to_key(musical: str) -> tuple[str, KeyScale] | None:
    """Convert musical-key notation to key and scale.

    Args:
        musical (str): Musical-key notation (e.g., "C", "Gm", "F#m").

    Returns:
        tuple[str, KeyScale] | None: Tuple of (key, scale) or None if invalid.

    Example:
        >>> musical_to_key("C")
        ('C', <KeyScale.MAJOR: 'MAJOR'>)
        >>> musical_to_key("Gm")
        ('G', <KeyScale.MINOR: 'MINOR'>)
    """
    # Normalize input to handle case variations
    musical_normalized = musical.strip()

    # Try direct lookup first
    if result := _MUSICAL_TO_KEY.get(musical_normalized):
        return result

    # Try with different casing (e.g., "gm" -> "Gm")
    if len(musical_normalized) >= 2:
        # Try capitalizing first letter
        musical_normalized = musical_normalized[0].upper() + musical_normalized[1:]
        return _MUSICAL_TO_KEY.get(musical_normalized)

    return None


def camelot_to_key(camelot: str) -> tuple[str, KeyScale] | None:
    """Convert Camelot code to key and scale.

    Args:
        camelot (str): Camelot code (e.g., "8B", "6A", "11A").

    Returns:
        tuple[str, KeyScale] | None: Tuple of (key, scale) or None if invalid.

    Example:
        >>> camelot_to_key("8B")
        ('C', <KeyScale.MAJOR: 'MAJOR'>)
        >>> camelot_to_key("6A")
        ('G', <KeyScale.MINOR: 'MINOR'>)
        >>> camelot_to_key("11A")
        ('FSharp', <KeyScale.MINOR: 'MINOR'>)
    """
    return _CAMELOT_TO_KEY.get(camelot.upper())


def musical_to_camelot(musical: str) -> str | None:
    """Convert musical-key notation to Camelot code.

    Args:
        musical (str): Musical-key notation (e.g., "C", "Gm", "F#m").

    Returns:
        str | None: Camelot code (e.g., "8B", "6A") or None if invalid.

    Example:
        >>> musical_to_camelot("C")
        '8B'
        >>> musical_to_camelot("Gm")
        '6A'
    """
    key_scale_tuple = musical_to_key(musical)
    if not key_scale_tuple:
        return None

    key, scale = key_scale_tuple
    return key_to_camelot(key, scale)


def camelot_to_musical(camelot: str) -> str | None:
    """Convert Camelot code to musical-key notation.

    Args:
        camelot (str): Camelot code (e.g., "8B", "6A").

    Returns:
        str | None: Musical-key notation (e.g., "C", "Gm") or None if invalid.

    Example:
        >>> camelot_to_musical("8B")
        'C'
        >>> camelot_to_musical("6A")
        'Gm'
    """
    key_scale_tuple = camelot_to_key(camelot)
    if not key_scale_tuple:
        return None

    key, scale = key_scale_tuple
    return key_to_musical(key, scale)


def format_initial_key(key: str, key_scale: str, initial_key_format: CamelotFormat | str) -> str:
    """Format musical key according to specified notation system.

    Converts a musical key and scale into the requested Camelot notation format.
    Returns empty string if key or scale is UNKNOWN, or if conversion fails.

    Args:
        key (str): Musical key (e.g., 'C', 'Eb', 'FSharp') or 'UNKNOWN'.
        key_scale (str): Scale type ('MAJOR', 'MINOR') or 'UNKNOWN'.
        initial_key_format (CamelotFormat | str): Desired output format
            ('musical' or 'camelot').

    Returns:
        str: Formatted key string or empty string if invalid/unknown.

    Example:
        >>> format_initial_key("C", "MAJOR", CamelotFormat.MUSICAL)
        'C'
        >>> format_initial_key("C", "MAJOR", "camelot")
        '8B'
        >>> format_initial_key("UNKNOWN", "MAJOR", CamelotFormat.MUSICAL)
        ''
        >>> format_initial_key("C", "UNKNOWN", CamelotFormat.MUSICAL)
        ''
    """
    # Early return for UNKNOWN values
    if not key or not key_scale or key == "UNKNOWN" or key_scale == "UNKNOWN":
        return ""

    # Normalize format parameter to enum
    if isinstance(initial_key_format, str):
        try:
            initial_key_format = CamelotFormat(initial_key_format.lower())
        except ValueError:
            return ""

    # Convert to requested format
    result: str | None = None

    if initial_key_format == CamelotFormat.MUSICAL:
        result = key_to_musical(key, key_scale)
    elif initial_key_format == CamelotFormat.CAMELOT:
        result = key_to_camelot(key, key_scale)

    # Return formatted string or empty string if conversion failed
    return result if result is not None else ""


def is_valid_key(key: str, key_scale: KeyScale | str) -> bool:
    """Check if key and scale combination is valid.

    Args:
        key (str): Musical key to validate.
        key_scale (KeyScale | str): Scale type.

    Returns:
        bool: True if valid key/scale combination.

    Example:
        >>> is_valid_key("C", KeyScale.MAJOR)
        True
        >>> is_valid_key("H", KeyScale.MINOR)
        False
    """
    if isinstance(key_scale, str):
        try:
            key_scale = KeyScale(key_scale.upper())
        except ValueError:
            return False

    normalized_key = _normalize_key_input(key)
    return (normalized_key, key_scale) in _KEY_TO_CAMELOT


def is_valid_musical(musical: str) -> bool:
    """Check if a string is valid musical-key notation.

    Args:
        musical (str): String to validate.

    Returns:
        bool: True if valid musical-key notation (e.g., "C", "Gm", "F#m").

    Example:
        >>> is_valid_musical("C")
        True
        >>> is_valid_musical("Gm")
        True
        >>> is_valid_musical("H")
        False
    """
    return musical_to_key(musical) is not None


def is_valid_camelot(camelot: str) -> bool:
    """Check if a string is valid Camelot code.

    Args:
        camelot (str): String to validate.

    Returns:
        bool: True if valid Camelot code (1A-12A, 1B-12B).

    Example:
        >>> is_valid_camelot("8B")
        True
        >>> is_valid_camelot("6A")
        True
        >>> is_valid_camelot("13A")
        False
    """
    return camelot.upper() in _CAMELOT_TO_KEY


def _normalize_key_input(key: str) -> str:
    """Normalize key input variations to standard format.

    Handles variations like 'F#', 'Gb', 'f sharp', etc.

    Args:
        key (str): Key input string.

    Returns:
        str: Normalized key (e.g., 'C', 'Eb', 'FSharp').
    """
    # Remove spaces and convert to title case
    key_clean = key.replace(" ", "").replace("sharp", "Sharp").replace("#", "Sharp")

    # Handle flat notation
    if "b" in key_clean and "Sharp" not in key_clean:
        # Already in flat format (e.g., 'Eb', 'Ab')
        return key_clean

    # Map sharp keys to their enharmonic flat equivalents where needed
    sharp_to_flat: dict[str, str] = {
        "CSharp": "Db",
        "DSharp": "Eb",
        "GSharp": "Ab",
        "ASharp": "Bb",
        # FSharp stays as is (it's used in the mapping)
    }

    return sharp_to_flat.get(key_clean, key_clean)
