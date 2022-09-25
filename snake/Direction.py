
class Direction:
    up = 1
    left = 2
    right = 3
    down = 4
    def go_left(current_direction):
        if(current_direction == Direction.left):
            return Direction.down
        if(current_direction == Direction.right):
            return Direction.up
        if(current_direction == Direction.up):
            return Direction.left
        if(current_direction == Direction.down):
            return Direction.right
    def go_right(current_direction):
        if(current_direction == Direction.left):
            return Direction.up
        if(current_direction == Direction.right):
            return Direction.down
        if(current_direction == Direction.up):
            return Direction.right
        if(current_direction == Direction.down):
            return Direction.left