import csv
from itertools import combinations

BUDGET = 500  # budget maximal par client (en euros)


def load_actions(path):
    """Lit le CSV et retourne une liste d'actions.

    Chaque action est un dictionnaire : nom, coût (€) et bénéfice (€) après 2 ans.
    """
    actions = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # ignore la ligne d'en-têtes (en français)

        # Lecture par position : nom, coût, bénéfice (et non par nom de colonne)
        for name, cost, percent in reader:
            cost = float(cost)
            # « 5% » -> 5.0 : on retire le signe % avant la conversion
            percent = float(percent.strip().rstrip("%"))
            actions.append({
                "name": name,
                "cost": cost,
                "profit": cost * percent / 100,  # le bénéfice est un % du coût
            })
    return actions


def brute_force(actions, budget=BUDGET):
    """Teste toutes les combinaisons possibles et garde la plus rentable
    parmi celles qui respectent le budget."""
    best_profit = 0
    best_combo = ()
    for size in range(1, len(actions) + 1):
        for combo in combinations(actions, size):
            cost = sum(a["cost"] for a in combo)
            if cost > budget:
                continue
            profit = sum(a["profit"] for a in combo)
            if profit > best_profit:
                best_profit = profit
                best_combo = combo
    return best_combo, best_profit


def main():
    actions = load_actions("actions.csv")
    combo, profit = brute_force(actions)

    print("Actions à acheter :", ", ".join(a["name"] for a in combo))
    print(f"Coût total : {sum(a['cost'] for a in combo):.2f} €")
    print(f"Bénéfice après 2 ans : {profit:.2f} €")


if __name__ == "__main__":
    main()