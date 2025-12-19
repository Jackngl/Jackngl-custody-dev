#!/usr/bin/env python3
"""Test de la logique summer_parity_auto modifiée avec reference_year"""

from datetime import datetime, time
from typing import Any

# Simulation simplifiée de la logique
def test_summer_parity_logic(reference_year: str, year: int) -> str:
    """Teste la logique summer_parity_auto"""
    is_even_year = year % 2 == 0
    
    if reference_year == "even":
        assign_august = is_even_year
    else:
        assign_august = not is_even_year
    
    return "Août" if assign_august else "Juillet"


def test_all_scenarios():
    """Teste tous les scénarios possibles"""
    print("=" * 80)
    print("TEST DE LA LOGIQUE MODIFIÉE")
    print("=" * 80)
    print()
    
    test_cases = [
        ("even", 2023, "Impaire", "Juillet"),
        ("even", 2024, "Paire", "Août"),
        ("even", 2025, "Impaire", "Juillet"),
        ("even", 2026, "Paire", "Août"),
        ("odd", 2023, "Impaire", "Août"),
        ("odd", 2024, "Paire", "Juillet"),
        ("odd", 2025, "Impaire", "Août"),
        ("odd", 2026, "Paire", "Juillet"),
    ]
    
    print(f"{'reference_year':<18} {'Année':<8} {'Parité':<10} {'Attendu':<12} {'Résultat':<12} {'Status'}")
    print("-" * 80)
    
    all_passed = True
    for ref_year, year, parity, expected in test_cases:
        result = test_summer_parity_logic(ref_year, year)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        if result != expected:
            all_passed = False
        
        ref_display = "Paire" if ref_year == "even" else "Impaire"
        print(f"{ref_display:<18} {year:<8} {parity:<10} {expected:<12} {result:<12} {status}")
    
    print("-" * 80)
    print(f"\nRésultat global: {'✅ TOUS LES TESTS PASSÉS' if all_passed else '❌ CERTAINS TESTS ONT ÉCHOUÉ'}")
    print()
    
    # Vérification de l'alternance équitable
    print("=" * 80)
    print("VÉRIFICATION ALTERNANCE ÉQUITABLE")
    print("=" * 80)
    print()
    
    # Parent 1 avec reference_year='even'
    print("Parent 1 (reference_year='even'):")
    parent1_years = []
    for year in range(2023, 2028):
        mois = test_summer_parity_logic("even", year)
        parent1_years.append((year, mois))
        print(f"  {year} ({'paire' if year % 2 == 0 else 'impaire'}): {mois}")
    
    # Parent 2 avec reference_year='odd'
    print("\nParent 2 (reference_year='odd'):")
    parent2_years = []
    for year in range(2023, 2028):
        mois = test_summer_parity_logic("odd", year)
        parent2_years.append((year, mois))
        print(f"  {year} ({'paire' if year % 2 == 0 else 'impaire'}): {mois}")
    
    # Vérifier que les parents ont toujours des mois différents
    print("\nVérification alternance:")
    alternance_ok = True
    for (y1, m1), (y2, m2) in zip(parent1_years, parent2_years):
        if m1 == m2:
            print(f"  ❌ {y1}: Les deux parents ont {m1}")
            alternance_ok = False
        else:
            print(f"  ✅ {y1}: Parent 1 = {m1}, Parent 2 = {m2}")
    
    print()
    if alternance_ok:
        print("✅ L'alternance est équitable : chaque année, les parents ont des mois différents")
    else:
        print("❌ PROBLÈME : Les parents ont parfois le même mois")
    
    print("=" * 80)


if __name__ == "__main__":
    test_all_scenarios()

