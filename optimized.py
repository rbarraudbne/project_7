import csv
import time

BUDGET = 500.0   # budget maximal par client (en euros)
PRECISION = 100  # 100 = on travaille au centime près (2 décimales)


def load_actions(path):
    """Lit le CSV et retourne une liste d'actions (nom, coût en euros,
    bénéfice en euros après 2 ans)."""
    actions = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # en-têtes en français, ignorées
        for name, cost, percent in reader:
            cost = float(cost)
            percent = float(percent.strip().rstrip("%"))
            if cost <= 0:
                continue
            actions.append({
                "name": name,
                "cost": cost,
                "profit": cost * percent / 100,
            })
    return actions


def knapsack(actions, budget=BUDGET, precision=PRECISION):
    """Sac à dos 0/1 par programmation dynamique, pour des coûts décimaux.

    Le sac à dos classique exige des coûts entiers, car il indexe un
    tableau par le budget. On contourne ça en mettant les coûts à
    l'échelle : avec precision=100, 12.34 € devient 1234 "centimes",
    un entier. Le tableau dp est alors indexé en centimes, et on
    reconvertit le budget trouvé en euros à la fin.

    """
    budget_scaled = int(round(budget * precision))
    scaled_actions = [
        {**a, "cost_scaled": int(round(a["cost"] * precision))}
        for a in actions
    ]

    n = len(scaled_actions)
    dp = [0.0] * (budget_scaled + 1)
    choice = [[False] * (budget_scaled + 1) for _ in range(n)]

    for i, action in enumerate(scaled_actions):
        cost, profit = action["cost_scaled"], action["profit"]
        for b in range(budget_scaled, cost - 1, -1):
            candidate = dp[b - cost] + profit
            if candidate > dp[b]:
                dp[b] = candidate
                choice[i][b] = True

    # reconstruction de la combinaison à partir de la table de choix
    combo = []
    b = budget_scaled
    for i in range(n - 1, -1, -1):
        if choice[i][b]:
            combo.append(actions[i])  # on garde les coûts non arrondis d'origine
            b -= scaled_actions[i]["cost_scaled"]
    combo.reverse()

    return combo, dp[budget_scaled]


def main():
    start = time.time()
    actions = load_actions("dataset1.csv")
    combo, profit = knapsack(actions)

    print("Actions à acheter :", ", ".join(a["name"] for a in combo))
    print(f"Coût total : {sum(a['cost'] for a in combo):.2f} €")
    print(f"Bénéfice après 2 ans : {profit:.2f} €")
    print(f"Temps d'exécution : {time.time() - start:.4f} s")


if __name__ == "__main__":
    main()