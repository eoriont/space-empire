# This utility file is used by Elijah's strategies
# to calculate some things

# Check if a position is within the grid
def is_in_bounds(x, y, bounds):
    x1, y1 = bounds
    return (x >= 0 and x < x1) and (y >= 0 and y < y1)


def get_possible_spots(pos, speed, bounds):
    return [(pos[0]+x, pos[1]+y)
            for x in range(-speed, speed+1)
            for y in range(-speed, speed+1)
            if abs(x)+abs(y) <= speed
            and is_in_bounds(pos[0]+x, pos[1]+y, bounds)]


def get_spaces(mov_level):
    spaces_per_phase = [
        (1, 1, 1),
        (1, 1, 2),
        (1, 2, 2),
        (2, 2, 2),
        (2, 2, 3),
        (2, 3, 3),
    ]
    return spaces_per_phase[mov_level]
