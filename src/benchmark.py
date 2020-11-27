from src.global_definition import *

class Benchmark:
    def __init__(self, left, top, width, height):
        # get the window DPI and set the size of box
        """
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        """
        infoObject = pygame.display.Info()
        screen_width = infoObject.current_w
        screen_height = infoObject.current_h
        
        
        # initialize the window:
        self.width = width if type(width) is int else int(screen_width*width) +20
        self.height = height if type(height) is int else int(screen_height*height)       
        self.left = left if type(left) is int else int(screen_width*left)- 20      
        self.top = top if type(top) is int else int(screen_height*top)
        self.position = self.left, self.top
        
        self.max_line = 1
        self.place_holder = ''
        self.input_buffer = self.place_holder
        self.text_buffer = ''
        self.type = TYPE_BENCHMARK

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
        paint the object
        '''
        font_size = self.height
        pygame.draw.rect(screen, GRAY, Rect(
            self.left, self.top, self.width, self.height), 2)
        pygame.gfxdraw.box(screen, pygame.Rect(
            self.left, self.top, self.width, self.height), PINK)
        offset = 0
        # paint all the text
        font = pygame.font.SysFont('comicsansmsttf', font_size-6)
        # font.set_bold(True)
        
        # paint text buffer
        text_rect = font.render(self.text_buffer, True, C, None)
        position = self.left, self.top+offset
        screen.blit(text_rect, position)
        offset += font_size
        
        # paint input buffer
        text_rect = font.render('{0}_'.format(
            self.input_buffer), True, WHITE, None)
        position = self.left, self.top+self.height-font_size
        screen.blit(text_rect, position)

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
        if key == pygame.K_RETURN:
            # parse the command
            command = self.store_buffer()
            font_size = int(self.height*0.1)
            font = pygame.font.SysFont('comicsansmsttf', font_size-5)
            text_rect2 = font.render(str(command), True, BY, None)
            return SIG_READ_FILE, command
        if key == pygame.K_BACKSPACE:
            self.input_buffer = self.input_buffer[:-1]
        else:
            self.input_buffer += pygame.key.name(key)

    # def insert_user(self, string):
    #     # reserve 1 line for the input display
    #     if len(self.text_buffer) == self.max_line-1:
    #         self.text_buffer = self.text_buffer[1:]
    #     self.text_buffer.append('user> '+string)

    def insert_text(self, string):
        # reserve 1 line for the input display
        if len(self.text_buffer) == self.max_line-1:
            self.text_buffer = self.text_buffer[1:]
        self.text_buffer.append(string)

    def insert_file(self, file):
        lines = file.readlines()
        for line in lines:
            self.insert_text(line[:-1]) # get rid of \n


    def store_buffer(self):
        command = self.input_buffer
        # self.insert_user(self.input_buffer)
        self.input_buffer = self.place_holder
        return command

