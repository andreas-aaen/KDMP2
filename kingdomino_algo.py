def calculate_kingdomino_score(grid):

#Calculate the total score for a Kingdomino board.
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    total_score = 0

    def is_valid_tile(r, c, target_type):
    #Check if a tile is valid for region calculation.
        return (0 <= r < rows and 
                0 <= c < cols and 
                grid[r][c] is not None and 
                grid[r][c]['type'] == target_type and 
                not visited[r][c])

    def dfs(r, c, target_type):
    #Depth-first search to calculate region size and total crowns
        visited[r][c] = True
        
        region_tiles = 1
        region_crowns = grid[r][c]['crowns']
        
        #Possible directions: up, right, down, left
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        for dr, dc in directions:
            new_r, new_c = r + dr, c + dc
            
            if is_valid_tile(new_r, new_c, target_type):
                sub_tiles, sub_crowns = dfs(new_r, new_c, target_type)
                region_tiles += sub_tiles
                region_crowns += sub_crowns
        
        return region_tiles, region_crowns

    #Iterate through all grid cells
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] is None or visited[r][c]:
                continue
            
            region_tiles, region_crowns = dfs(r, c, grid[r][c]['type'])
            region_score = region_tiles * region_crowns
            total_score += region_score

    return total_score