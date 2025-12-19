#!/usr/bin/env python3
"""Simulation de la logique summer_parity_auto avec reference_year"""

from datetime import datetime

def simulate_summer_parity_auto(reference_year: str, year: int) -> tuple[str, str]:
    """
    Simule la logique summer_parity_auto avec reference_year.
    
    Args:
        reference_year: "even" ou "odd"
        year: Année à tester (ex: 2024, 2025)
    
    Returns:
        Tuple (mois_assigné, explication)
    """
    is_even_year = year % 2 == 0
    
    if reference_year == "even":
        # Année de référence paire
        if is_even_year:
            # Année paire → Août
            return "Août", f"Année {year} est paire, reference_year=even → Août"
        else:
            # Année impaire → Juillet
            return "Juillet", f"Année {year} est impaire, reference_year=even → Juillet"
    else:  # reference_year == "odd"
        # Année de référence impaire
        if is_even_year:
            # Année paire → Juillet (inverse de la logique "even")
            return "Juillet", f"Année {year} est paire, reference_year=odd → Juillet"
        else:
            # Année impaire → Août (inverse de la logique "even")
            return "Août", f"Année {year} est impaire, reference_year=odd → Août"


def print_simulation_table():
    """Affiche un tableau de simulation pour différentes années et reference_year"""
    print("=" * 80)
    print("SIMULATION: summer_parity_auto avec reference_year")
    print("=" * 80)
    print()
    
    years = [2023, 2024, 2025, 2026, 2027]
    reference_years = ["even", "odd"]
    
    print(f"{'Année':<8} {'Parité':<10} {'reference_year':<18} {'Mois assigné':<15} {'Explication'}")
    print("-" * 80)
    
    for year in years:
        is_even = year % 2 == 0
        parity_str = "Paire" if is_even else "Impaire"
        
        for ref_year in reference_years:
            mois, explication = simulate_summer_parity_auto(ref_year, year)
            ref_year_display = "Paire" if ref_year == "even" else "Impaire"
            print(f"{year:<8} {parity_str:<10} {ref_year_display:<18} {mois:<15} {explication}")
        print()
    
    print("=" * 80)
    print()
    
    # Scénarios spécifiques
    print("SCÉNARIOS D'EXEMPLE:")
    print("-" * 80)
    
    scenarios = [
        ("even", 2024, "Année paire avec reference_year=even"),
        ("even", 2025, "Année impaire avec reference_year=even"),
        ("odd", 2024, "Année paire avec reference_year=odd"),
        ("odd", 2025, "Année impaire avec reference_year=odd"),
    ]
    
    for ref_year, year, description in scenarios:
        mois, explication = simulate_summer_parity_auto(ref_year, year)
        print(f"\n{description}:")
        print(f"  → {mois} complet")
        print(f"  → {explication}")


def compare_with_current_logic():
    """Compare la nouvelle logique avec l'ancienne"""
    print("\n" + "=" * 80)
    print("COMPARAISON: Ancienne vs Nouvelle logique")
    print("=" * 80)
    print()
    
    print("ANCIENNE LOGIQUE (sans reference_year):")
    print("  - Année paire → Toujours Août")
    print("  - Année impaire → Toujours Juillet")
    print()
    
    print("NOUVELLE LOGIQUE (avec reference_year):")
    print("  - reference_year='even':")
    print("    * Année paire → Août")
    print("    * Année impaire → Juillet")
    print("  - reference_year='odd':")
    print("    * Année paire → Juillet")
    print("    * Année impaire → Août")
    print()
    
    print("EXEMPLE CONCRET (année 2024, paire):")
    print("  - Ancienne: → Août")
    print("  - Nouvelle avec reference_year='even': → Août")
    print("  - Nouvelle avec reference_year='odd': → Juillet")
    print()
    
    print("EXEMPLE CONCRET (année 2025, impaire):")
    print("  - Ancienne: → Juillet")
    print("  - Nouvelle avec reference_year='even': → Juillet")
    print("  - Nouvelle avec reference_year='odd': → Août")


if __name__ == "__main__":
    print_simulation_table()
    compare_with_current_logic()
    
    print("\n" + "=" * 80)
    print("CONCLUSION:")
    print("=" * 80)
    print("La nouvelle logique permet à chaque parent de configurer:")
    print("  - reference_year='even' → années paires = Août, impaires = Juillet")
    print("  - reference_year='odd' → années impaires = Août, paires = Juillet")
    print("Cela garantit une alternance équitable entre les deux parents.")
    print("=" * 80)

