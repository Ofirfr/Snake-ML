from snake.Direction import Direction

MAX_STEPS = 200
OUT_OF_BOUNDS = -100
BODY_PART_COLLISION = -100
TOO_MANY_STEPS = -500
REWARD_PER_STEP = 1


class Body:

    def __init__(self):
        # body is list of pixels of the body, from tail to head
        self.body_parts = [(196, 256),(208, 256),(224, 256), (240, 256), (256, 256)]
        self.direction = Direction.up
        self.remaining_steps = MAX_STEPS
        self.fruit_eaten = False

    def update_body(self):
        if (self.fruit_eaten):  # Fruit eaten, dont delete tail
            self.fruit_eaten = False
        else:
            del self.body_parts[0]
        new_part_x, new_part_y = self.get_new_part()
        self.remaining_steps -= 1
        self.body_parts.append((new_part_x, new_part_y))

    def get_new_part(self):
        from snake.Game import BODY_PART_SIZE
        head = self.body_parts[-1]
        if (self.direction == Direction.right):
            return (head[0]+BODY_PART_SIZE, head[1])
        if (self.direction == Direction.left):
            return (head[0]-BODY_PART_SIZE, head[1])
        if (self.direction == Direction.down):
            return (head[0], head[1]+BODY_PART_SIZE)
        if (self.direction == Direction.up):
            return (head[0], head[1]-BODY_PART_SIZE)

    def go_left(self):
        self.direction = Direction.go_left(self.direction)

    def go_right(self):
        self.direction = Direction.go_right(self.direction)

    def calc_reward(self):
        head = self.body_parts[-1]
        from snake.Game import BODY_PART_SIZE, HEIGHT, WIDTH
        # Check if body part got out of bounds
        if (head[0] > WIDTH-BODY_PART_SIZE or head[0] < 0 or head[1] > HEIGHT-BODY_PART_SIZE or head[1] < 0):
            return OUT_OF_BOUNDS
        # Check if body part got over another body part
        counted_parts = set()
        for part in self.body_parts:
            if part in counted_parts:
                return BODY_PART_COLLISION
            counted_parts.add(part)
        if self.remaining_steps <= 0:
            return TOO_MANY_STEPS
        return REWARD_PER_STEP
