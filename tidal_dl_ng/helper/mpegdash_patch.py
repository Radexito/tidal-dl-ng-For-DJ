"""
Monkey-patch for mpegdash to handle non-integer AdaptationSet id/group attributes.

TIDAL recently started returning MPD manifests with string values like "main"
for the AdaptationSet `id` and `group` attributes, which mpegdash expects to be integers.
This causes a ValueError: invalid literal for int() with base 10: 'main'

This patch modifies the parse_attr_value function to gracefully handle
non-integer values for attributes that are expected to be integers.
"""

import logging
import re

logger = logging.getLogger(__name__)

_patched = False


def _safe_int(value: str) -> int | None:
    """Safely convert a value to int, returning None if conversion fails."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def _convert_list(attr_val: str, value_type) -> list[str]:
    attr_type = value_type[0] if value_type else str
    try:
        return [attr_type(elem) for elem in re.split(r"[, ]", attr_val)]
    except (ValueError, TypeError):
        return [str(elem) for elem in re.split(r"[, ]", attr_val)]


def _convert_single(attr_name: str, attr_val: str, value_type):
    if value_type == int:
        result = _safe_int(attr_val)
        if result is None:
            logger.debug(
                "mpegdash: Could not convert '%s'='%s' to int, using None",
                attr_name,
                attr_val,
            )
        return result
    try:
        return value_type(attr_val)
    except (ValueError, TypeError):
        logger.debug(
            "mpegdash: Could not convert '%s'='%s' to %s, using None",
            attr_name,
            attr_val,
            value_type.__name__,
        )
        return None


def apply_mpegdash_patch() -> None:
    """
    Apply a monkey-patch to mpegdash to handle string values in integer fields.

    This patches the parse_attr_value function in mpegdash.utils to gracefully
    handle non-integer values (like "main") for attributes expected to be integers.
    """
    global _patched

    if _patched:
        return

    try:
        from mpegdash import utils as mpegdash_utils

        def patched_parse_attr_value(xmlnode, attr_name, value_type):
            if attr_name not in xmlnode.attributes:
                return None

            attr_val = xmlnode.attributes[attr_name].nodeValue

            if isinstance(value_type, list):
                return _convert_list(attr_val, value_type)

            return _convert_single(attr_name, attr_val, value_type)

        mpegdash_utils.parse_attr_value = patched_parse_attr_value
        _patched = True
        logger.debug("mpegdash patch applied successfully")

    except ImportError:
        logger.warning("Could not import mpegdash, patch not applied")
    except Exception as e:
        logger.warning("Failed to apply mpegdash patch: %s", e)
