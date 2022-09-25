import Direction
import pygame as pg

WIDTH, HEIGHT = 512, 512
WIN = pg.display.set_mode((WIDTH, HEIGHT))
BODY_COLOR = (255, 0, 0)
FRUIT_COLOR = (0, 255, 0)
BACKGROUND_COLOR = (0, 0, 0)
BODY_PART_SIZE = 16
FPS = 12
pg.display.set_caption("Snake")


class Snake:
    body = []  # body is list of pixels of the body, from tail to head
    direction = Direction.up

    def __init__(self):
        self.body = [(224, 256), (240, 256), (256, 256)]
        clock = pg.time.Clock()
        run = True
        while run:
            clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        self.direction = Direction.go_left(self.direction)
                    if event.key == pg.K_RIGHT:
                        self.direction = Direction.go_right(self.direction)

            self.draw_game()
            self.update_body()
            if (self.collisions_found()):
                run = False
                print("Collision found!")
        pg.quit()
    



    def update_body(self):
        del self.body[0]
        new_part_x, new_part_y = self.get_new_part()
        self.body.append((new_part_x, new_part_y))

    def get_new_part(self):
        head = self.body[-1]
        if (self.direction == Direction.right):
            return (head[0]+BODY_PART_SIZE, head[1])
        if (self.direction == Direction.left):
            return (head[0]-BODY_PART_SIZE, head[1])
        if (self.direction == Direction.down):
            return (head[0], head[1]+BODY_PART_SIZE)
        if (self.direction == Direction.up):
            return (head[0], head[1]-BODY_PART_SIZE)

    def collisions_found(self):
        head = self.body[-1]
        # Check if body part got out of bounds
        if (head[0]>WIDTH-BODY_PART_SIZE or head[0]<0 or head[1]>HEIGHT-BODY_PART_SIZE or head[1]<0):
            print("Out of bounds!")
            print("Head was at ",head)
            return True
        # Check if body part got over another body part
        counted_parts = set()
        for part in self.body:
            if part in counted_parts:
                print("Body parts collision")
                return True
            counted_parts.add(part)
        return False



    def draw_game(self):
        WIN.fill(BACKGROUND_COLOR)
        pixels = pg.PixelArray(WIN)
        for body_part in self.body:
            for x in range(1, BODY_PART_SIZE-1):
                for y in range(1, BODY_PART_SIZE-1):
                    pixels[body_part[0]+x, body_part[1]+y] = BODY_COLOR
        pixels.close()
        pg.display.update()