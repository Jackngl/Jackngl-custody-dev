#!/usr/bin/env python3
"""Test de la logique des quinzaines modifiée avec reference_year"""

def test_quinzaine_logic(reference_year: str, year: int, rule: str) -> tuple[bool, str]:
    """
    Teste la logique des quinzaines avec reference_year.
    
    Args:
        reference_year: "even" ou "odd"
        year: Année à tester
        rule: "july_first_half", "july_second_half", "august_first_half", "august_second_half"
    
    Returns:
        Tuple (should_apply, explication)
    """
    is_even_year = year % 2 == 0
    
    if rule == "july_first_half":
        should_apply = (reference_year == "even" and not is_even_year) or (reference_year == "odd" and is_even_year)
        quinzaine = "1ère quinzaine de juillet"
    elif rule == "july_second_half":
        should_apply = (reference_year == "even" and is_even_year) or (reference_year == "odd" and not is_even_year)
        quinzaine = "2ème quinzaine de juillet"
    elif rule == "august_first_half":
        should_apply = (reference_year == "even" and not is_even_year) or (reference_year == "odd" and is_even_year)
        quinzaine = "1ère quinzaine d'août"
    elif rule == "august_second_half":
        should_apply = (reference_year == "even" and is_even_year) or (reference_year == "odd" and not is_even_year)
        quinzaine = "2ème quinzaine d'août"
    else:
        return False, "Règle inconnue"
    
    if should_apply:
        explication = f"✅ {year} ({'paire' if is_even_year else 'impaire'}), ref={reference_year} → {quinzaine}"
    else:
        explication = f"❌ {year} ({'paire' if is_even_year else 'impaire'}), ref={reference_year} → {quinzaine} (ne s'applique pas)"
    
    return should_apply, explication


def test_all_scenarios():
    """Teste tous les scénarios possibles"""
    print("=" * 90)
    print("TEST DE LA LOGIQUE DES QUINZAINES MODIFIÉE")
    print("=" * 90)
    print()
    
    rules = ["july_first_half", "july_second_half", "august_first_half", "august_second_half"]
    years = [2023, 2024, 2025, 2026]
    reference_years = ["even", "odd"]
    
    for rule in rules:
        print(f"\n{rule.upper().replace('_', ' ')}:")
        print("-" * 90)
        
        for year in years:
            is_even = year % 2 == 0
            parity_str = "Paire" if is_even else "Impaire"
            
            for ref_year in reference_years:
                should_apply, explication = test_quinzaine_logic(ref_year, year, rule)
                ref_year_display = "Paire" if ref_year == "even" else "Impaire"
                status = "✅ APPLIQUE" if should_apply else "❌ N'APPLIQUE PAS"
                print(f"  {year} ({parity_str}), ref={ref_year_display}: {status}")
        print()
    
    print("=" * 90)
    print()
    
    # Vérification de l'alternance équitable
    print("VÉRIFICATION ALTERNANCE ÉQUITABLE:")
    print("-" * 90)
    
    # Parent 1 avec reference_year='even'
    print("\nParent 1 (reference_year='even'):")
    parent1_quinzaines = {}
    for year in range(2023, 2028):
        for rule in rules:
            should_apply, _ = test_quinzaine_logic("even", year, rule)
            if should_apply:
                if year not in parent1_quinzaines:
                    parent1_quinzaines[year] = []
                parent1_quinzaines[year].append(rule)
    
    for year, quinzaines in sorted(parent1_quinzaines.items()):
        print(f"  {year}: {', '.join(quinzaines)}")
    
    # Parent 2 avec reference_year='odd'
    print("\nParent 2 (reference_year='odd'):")
    parent2_quinzaines = {}
    for year in range(2023, 2028):
        for rule in rules:
            should_apply, _ = test_quinzaine_logic("odd", year, rule)
            if should_apply:
                if year not in parent2_quinzaines:
                    parent2_quinzaines[year] = []
                parent2_quinzaines[year].append(rule)
    
    for year, quinzaines in sorted(parent2_quinzaines.items()):
        print(f"  {year}: {', '.join(quinzaines)}")
    
    # Vérifier que les parents ont toujours des quinzaines différentes
    print("\nVérification alternance:")
    alternance_ok = True
    for year in range(2023, 2028):
        p1 = set(parent1_quinzaines.get(year, []))
        p2 = set(parent2_quinzaines.get(year, []))
        if p1 & p2:  # Intersection non vide
            print(f"  ❌ {year}: Conflit - Les deux parents ont {p1 & p2}")
            alternance_ok = False
        else:
            print(f"  ✅ {year}: Pas de conflit")
    
    print()
    if alternance_ok:
        print("✅ L'alternance est équitable : chaque année, les parents ont des quinzaines différentes")
    else:
        print("❌ PROBLÈME : Les parents ont parfois les mêmes quinzaines")
    
    print("=" * 90)


if __name__ == "__main__":
    test_all_scenarios()

