"""Tests for Camelot wheel notation conversions."""

from tidal_dl_ng.helper.camelot import (
    CamelotFormat,
    KeyScale,
    camelot_to_musical,
    camelot_to_key,
    musical_to_camelot,
    musical_to_key,
    format_initial_key,
    is_valid_camelot,
    is_valid_musical,
    is_valid_key,
    key_to_camelot,
    key_to_musical,
)


class TestKeyToCamelot:
    """Test key_to_camelot function."""

    def test_major_keys(self):
        """Test conversion of major keys to Camelot code."""
        assert key_to_camelot("C", KeyScale.MAJOR) == "8B"
        assert key_to_camelot("E", KeyScale.MAJOR) == "12B"
        assert key_to_camelot("G", KeyScale.MAJOR) == "9B"

    def test_minor_keys(self):
        """Test conversion of minor keys to Camelot code."""
        assert key_to_camelot("G", KeyScale.MINOR) == "6A"
        assert key_to_camelot("A", KeyScale.MINOR) == "8A"
        assert key_to_camelot("D", KeyScale.MINOR) == "7A"

    def test_flat_keys(self):
        """Test conversion of flat keys to Camelot code."""
        assert key_to_camelot("Eb", KeyScale.MINOR) == "2A"
        assert key_to_camelot("Ab", KeyScale.MAJOR) == "4B"
        assert key_to_camelot("Bb", KeyScale.MAJOR) == "6B"

    def test_sharp_keys(self):
        """Test conversion of sharp keys (FSharp) to Camelot code."""
        assert key_to_camelot("FSharp", KeyScale.MAJOR) == "2B"
        assert key_to_camelot("FSharp", KeyScale.MINOR) == "11A"

    def test_string_scale_parameter(self):
        """Test that string scale parameters work."""
        assert key_to_camelot("C", "MAJOR") == "8B"
        assert key_to_camelot("G", "MINOR") == "6A"

    def test_invalid_key(self):
        """Test that invalid keys return None."""
        assert key_to_camelot("H", KeyScale.MAJOR) is None
        assert key_to_camelot("X", KeyScale.MINOR) is None

    def test_invalid_scale(self):
        """Test that invalid scale strings return None."""
        assert key_to_camelot("C", "INVALID") is None


class TestKeyToMusical:
    """Test key_to_musical function."""

    def test_major_keys(self):
        """Test conversion of major keys to musical-key notation."""
        assert key_to_musical("C", KeyScale.MAJOR) == "C"
        assert key_to_musical("E", KeyScale.MAJOR) == "E"
        assert key_to_musical("G", KeyScale.MAJOR) == "G"

    def test_minor_keys(self):
        """Test conversion of minor keys to musical-key notation."""
        assert key_to_musical("G", KeyScale.MINOR) == "Gm"
        assert key_to_musical("A", KeyScale.MINOR) == "Am"
        assert key_to_musical("Db", KeyScale.MINOR) == "Dbm"

    def test_flat_keys(self):
        """Test conversion of flat keys to musical-key notation."""
        assert key_to_musical("Eb", KeyScale.MINOR) == "Ebm"
        assert key_to_musical("Ab", KeyScale.MAJOR) == "Ab"

    def test_sharp_keys(self):
        """Test conversion of sharp keys to musical-key notation."""
        assert key_to_musical("FSharp", KeyScale.MINOR) == "F#m"
        assert key_to_musical("FSharp", KeyScale.MAJOR) == "Gb"

    def test_string_scale_parameter(self):
        """Test that string scale parameters work."""
        assert key_to_musical("C", "MAJOR") == "C"
        assert key_to_musical("G", "MINOR") == "Gm"

    def test_invalid_key(self):
        """Test that invalid keys return None."""
        assert key_to_musical("H", KeyScale.MAJOR) is None


class TestMusicalToKey:
    """Test musical_to_key function."""

    def test_major_keys(self):
        """Test conversion of musical-key notation to major keys."""
        result = musical_to_key("C")
        assert result is not None
        key, scale = result
        assert key == "C"
        assert scale == KeyScale.MAJOR

        result = musical_to_key("E")
        assert result is not None
        key, scale = result
        assert key == "E"
        assert scale == KeyScale.MAJOR

    def test_minor_keys(self):
        """Test conversion of musical-key notation to minor keys."""
        result = musical_to_key("Gm")
        assert result is not None
        key, scale = result
        assert key == "G"
        assert scale == KeyScale.MINOR

        result = musical_to_key("Am")
        assert result is not None
        key, scale = result
        assert key == "A"
        assert scale == KeyScale.MINOR

    def test_case_insensitive(self):
        """Test that musical-key notation is case-insensitive."""
        result = musical_to_key("gm")
        assert result is not None
        key, scale = result
        assert key == "G"
        assert scale == KeyScale.MINOR

    def test_invalid_notation(self):
        """Test that invalid musical-key notation returns None."""
        assert musical_to_key("H") is None
        assert musical_to_key("Xm") is None
        assert musical_to_key("Z") is None


class TestCamelotToKey:
    """Test camelot_to_key function."""

    def test_major_keys(self):
        """Test conversion of Camelot code to major keys."""
        result = camelot_to_key("8B")
        assert result is not None
        key, scale = result
        assert key == "C"
        assert scale == KeyScale.MAJOR

        result = camelot_to_key("12B")
        assert result is not None
        key, scale = result
        assert key == "E"
        assert scale == KeyScale.MAJOR

    def test_minor_keys(self):
        """Test conversion of Camelot code to minor keys."""
        result = camelot_to_key("6A")
        assert result is not None
        key, scale = result
        assert key == "G"
        assert scale == KeyScale.MINOR

        result = camelot_to_key("8A")
        assert result is not None
        key, scale = result
        assert key == "A"
        assert scale == KeyScale.MINOR

    def test_sharp_notation(self):
        """Test conversion of FSharp Camelot code."""
        result = camelot_to_key("11A")
        assert result is not None
        key, scale = result
        assert key == "FSharp"
        assert scale == KeyScale.MINOR

    def test_case_variations(self):
        """Test that case variations are handled."""
        result = camelot_to_key("6a")
        assert result is not None
        key, scale = result
        assert key == "G"
        assert scale == KeyScale.MINOR

    def test_invalid_notation(self):
        """Test that invalid Camelot code returns None."""
        assert camelot_to_key("13A") is None
        assert camelot_to_key("0B") is None


class TestMusicalToCamelot:
    """Test musical_to_camelot function."""

    def test_major_conversions(self):
        """Test conversion from musical to camelot for major keys."""
        assert musical_to_camelot("C") == "8B"
        assert musical_to_camelot("E") == "12B"
        assert musical_to_camelot("G") == "9B"

    def test_minor_conversions(self):
        """Test conversion from musical to camelot for minor keys."""
        assert musical_to_camelot("Gm") == "6A"
        assert musical_to_camelot("Am") == "8A"
        assert musical_to_camelot("Dbm") == "12A"

    def test_invalid_notation(self):
        """Test that invalid musical-key notation returns None."""
        assert musical_to_camelot("H") is None


class TestCamelotToMusical:
    """Test camelot_to_musical function."""

    def test_major_conversions(self):
        """Test conversion from camelot to musical for major keys."""
        assert camelot_to_musical("8B") == "C"
        assert camelot_to_musical("12B") == "E"
        assert camelot_to_musical("9B") == "G"

    def test_minor_conversions(self):
        """Test conversion from camelot to musical for minor keys."""
        assert camelot_to_musical("6A") == "Gm"
        assert camelot_to_musical("8A") == "Am"
        assert camelot_to_musical("12A") == "Dbm"

    def test_invalid_notation(self):
        """Test that invalid Camelot code returns None."""
        assert camelot_to_musical("13A") is None


class TestValidationFunctions:
    """Test validation functions."""

    def test_is_valid_key(self):
        """Test is_valid_key function."""
        assert is_valid_key("C", KeyScale.MAJOR) is True
        assert is_valid_key("G", KeyScale.MINOR) is True
        assert is_valid_key("FSharp", KeyScale.MAJOR) is True
        assert is_valid_key("H", KeyScale.MAJOR) is False
        assert is_valid_key("C", "INVALID") is False

    def test_is_valid_musical(self):
        """Test is_valid_musical function."""
        assert is_valid_musical("C") is True
        assert is_valid_musical("Gm") is True
        assert is_valid_musical("F#m") is True
        assert is_valid_musical("H") is False
        assert is_valid_musical("Xm") is False
        assert is_valid_musical("13A") is False

    def test_is_valid_camelot(self):
        """Test is_valid_camelot function."""
        assert is_valid_camelot("8B") is True
        assert is_valid_camelot("6A") is True
        assert is_valid_camelot("12A") is True
        assert is_valid_camelot("13A") is False
        assert is_valid_camelot("0B") is False


class TestFormatInitialKey:
    """Test format_initial_key function."""

    def test_format_musical_major(self):
        """Test formatting to musical-key notation for major keys."""
        assert format_initial_key("C", "MAJOR", CamelotFormat.MUSICAL) == "C"
        assert format_initial_key("E", "MAJOR", "musical") == "E"

    def test_format_musical_minor(self):
        """Test formatting to musical-key notation for minor keys."""
        assert format_initial_key("G", "MINOR", CamelotFormat.MUSICAL) == "Gm"
        assert format_initial_key("A", "MINOR", "musical") == "Am"

    def test_format_camelot_major(self):
        """Test formatting to Camelot code for major keys."""
        assert format_initial_key("C", "MAJOR", CamelotFormat.CAMELOT) == "8B"
        assert format_initial_key("E", "MAJOR", "camelot") == "12B"

    def test_format_camelot_minor(self):
        """Test formatting to Camelot code for minor keys."""
        assert format_initial_key("G", "MINOR", CamelotFormat.CAMELOT) == "6A"
        assert format_initial_key("A", "MINOR", "camelot") == "8A"

    def test_format_unknown_key(self):
        """Test that UNKNOWN key returns empty string."""
        assert format_initial_key("UNKNOWN", "MAJOR", CamelotFormat.MUSICAL) == ""
        assert format_initial_key("UNKNOWN", "MINOR", CamelotFormat.CAMELOT) == ""

    def test_format_unknown_scale(self):
        """Test that UNKNOWN scale returns empty string."""
        assert format_initial_key("C", "UNKNOWN", CamelotFormat.MUSICAL) == ""
        assert format_initial_key("G", "UNKNOWN", CamelotFormat.CAMELOT) == ""

    def test_format_both_unknown(self):
        """Test that both UNKNOWN returns empty string."""
        assert format_initial_key("UNKNOWN", "UNKNOWN", CamelotFormat.MUSICAL) == ""
        assert format_initial_key("UNKNOWN", "UNKNOWN", CamelotFormat.CAMELOT) == ""

    def test_format_invalid_key(self):
        """Test that invalid key returns empty string."""
        assert format_initial_key("InvalidKey", "MAJOR", CamelotFormat.MUSICAL) == ""
        assert format_initial_key("H", "MINOR", CamelotFormat.CAMELOT) == ""

    def test_format_invalid_format(self):
        """Test that invalid format returns empty string."""
        assert format_initial_key("C", "MAJOR", "invalid_format") == ""

    def test_format_fsharp_keys(self):
        """Test formatting FSharp keys in both notations."""
        assert format_initial_key("FSharp", "MINOR", CamelotFormat.MUSICAL) == "F#m"
        assert format_initial_key("FSharp", "MINOR", CamelotFormat.CAMELOT) == "11A"
        assert format_initial_key("FSharp", "MAJOR", CamelotFormat.MUSICAL) == "Gb"
        assert format_initial_key("FSharp", "MAJOR", CamelotFormat.CAMELOT) == "2B"


class TestRoundTripConversions:
    """Test round-trip conversions to ensure consistency."""

    def test_key_to_camelot_to_key(self):
        """Test that key -> camelot -> key preserves values."""
        original_key = "C"
        original_scale = KeyScale.MAJOR

        camelot = key_to_camelot(original_key, original_scale)
        assert camelot is not None

        result = camelot_to_key(camelot)
        assert result is not None

        result_key, result_scale = result
        assert result_key == original_key
        assert result_scale == original_scale

    def test_key_to_musical_to_key(self):
        """Test that key -> musical -> key preserves values."""
        original_key = "G"
        original_scale = KeyScale.MINOR

        musical = key_to_musical(original_key, original_scale)
        assert musical is not None

        result = musical_to_key(musical)
        assert result is not None

        result_key, result_scale = result
        assert result_key == original_key
        assert result_scale == original_scale

    def test_camelot_to_musical_to_camelot(self):
        """Test that camelot -> musical -> camelot preserves values."""
        original_camelot = "8B"

        musical = camelot_to_musical(original_camelot)
        assert musical is not None

        result_camelot = musical_to_camelot(musical)
        assert result_camelot == original_camelot
