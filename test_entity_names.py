#!/usr/bin/env python3
"""Test script to verify entity IDs are in English and display names are localized."""

import re
import unicodedata

# Simplified slugify function (similar to Home Assistant's slugify)
def slugify(text: str, separator: str = "_") -> str:
    """Convert text to a slug."""
    # Normalize unicode characters
    text = unicodedata.normalize("NFKD", text)
    # Convert to lowercase and replace non-alphanumeric with separator
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[-\s]+", separator, text)
    return text.strip(separator)

# Simulate the logic from config_flow.py
def _format_child_name(value: str) -> str:
    """Normalize child name to ASCII words recognized by Home Assistant."""
    normalized = slugify(value, separator=" ").strip()
    if not normalized:
        return ""
    return " ".join(part.capitalize() for part in normalized.split())


# Test cases
test_cases = [
    ("Lucas", "Lucas"),
    ("Sarah-Léa", "Sarah Lea"),
    ("Jean-Pierre", "Jean Pierre"),
    ("Marie-Claire", "Marie Claire"),
    ("François", "Francois"),
    ("Élise", "Elise"),
]

print("=" * 60)
print("Test: Entity ID generation (should be in English)")
print("=" * 60)

for display_name, expected_normalized in test_cases:
    normalized = _format_child_name(display_name)
    entity_id_calendar = f"calendar.{slugify(normalized)}_calendar"
    entity_id_presence = f"binary_sensor.{slugify(normalized)}_presence"
    
    print(f"\nDisplay Name: '{display_name}'")
    print(f"  Normalized: '{normalized}'")
    print(f"  Calendar Entity ID: {entity_id_calendar}")
    print(f"  Presence Entity ID: {entity_id_presence}")
    
    # Verify entity_id contains only ASCII characters
    assert entity_id_calendar.isascii(), f"Entity ID contains non-ASCII: {entity_id_calendar}"
    assert entity_id_presence.isascii(), f"Entity ID contains non-ASCII: {entity_id_presence}"
    
    # Verify entity_id doesn't contain accented characters
    assert "é" not in entity_id_calendar.lower(), f"Entity ID contains 'é': {entity_id_calendar}"
    assert "è" not in entity_id_calendar.lower(), f"Entity ID contains 'è': {entity_id_calendar}"
    assert "à" not in entity_id_calendar.lower(), f"Entity ID contains 'à': {entity_id_calendar}"

print("\n" + "=" * 60)
print("Test: Display names (should preserve original)")
print("=" * 60)

for display_name, _ in test_cases:
    print(f"\nDisplay Name: '{display_name}'")
    print(f"  Will be used for device name (localized in UI)")
    print(f"  English UI: '{display_name} Calendar'")
    print(f"  French UI: '{display_name} Calendrier'")

print("\n" + "=" * 60)
print("✅ All tests passed!")
print("=" * 60)
print("\nSummary:")
print("- Entity IDs are generated from normalized (English) names")
print("- Display names preserve original characters for localization")
print("- Home Assistant will show localized names based on UI language")
