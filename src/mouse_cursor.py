from src.global_definition import *

class Mouse_Cursor(object):
    def __init__(self):
        self.position = 0, 0
        self.type = TYPE_MOUSE_CURSOR
        # disable original mouse cursor
        pygame.mouse.set_visible(False)
        pass
        
    def is_over(self, position):
        return False

    def paint(self, screen):
        pygame.draw.circle(screen, RED, self.position, 25, 1)

    def on_left_down(self, position):
        pass

    def on_left_up(self, position):
        pass

    def on_right_down(self, position):
        pass

    def on_right_up(self, position):
        pass

    def on_mouse_moving(self, position):
        self.position = position

    