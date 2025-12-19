#!/usr/bin/env python3
"""Simulation de la logique des quinzaines avec reference_year"""

def simulate_quinzaine_logic(reference_year: str, year: int, mois: str) -> tuple[str, str]:
    """
    Simule la logique des quinzaines avec reference_year.
    
    Args:
        reference_year: "even" ou "odd"
        year: Année à tester
        mois: "july" ou "august"
    
    Returns:
        Tuple (quinzaine, explication)
    """
    is_even_year = year % 2 == 0
    
    if reference_year == "even":
        # reference_year='even': années paires = 2ème quinzaine, années impaires = 1ère quinzaine
        if is_even_year:
            quinzaine = "2ème"
        else:
            quinzaine = "1ère"
    else:  # reference_year == "odd"
        # reference_year='odd': années impaires = 2ème quinzaine, années paires = 1ère quinzaine
        if is_even_year:
            quinzaine = "1ère"
        else:
            quinzaine = "2ème"
    
    explication = f"Année {year} ({'paire' if is_even_year else 'impaire'}), ref={reference_year} → {quinzaine} quinzaine de {mois}"
    return quinzaine, explication


def print_simulation_table():
    """Affiche un tableau de simulation pour les quinzaines"""
    print("=" * 90)
    print("SIMULATION: Règles de quinzaines avec reference_year")
    print("=" * 90)
    print()
    
    years = [2023, 2024, 2025, 2026]
    reference_years = ["even", "odd"]
    mois_list = ["juillet", "août"]
    
    for mois in mois_list:
        print(f"\n{mois.upper()}:")
        print("-" * 90)
        print(f"{'Année':<8} {'Parité':<10} {'reference_year':<18} {'Quinzaine assignée':<20} {'Explication'}")
        print("-" * 90)
        
        for year in years:
            is_even = year % 2 == 0
            parity_str = "Paire" if is_even else "Impaire"
            
            for ref_year in reference_years:
                quinzaine, explication = simulate_quinzaine_logic(ref_year, year, mois)
                ref_year_display = "Paire" if ref_year == "even" else "Impaire"
                print(f"{year:<8} {parity_str:<10} {ref_year_display:<18} {quinzaine:<20} {explication}")
        print()
    
    print("=" * 90)
    print()
    
    # Scénarios spécifiques
    print("SCÉNARIOS D'EXEMPLE:")
    print("-" * 90)
    
    scenarios = [
        ("even", 2024, "juillet", "2ème"),
        ("even", 2025, "juillet", "1ère"),
        ("even", 2024, "août", "2ème"),
        ("even", 2025, "août", "1ère"),
        ("odd", 2024, "juillet", "1ère"),
        ("odd", 2025, "juillet", "2ème"),
        ("odd", 2024, "août", "1ère"),
        ("odd", 2025, "août", "2ème"),
    ]
    
    for ref_year, year, mois, expected_quinzaine in scenarios:
        quinzaine, explication = simulate_quinzaine_logic(ref_year, year, mois)
        status = "✅" if quinzaine == expected_quinzaine else "❌"
        print(f"{status} {explication}")


def compare_rules():
    """Compare les différentes règles"""
    print("\n" + "=" * 90)
    print("COMPARAISON DES RÈGLES")
    print("=" * 90)
    print()
    
    print("RÈGLE ACTUELLE (sans reference_year):")
    print("  - july_first_half: Toujours 1ère quinzaine de juillet")
    print("  - july_second_half: Toujours 2ème quinzaine de juillet")
    print("  - august_first_half: Toujours 1ère quinzaine d'août")
    print("  - august_second_half: Toujours 2ème quinzaine d'août")
    print()
    
    print("NOUVELLE RÈGLE (avec reference_year):")
    print("  - july_first_half: 1ère quinzaine selon reference_year")
    print("    * reference_year='even': années impaires seulement")
    print("    * reference_year='odd': années paires seulement")
    print("  - july_second_half: 2ème quinzaine selon reference_year")
    print("    * reference_year='even': années paires seulement")
    print("    * reference_year='odd': années impaires seulement")
    print("  - august_first_half: 1ère quinzaine selon reference_year")
    print("    * reference_year='even': années impaires seulement")
    print("    * reference_year='odd': années paires seulement")
    print("  - august_second_half: 2ème quinzaine selon reference_year")
    print("    * reference_year='even': années paires seulement")
    print("    * reference_year='odd': années impaires seulement")
    print()


if __name__ == "__main__":
    print_simulation_table()
    compare_rules()
    
    print("\n" + "=" * 90)
    print("CONCLUSION:")
    print("=" * 90)
    print("Les règles de quinzaines utiliseront reference_year pour déterminer")
    print("automatiquement si la quinzaine s'applique selon la parité de l'année.")
    print("=" * 90)

