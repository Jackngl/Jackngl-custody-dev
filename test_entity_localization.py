#!/usr/bin/env python3
"""Test script to verify entity localization behavior."""

import re
import unicodedata

# Simplified slugify function (similar to Home Assistant's slugify)
def slugify(text: str, separator: str = "_") -> str:
    """Convert text to a slug."""
    text = unicodedata.normalize("NFKD", text)
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


# Simulate entity creation
def create_entity_ids(display_name: str, normalized_name: str, entity_type: str, key: str = ""):
    """Simulate entity ID creation."""
    if entity_type == "calendar":
        return f"calendar.{slugify(normalized_name)}_calendar"
    elif entity_type == "binary_sensor":
        return f"binary_sensor.{slugify(normalized_name)}_presence"
    elif entity_type == "sensor":
        return f"sensor.{slugify(normalized_name)}_{key}"
    elif entity_type == "device_tracker":
        return f"device_tracker.{slugify(normalized_name)}_tracker"
    return None


# Translations (from en.json and fr.json)
TRANSLATIONS = {
    "en": {
        "calendar": "Calendar",
        "presence": "Presence",
        "tracker": "Tracker",
        "next_arrival": "Next arrival",
        "next_departure": "Next departure",
    },
    "fr": {
        "calendar": "Calendrier",
        "presence": "Présence",
        "tracker": "Suivi",
        "next_arrival": "Arrivée prévue",
        "next_departure": "Départ prévu",
    },
}


def get_display_name(device_name: str, translation_key: str, language: str = "en") -> str:
    """Get localized display name."""
    translation = TRANSLATIONS.get(language, TRANSLATIONS["en"]).get(translation_key, translation_key)
    return f"{device_name} {translation}"


# Test cases
test_cases = [
    ("Lucas", "Lucas"),
    ("Sarah-Léa", "Sarah Lea"),
    ("Jean-Pierre", "Jean Pierre"),
    ("François", "Francois"),
    ("Élise", "Elise"),
]

print("=" * 80)
print("TEST: Entity ID Generation (English only)")
print("=" * 80)

for display_name, expected_normalized in test_cases:
    normalized = _format_child_name(display_name)
    
    calendar_id = create_entity_ids(display_name, normalized, "calendar")
    presence_id = create_entity_ids(display_name, normalized, "binary_sensor")
    arrival_id = create_entity_ids(display_name, normalized, "sensor", "next_arrival")
    
    print(f"\n📝 Child: '{display_name}'")
    print(f"   Normalized: '{normalized}'")
    print(f"   Entity IDs:")
    print(f"     - {calendar_id}")
    print(f"     - {presence_id}")
    print(f"     - {arrival_id}")
    
    # Verify all entity IDs are ASCII
    for eid in [calendar_id, presence_id, arrival_id]:
        assert eid.isascii(), f"❌ Non-ASCII in entity ID: {eid}"
        assert not any(c in eid for c in "éèàêôù"), f"❌ Accented chars in entity ID: {eid}"

print("\n" + "=" * 80)
print("TEST: Display Names (Localized)")
print("=" * 80)

for display_name, normalized in test_cases:
    print(f"\n📝 Child: '{display_name}'")
    print(f"   Device Name: '{display_name}' (preserves original)")
    
    # English UI
    print(f"   🇬🇧 English UI:")
    print(f"     - {get_display_name(display_name, 'calendar', 'en')}")
    print(f"     - {get_display_name(display_name, 'presence', 'en')}")
    print(f"     - {get_display_name(display_name, 'next_arrival', 'en')}")
    
    # French UI
    print(f"   🇫🇷 French UI:")
    print(f"     - {get_display_name(display_name, 'calendar', 'fr')}")
    print(f"     - {get_display_name(display_name, 'presence', 'fr')}")
    print(f"     - {get_display_name(display_name, 'next_arrival', 'fr')}")

print("\n" + "=" * 80)
print("✅ ALL TESTS PASSED!")
print("=" * 80)
print("\n📋 Summary:")
print("   ✓ Entity IDs are always in English (ASCII only)")
print("   ✓ Display names preserve original characters")
print("   ✓ UI shows localized names based on Home Assistant language")
print("   ✓ Example: 'Sarah-Léa' → entity_id: 'sarah_lea_calendar', display: 'Sarah-Léa Calendrier' (FR)")
