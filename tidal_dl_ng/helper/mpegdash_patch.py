"""
Monkey-patch for mpegdash to handle non-integer AdaptationSet id/group attributes.

TIDAL recently started returning MPD manifests with string values like "main"
for the AdaptationSet `id` and `group` attributes, which mpegdash expects to be integers.
This causes a ValueError: invalid literal for int() with base 10: 'main'

This patch modifies the parse_attr_value function to gracefully handle
non-integer values for attributes that are expected to be integers.
"""

import logging

logger = logging.getLogger(__name__)

_patched = False


def _safe_int(value: str) -> int | None:
    """Safely convert a value to int, returning None if conversion fails."""
    try:
        return int(value)
    except (ValueError, TypeError):
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
        import re

        # Store the original function
        original_parse_attr_value = mpegdash_utils.parse_attr_value

        def patched_parse_attr_value(xmlnode, attr_name, value_type):
            """
            Patched version of parse_attr_value that handles non-integer values gracefully.
            """
            if attr_name not in xmlnode.attributes.keys():
                return None

            attr_val = xmlnode.attributes[attr_name].nodeValue

            if isinstance(value_type, list):
                attr_type = value_type[0] if len(value_type) > 0 else str
                try:
                    return [attr_type(elem) for elem in re.split(r"[, ]", attr_val)]
                except (ValueError, TypeError):
                    # If conversion fails, return as strings
                    return [str(elem) for elem in re.split(r"[, ]", attr_val)]

            # Handle integer conversion failures gracefully
            if value_type == int:
                result = _safe_int(attr_val)
                if result is None:
                    logger.debug(
                        f"mpegdash: Could not convert '{attr_name}'='{attr_val}' to int, using None"
                    )
                return result

            try:
                return value_type(attr_val)
            except (ValueError, TypeError):
                logger.debug(
                    f"mpegdash: Could not convert '{attr_name}'='{attr_val}' to {value_type.__name__}, using None"
                )
                return None

        # Apply the patch
        mpegdash_utils.parse_attr_value = patched_parse_attr_value
        _patched = True
        logger.debug("mpegdash patch applied successfully")

    except ImportError:
        logger.warning("Could not import mpegdash, patch not applied")
    except Exception as e:
        logger.warning(f"Failed to apply mpegdash patch: {e}")
