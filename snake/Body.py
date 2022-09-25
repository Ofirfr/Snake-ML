from snake.Direction import Direction



class Body:
    body_parts =[(224, 256), (240, 256), (256, 256)] # body is list of pixels of the body, from tail to head
    direction = Direction.up
    fruit_eaten = False
    
    def update_body(self):
        if (self.fruit_eaten):  # Fruit eaten, dont delete tail
            self.fruit_eaten = False
        else:
            del self.body_parts[0]
        new_part_x, new_part_y = self.get_new_part()
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