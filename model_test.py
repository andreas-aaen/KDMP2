from TerrainIdentifier import TileDivsion, Clustering, IdentifyBoard, cluster_names, Terrain_clusters
from kingdomino_algo import calculate_kingdomino_score
from templatematching import templateMatching
import cv2
import os
# === TRAIN THE CLUSTERING MODEL ONCE ===
TileList = TileDivsion()
Labels, Model = Clustering(TileList, Terrain_clusters)
# === GROUND TRUTH SCORES ===
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
tested = 0
# === TEST ON BOARDS 60–74 ===
script_dir = os.path.dirname(os.path.abspath(__file__))
for i in range(60, 75):
    img_path = os.path.join(script_dir, f"Test_Boards/{i}.jpg")
    if not os.path.exists(img_path):
        print(f"❌ Could not find {img_path}")
        continue
    # === Predict terrain
    terrain_grid = IdentifyBoard(img_path, Model, cluster_names)
    # === Detect crowns
    crown_data = templateMatching(img_path)
    # === Build full board with terrain and crowns
    updated_grid = []
    for row in terrain_grid:
        updated_row = []
        for tile in row:
            updated_row.append({
                "type": tile,
                "crowns": 0
            })
        updated_grid.append(updated_row)
    for (x, y), crowns in crown_data.items():
        try:
            updated_grid[y][x]['crowns'] = crowns
        except IndexError:
            print(f"⚠️ Warning: Skipping crown at ({x},{y})")
    # === Calculate score
    score = calculate_kingdomino_score(updated_grid)
    gt = ground_truth_scores[i - 1]
    if score == gt:
        correct += 1
    tested += 1
    print(f"{i}.jpg — Predicted: {score}, Ground truth: {gt}")
# === FINAL RESULT
accuracy = correct / tested * 100
print(f"\n✅ Overall score match: {accuracy:.2f}% ({correct} correct out of {tested})")
