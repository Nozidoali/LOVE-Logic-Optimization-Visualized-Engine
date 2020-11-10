from src.global_definition import *

class Count_box:
    def __init__(self, left, top, width, height, text):
        # get the window DPI and set the size of box
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        """
        infoObject = pygame.display.Info()
        screen_width = infoObject.current_w
        screen_height = infoObject.current_h
        """
        
        # initialize the window:
        self.width = width if type(width) is int else int(screen_width*width)
        self.height = height if type(height) is int else int(screen_height*height)       
        self.left = left if type(left) is int else int(screen_width*left)    
        self.top = top if type(top) is int else int(screen_height*top)
        self.position = self.left, self.top

        self.text = text

        self.type = TYPE_COUNT_BOX

    def is_over(self, position):
        return False

    def zoom_in(self):
        pass

    def zoom_out(self):
        pass

    def paint(self, screen):
        '''
        paint the object
        '''
        font_size = math.floor(self.height/4)
        pygame.draw.rect(screen, C, Rect(
            self.left-10, self.top-10, self.width+20, self.height+20), 3)

        font1 = pygame.font.SysFont('comicsansms', font_size)
        font2 = pygame.font.SysFont('comicsansms', font_size*2)
        text_rect1 = font2.render('{0}'.format(self.text), True, WHITE, None)
        position1 = self.left+self.width+253, self.top+25
        text_rect2 = font1.render('Nodes', True, WHITE, None)
        position2 = self.left+self.width+233, self.top+105
        screen.blit(text_rect1, position1)
        screen.blit(text_rect2, position2)

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
        if key == pygame.K_ESCAPE:
            sys.exit()