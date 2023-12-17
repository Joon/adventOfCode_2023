import numpy as np

world = [[c for c in l.strip()] for l in open("Inputs/day14_test.txt", "r").readlines()]

def print_world(world):
    for row in world:
        print("".join(row))

def world_as_matrice(world):
    return np.array([[1 if c == 'O' else -1 if c == '#' else 0 for c in row] for row in world])

def transformer(a, shift, axis):
    return np.roll(a, shift, axis=axis)
    
def tilt(world_matrice, y_movement, x_movement):
    np.apply_along_axis(transformer, 0, world_matrice, y_movement)
    world_matrice = np.roll(world_matrice, y_movement, axis=0)
    world_matrice = np.roll(world_matrice, x_movement, axis=1)
    return world_matrice

print("Original Matrix:")
print(world_as_matrice(world))

tilted = tilt(world_as_matrice(world), 1, 0)
print("Tilted Matrix:", tilted)

