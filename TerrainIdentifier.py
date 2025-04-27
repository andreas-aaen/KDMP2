# Import libraries
from sklearn.cluster import KMeans
from tkinter import simpledialog
import matplotlib.pylab as plt
from pathlib import Path
import tkinter as tk
import numpy as np
import cv2

# Define the amount of clusters we use
Terrain_clusters = 9

# Manual classification of clusters
cluster_names = {
0: "Forest",
1: "Lake",
2: "Forest",
3: "Field",
4: "Swamp",
5: "Lake",
6: "Castle",
7: "Mine",
8: "Grassland"
}

# Dividing the board into 100x100 pixels and appending the tiles to a tileslist and returning it.
def TileDivsion():
    folder = Path.cwd() / "Train_boards"
    BoardCount = 0
    TileCount = 0

    BoardsList = []
    TileList = []

    for board in folder.iterdir():
        if board.is_file():
            # Converting the colors from RGB to HSV for higher accuracy
            img = cv2.imread(str(board))
            boardHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            BoardCount +=1
            BoardsList.append(boardHSV)

            for x in range(5):
                for y in range(5):
                    tile = boardHSV[x*100:(x+1)*100, y*100:(y+1)*100]
                    TileList.append(tile)
                    TileCount += 1
    print(f"Boards: {BoardCount}, Tiles: {TileCount}")
    return TileList 


# Defining K means after flattening the images, and returning the clusters and the model itself.
def Clustering(TilesList, Terrain_clusters):
    FlatTileList = []
    for tile in TilesList:
        Flattenedtile = tile.flatten() 
        FlatTileList.append(Flattenedtile)

    X = np.array(FlatTileList)

    Model = KMeans(n_clusters=Terrain_clusters, random_state=42)
    labels = Model.fit_predict(X)

    return labels, Model


# Creating an input UI and converting the number of the image into Integers and extracting the board from the folder and returning the image.
def GetBoard():
    root = tk.Tk()
    root.withdraw()

    img_num = simpledialog.askstring("Board Selector", "Enter board number:")
    if img_num is None:
        print("No input provided. Exiting...")
        exit()

    num = int(img_num)

    Boards = Path.cwd() / "Test_Boards"
    img = Boards / f"{num}.jpg"

    print(f"Selected Board: {img_num}")

    return img

# Getting an image from our test boards and applying the model, then returning a list of lists with dictionaries.
def IdentifyBoard(Board, Model, cluster_names):
    tiles =  []
    flattened_tiles = []
    terrain_names = []
    terrain_index = 0

    Image = cv2.imread(str(Board))
    boardHSV = cv2.cvtColor(Image, cv2.COLOR_BGR2HSV)
    BoardRGB = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)

    # Split board to a list consisting of lists (5 lists)
    for x in range(5):
        rows = []
        for y in range(5):
            tile = boardHSV[x*100:(x+1)*100, y*100:(y+1)*100]
            rows.append(tile)
        tiles.append(rows)


    
    # Flatten tiles for prediction
    for row in tiles:
        for tile in row:
            flattened_tile = tile.flatten()
            flattened_tiles.append(flattened_tile)

    # Predict and build tile grid with terrain type + value
    X = np.array(flattened_tiles)
    cluster_ids = Model.predict(X)

    tile_grid = []
    terrain_index = 0
    for x in range(5):
        row_dicts = []
        for y in range(5):
            cluster_id = cluster_ids[terrain_index]
            terrain_type = cluster_names[cluster_id]
            tile_data = {"type": terrain_type, "crowns": 0}
            row_dicts.append(tile_data)
            terrain_index += 1
        tile_grid.append(row_dicts)

    # Show board with terrain names
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(BoardRGB)
    ax.axis('off')
    for x in range(5):
        for y in range(5):
            terrain = tile_grid[x][y]["type"]
            center_x = y * 100 + 50
            center_y = x * 100 + 50
            ax.text(center_x, center_y, terrain, color='white', fontsize=8,
                    ha='center', va='center', bbox=dict(facecolor='black', alpha=0.6, boxstyle='round,pad=0.3'))
    print(tile_grid)
    plt.tight_layout()
    plt.show()
    return tile_grid
