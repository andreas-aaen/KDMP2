
ground_truth_scores = [
    36, 43, 52, 42, 36, 43, 41, 42, 45, 38,
    49, 22, 45, 37, 49, 22, 40, 60, 36, 52,
    40, 60, 36, 52, 44, 48, 59, 63, 48, 48,
    67, 65, 21, 46, 45, 43, 21, 26, 46, 33,
    40, 66, 55, 33, 38, 43, 66, 42, 26, 34,
    37, 40, 23, 34, 24, 44, 64, 36, 38, 44,
    64, 36, 37, 66, 80, 124, 99, 66, 124, 99,
    66, 80, 124, 99
]

correct = 0

for i in range(60, 75):
    grid = calculated_grid(f"{i}.jpg")
    score = calculate_kingdomino_score(grid)
    gt = ground_truth_scores[i - 1]

    if score == gt:
        correct += 1

    print(f"{i}.jpg — Beregnet: {score}, Ground truth: {gt}")

accuracy = correct / len(ground_truth_scores) * 100
print(f"\nAndel præcist korrekte scores: {accuracy:.2f}% ({correct} ud af {len(ground_truth_scores)})")
