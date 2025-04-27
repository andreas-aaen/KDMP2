from TerrainIdentifier import GetBoard, TileDivsion, Clustering, IdentifyBoard, cluster_names, Terrain_clusters
from kingdomino_algo import calculate_kingdomino_score
from templatematching import templateMatching

def updateBoardCrowns(board, crown_data):
    for (x, y), crowns in crown_data.items():
        try:
            board[y][x]['crowns'] = crowns
        except IndexError:
            print(f"Warning: Skipping out-of-bounds coordinate ({x},{y})")
    return board

def main():
    # Step 1: Train clustering model
    TileList = TileDivsion()
    Labels, Model = Clustering(TileList, Terrain_clusters)

    # Step 2: Select a test board
    Board = GetBoard()

    # Step 3: Identify terrain types
    tile_grid = IdentifyBoard(Board, Model, cluster_names)

    # Step 4: Detect crowns
    crown_data = templateMatching(Board)

    # Step 5: Update tile grid with crown counts
    updated_tile_grid = updateBoardCrowns(tile_grid, crown_data)

    # Step 6: Print final board
    print("\nUpdated Board:")
    for row in updated_tile_grid:
        print(row)

    # Step 7: Now you could also calculate score here if you want
    score = calculate_kingdomino_score(updated_tile_grid)
    print(f"Final Score: {score}")

if __name__ == "__main__":
    main()
