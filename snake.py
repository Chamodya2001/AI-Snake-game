# snake.py

class Snake:
    def __init__(self, start_pos=(100, 100), block_size=20):
        self.block_size = block_size
        self.body = [start_pos]
        self.direction = (block_size, 0)
        self.grow_flag = False

    def move(self):
        head_x, head_y = self.body[-1]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.append(new_head)
        if not self.grow_flag:
            self.body.pop(0)
        else:
            self.grow_flag = False

    def grow(self):
        self.grow_flag = True

    def set_direction(self, direction):
        self.direction = direction

    def check_collision(self, width, height):
        head = self.body[-1]
        # Wall collision
        if head[0] < 0 or head[0] >= width or head[1] < 0 or head[1] >= height:
            return True
        # Self collision
        if head in self.body[:-1]:
            return True
        return False
