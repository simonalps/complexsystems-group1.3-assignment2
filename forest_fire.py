import numpy as np

def neighbour_is_burning(L, n, row, col):
    up = (row > 0) and (L[row - 1, col] == 2)
    down = (row < (n - 1)) and (L[row + 1, col] == 2)
    left = (col > 0) and (L[row, col - 1] == 2)
    right = (col < (n - 1)) and (L[row, col + 1] == 2)

    return up or down or left or right



# for the purpose of this replication we will keep d = 2 at all times!
# states: 0 empty, 1 tree, 2 burning
def model_step(L, n, p, f, rng):
    L_new = np.zeros((n, n))

    for i in range(n):
        for j in range(n):

            # L[i, j] = 0 --> the cell is empty, tree grows with probability p
            if L[i, j] == 0:
                if rng.random() < p:
                    L_new[i, j] = 1     # tree is growing with probability p
                else:
                    L_new[i, j] = 0     # cell remains empty
                continue

            # L[i, j] = 1 --> there is a tree at this cell
            if L[i, j] == 1:
                if neighbour_is_burning(L, n, i, j):
                    L_new[i, j] = 2     # tree cell is burning if is has a burning neighbour
                elif rng.random() < f:
                    L_new[i, j] = 2     # lightning strike causes tree to burn
                else:
                    L_new[i, j] = 1     # cell remains a tree
                continue

            # L[i, j] = 2 --> the cell is burning, now it must be empty
            if L[i, j] == 2:
                L_new[i, j] = 0         # cell is now empty
                continue

    return L_new


def run_model(L, n, p, f, steps, rng):

    for _ in range(steps):
        L = model_step(L, n, p, f, rng)

    return L