from random import Random




FRUIT_COLOR = (0, 255, 0)
NO_FRUIT_LOCATION = (-1, -1)

rnd = Random()
class Fruits:
    
    fruit_ticker = rnd.randint(5, 15)
    fruit_exists = False
    current_fruit_location = NO_FRUIT_LOCATION

    def new_ticker(self):
        return rnd.randint(5, 15)

    # Updates fruit system, should be ran for every new frame
    def new_frame(self,snake_body_parts):
        if (self.fruit_ticker == 0 and not self.fruit_exists):
            self.new_fruit(snake_body_parts)
            return
        self.fruit_ticker -= 1

    def fruit_eaten(self):
        self.fruit_ticker = self.new_ticker()
        self.fruit_exists = False
        self.current_fruit_location = NO_FRUIT_LOCATION

    def new_fruit(self, snake_body):
        found_fruit_location = False
        from snake.Game import BODY_PART_SIZE, HEIGHT, WIDTH
        while (not found_fruit_location):
            test_location_x, test_location_y = rnd.randint(
                0, WIDTH/BODY_PART_SIZE-1)*BODY_PART_SIZE, rnd.randint(0, HEIGHT/BODY_PART_SIZE-1)*BODY_PART_SIZE
            if (test_location_x, test_location_y) not in snake_body:
                found_fruit_location = True
                self.current_fruit_location = (
                    test_location_x, test_location_y)
                self.fruit_exists = True
