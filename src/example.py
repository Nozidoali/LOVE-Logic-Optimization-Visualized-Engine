from src.global_definition import *

class Example(object):
    def __init__(self):
        self.type = TYPE_DEFAULT
        pass
        
    def is_over(self, position):
        return False

    def paint(self, screen):
        pass

    def on_left_down(self, position):
        pass

    def on_left_up(self, position):
        pass

    def on_right_down(self, position):
        pass

    def on_right_up(self, position):
        pass

    def on_mouse_moving(self, position):
        pass

    def on_key_down(self, key):
        pass