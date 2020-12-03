from src.global_definition import *
import pygame.gfxdraw

class Button(object):
    def __init__(self, left, top, width, height, text):

        infoObject = pygame.display.Info()
        screen_width = infoObject.current_w
        screen_height = infoObject.current_h
        
        
        # initialize the window:
        self.width = width if type(width) is int else int(screen_width*width)
        self.height = height if type(height) is int else int(screen_height*height)       
        self.left = left if type(left) is int else int(screen_width*left)       
        self.top = top if type(top) is int else int(screen_height*top)
        self.position = self.left, self.top

        self.type = TYPE_BUTTON
        self.highlight = False
        self.text = text
        

    def is_over(self, position):
        '''
        return if a position is covered in the object
        '''
        x, y = position
        if x < self.left:
            return False
        if x > self.left+self.width:
            return False
        if y < self.top:
            return False
        if y > self.top+self.height:
            return False
        return True

    def paint(self, screen):
        '''
        paint the object to a screen
        '''
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

    def on__key_down(self, key):
        pass
