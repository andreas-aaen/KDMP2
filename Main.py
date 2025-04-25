from TerrainIdentifier import GetBoard, TileDivsion, Clustering, IdentifyBoard, cluster_names, Terrain_clusters

TileList = TileDivsion()
Labels, Model = Clustering(TileList, Terrain_clusters)
Board = GetBoard()
IdentifyBoard(Board, Model, cluster_names)