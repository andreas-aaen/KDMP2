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

def main():
    #Test grid (picture 1)
    grid_1 = [
        [{'type': 'grass', 'crowns': 0}, {'type': 'water', 'crowns': 0}, {'type': 'forest', 'crowns': 0}, {'type': 'forest', 'crowns': 0}, {'type': 'forest', 'crowns': 0}],
        [{'type': 'grass', 'crowns': 0}, {'type': 'forest', 'crowns': 0}, {'type': 'forest', 'crowns': 0}, {'type': 'forest', 'crowns': 1}, {'type': 'grass', 'crowns': 0}],
        [{'type': 'grass', 'crowns': 0}, {'type': 'swamp', 'crowns': 1}, None,                              {'type': 'forest', 'crowns': 0}, {'type': 'grass', 'crowns': 0}],
        [{'type': 'grass', 'crowns': 0}, {'type': 'swamp', 'crowns': 2}, {'type': 'lake', 'crowns': 0}, {'type': 'grass', 'crowns': 2}, {'type': 'grass', 'crowns': 1}],
        [{'type': 'forest', 'crowns': 0}, {'type': 'lake', 'crowns': 1}, {'type': 'lake', 'crowns': 0}, {'type': 'grass', 'crowns': 1}, {'type': 'field', 'crowns': 0}]
    ]
    #Test grid (picture 2)
    grid_2 = [
        [{'type': 'field', 'crowns': 0}, {'type': 'swamp', 'crowns': 0}, {'type': 'field', 'crowns': 0}, {'type': 'mine', 'crowns': 2}, {'type': 'swamp', 'crowns': 0}],
        [{'type': 'mine', 'crowns': 1}, {'type': 'swamp', 'crowns': 1}, {'type': 'field', 'crowns': 0}, {'type': 'field', 'crowns': 0}, {'type': 'forest', 'crowns': 0}],
        [{'type': 'mine', 'crowns': 2}, {'type': 'swamp', 'crowns': 0},         None,                   {'type': 'field', 'crowns': 0}, {'type': 'field', 'crowns': 0}],
        [{'type': 'mine', 'crowns': 2}, {'type': 'mine', 'crowns': 3}, {'type': 'grass', 'crowns': 0}, {'type': 'grass', 'crowns': 0}, {'type': 'field', 'crowns': 1}],
        [{'type': 'field', 'crowns': 0}, {'type': 'field', 'crowns': 0}, {'type': 'swamp', 'crowns': 0}, {'type': 'swamp', 'crowns': 0}, {'type': 'grass', 'crowns': 0}]
    ]

    # Calculate and print the score
    score = calculate_kingdomino_score(grid_2)
    print(f"Total Kingdomino Score: {score}")

if __name__ == "__main__":
    main()