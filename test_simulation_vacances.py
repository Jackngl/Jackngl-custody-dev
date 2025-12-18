#!/usr/bin/env python3
"""
Simulation de répartition des vacances scolaires entre deux parents
Zone C - Années 2025-2026
"""

from datetime import datetime, timedelta

# Configuration Parent A
PARENT_A_REFERENCE_YEAR = "odd"  # Impaire
PARENT_A_SUMMER_RULE = "july"  # Juillet complet

# Configuration Parent B (automatiquement l'inverse)
PARENT_B_REFERENCE_YEAR = "even"  # Paire
PARENT_B_SUMMER_RULE = "august"  # Août complet

# Périodes de vacances Zone C (exemples)
VACANCES = {
    "Noël 2025": {
        "start": datetime(2025, 12, 20, 0, 0),
        "end": datetime(2026, 1, 5, 0, 0),
        "year": 2025,  # Année impaire
    },
    "Hiver 2026": {
        "start": datetime(2026, 2, 21, 0, 0),
        "end": datetime(2026, 3, 9, 0, 0),
        "year": 2026,  # Année paire
    },
    "Printemps 2026": {
        "start": datetime(2026, 4, 24, 0, 0),
        "end": datetime(2026, 5, 10, 0, 0),
        "year": 2026,  # Année paire
    },
    "Été 2026": {
        "start": datetime(2026, 7, 5, 0, 0),
        "end": datetime(2026, 9, 1, 0, 0),
        "year": 2026,  # Année paire
    },
    "Toussaint 2026": {
        "start": datetime(2026, 10, 18, 0, 0),
        "end": datetime(2026, 11, 3, 0, 0),
        "year": 2026,  # Année paire
    },
    "Noël 2026": {
        "start": datetime(2026, 12, 19, 0, 0),
        "end": datetime(2027, 1, 4, 0, 0),
        "year": 2026,  # Année paire
    },
    "Été 2027": {
        "start": datetime(2027, 7, 4, 0, 0),
        "end": datetime(2027, 8, 31, 0, 0),
        "year": 2027,  # Année impaire
    },
}

def calculate_midpoint(start, end):
    """Calcule le milieu exact entre deux dates."""
    delta = end - start
    return start + delta / 2

def simulate_vacation_split(vacation_name, start, end, year, parent_ref_year, summer_rule=None):
    """Simule la répartition d'une période de vacances."""
    is_even_year = year % 2 == 0
    is_summer = "Été" in vacation_name
    
    # Calcul du milieu pour les vacances normales
    midpoint = calculate_midpoint(start, end)
    
    if is_summer and summer_rule:
        # Logique pour les vacances d'été
        if summer_rule == "july":
            if is_even_year:
                # Année paire : Août complet
                return {
                    "parent": "A" if parent_ref_year == "odd" else "B",
                    "period": f"Août complet ({start.year})",
                    "start": datetime(start.year, 8, 1),
                    "end": datetime(start.year, 8, 31),
                }
            else:
                # Année impaire : Juillet complet
                return {
                    "parent": "A" if parent_ref_year == "odd" else "B",
                    "period": f"Juillet complet ({start.year})",
                    "start": datetime(start.year, 7, 1),
                    "end": datetime(start.year, 7, 31),
                }
        elif summer_rule == "august":
            if is_even_year:
                # Année paire : Août complet
                return {
                    "parent": "A" if parent_ref_year == "even" else "B",
                    "period": f"Août complet ({start.year})",
                    "start": datetime(start.year, 8, 1),
                    "end": datetime(start.year, 8, 31),
                }
            else:
                # Année impaire : Juillet complet
                return {
                    "parent": "A" if parent_ref_year == "even" else "B",
                    "period": f"Juillet complet ({start.year})",
                    "start": datetime(start.year, 7, 1),
                    "end": datetime(start.year, 7, 31),
                }
    else:
        # Logique pour les vacances normales (Noël, Hiver, Printemps, Toussaint)
        if parent_ref_year == "odd":
            # Parent avec reference_year "odd" (impaire) = 1ère partie
            if is_even_year:
                # Année paire : pas de garde (car c'est la 2ème partie)
                return {
                    "parent": "A" if parent_ref_year == "odd" else "B",
                    "period": "Aucune garde (2ème partie)",
                    "start": None,
                    "end": None,
                }
            else:
                # Année impaire : 1ère moitié
                return {
                    "parent": "A" if parent_ref_year == "odd" else "B",
                    "period": "1ère moitié",
                    "start": start,
                    "end": midpoint,
                }
        else:  # parent_ref_year == "even"
            # Parent avec reference_year "even" (paire) = 2ème partie
            if is_even_year:
                # Année paire : 2ème moitié
                return {
                    "parent": "A" if parent_ref_year == "even" else "B",
                    "period": "2ème moitié",
                    "start": midpoint,
                    "end": end,
                }
            else:
                # Année impaire : pas de garde (car c'est la 1ère partie)
                return {
                    "parent": "A" if parent_ref_year == "even" else "B",
                    "period": "Aucune garde (1ère partie)",
                    "start": None,
                    "end": None,
                }

def print_simulation():
    """Affiche la simulation complète."""
    print("=" * 80)
    print("SIMULATION RÉPARTITION VACANCES SCOLAIRES - ZONE C")
    print("=" * 80)
    print()
    print(f"PARENT A : reference_year = {PARENT_A_REFERENCE_YEAR} (impaire), summer_rule = {PARENT_A_SUMMER_RULE}")
    print(f"PARENT B : reference_year = {PARENT_B_REFERENCE_YEAR} (paire), summer_rule = {PARENT_B_SUMMER_RULE}")
    print()
    print("=" * 80)
    print()
    
    for vac_name, vac_data in VACANCES.items():
        start = vac_data["start"]
        end = vac_data["end"]
        year = vac_data["year"]
        
        print(f"📅 {vac_name.upper()}")
        print(f"   Période officielle : {start.strftime('%d/%m/%Y')} → {end.strftime('%d/%m/%Y')}")
        print(f"   Année : {year} ({'PAIRE' if year % 2 == 0 else 'IMPAIRE'})")
        print()
        
        # Parent A
        parent_a = simulate_vacation_split(
            vac_name, start, end, year, 
            PARENT_A_REFERENCE_YEAR, 
            PARENT_A_SUMMER_RULE if "Été" in vac_name else None
        )
        
        # Parent B (inverse)
        parent_b = simulate_vacation_split(
            vac_name, start, end, year,
            PARENT_B_REFERENCE_YEAR,
            PARENT_B_SUMMER_RULE if "Été" in vac_name else None
        )
        
        # Afficher les résultats
        print(f"   👤 PARENT A (reference_year: {PARENT_A_REFERENCE_YEAR}):")
        if parent_a["start"]:
            duration = (parent_a["end"] - parent_a["start"]).days
            print(f"      ✅ {parent_a['period']}")
            print(f"      📆 {parent_a['start'].strftime('%d/%m/%Y')} → {parent_a['end'].strftime('%d/%m/%Y')} ({duration} jours)")
        else:
            print(f"      ❌ {parent_a['period']}")
        print()
        
        print(f"   👤 PARENT B (reference_year: {PARENT_B_REFERENCE_YEAR}):")
        if parent_b["start"]:
            duration = (parent_b["end"] - parent_b["start"]).days
            print(f"      ✅ {parent_b['period']}")
            print(f"      📆 {parent_b['start'].strftime('%d/%m/%Y')} → {parent_b['end'].strftime('%d/%m/%Y')} ({duration} jours)")
        else:
            print(f"      ❌ {parent_b['period']}")
        print()
        
        # Vérification 50/50
        total_days = (end - start).days
        parent_a_days = (parent_a["end"] - parent_a["start"]).days if parent_a["start"] else 0
        parent_b_days = (parent_b["end"] - parent_b["start"]).days if parent_b["start"] else 0
        
        if parent_a_days + parent_b_days == total_days:
            print(f"   ✅ RÉPARTITION 50/50 : {parent_a_days} jours + {parent_b_days} jours = {total_days} jours")
        else:
            print(f"   ⚠️  ATTENTION : {parent_a_days} jours + {parent_b_days} jours = {parent_a_days + parent_b_days} jours (total: {total_days})")
        print()
        print("-" * 80)
        print()

if __name__ == "__main__":
    print_simulation()
