def numIslands(grid):
    if not grid:
        return 0
    def dfs(i, j):
        if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]) or grid[i][j] == '0':
            return

        grid[i][j] = '0'
        dfs(i + 1, j)  # down
        dfs(i - 1, j)  # up
        dfs(i, j + 1)  # right
        dfs(i, j - 1)  # left
    island_count = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '1':
                island_count += 1
                dfs(i, j)
    return island_count
