from src.global_definition import *

class Text_box:
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
        self.width = width if type(width) is int else int(screen_width*width) + 20
        self.height = height if type(height) is int else int(screen_height*height)       
        self.left = left if type(left) is int else int(screen_width*left) - 20      
        self.top = top if type(top) is int else int(screen_height*top)
        self.position = self.left, self.top
        
        self.max_line = 13
        self.text_buffer = [
            '=== Textbox Initialization ===',
            'Hi! This is {0}, ver: {1}'.format(GUI_NAME, VERSION),
            'The demo is successfully initialized.  ',
            'Now you can use the textbox  ',
        ]
        self.input_buffer = ''
        self.type = TYPE_TEXT_BOX

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

    def zoom_in(self):
        if 20 > self.max_line > 13:
            self.max_line -= 1

    def zoom_out(self):
        if 13< self.max_line < 20:
            self.max_line += 1

    def paint(self, screen):
        '''
        paint the object
        '''
        font_size = math.floor((self.height-70)/(self.max_line))+5
        pygame.draw.rect(screen, GRAY, Rect(
            self.left-10, self.top-10, self.width+20, self.height+20), 2)
        pygame.gfxdraw.box(screen, pygame.Rect(
            self.left-10, self.top-10, self.width+20, self.height+20), BB)
        offset = 0
        line_number = 0
        # paint all the text
        font = pygame.font.SysFont('microsoftsansserifttf', font_size-3)
        #font.set_bold(True)
        
        for text in self.text_buffer:
            text_rect = font.render('[{0}]  '.format(
                line_number)+text, True, C, None)
            position = self.left, self.top+offset
            screen.blit(text_rect, position)
            offset += font_size
            line_number += 1
        # paint input buffer
        text_rect = font.render('>>   {0}_'.format(
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
        elif key == pygame.K_RETURN:
            # parse the command
            command = self.store_buffer()
            if command == 'help':
                self.print_help()
            if command.startswith('write'):
                tokens = command.split(' ')
                if len(tokens) is not 2:
                    return None
                return SIG_WRITE_FILE, tokens[1]
            if command.startswith('read'):
                tokens = command.split(' ')
                if len(tokens) is not 2:
                    return None
                return SIG_READ_FILE, tokens[1]
            
        elif key == pygame.K_SPACE:
            self.input_buffer += ' '
        elif key == pygame.K_BACKSPACE:
            self.input_buffer = self.input_buffer[:-1]
        else:
            self.input_buffer += pygame.key.name(key)

    def insert_user(self, string):
        # reserve 1 line for the input display
        if len(self.text_buffer) == self.max_line-1:
            self.text_buffer = self.text_buffer[1:]
        self.text_buffer.append('user> '+string)

    def insert_text(self, string):
        # reserve 1 line for the input display
        if len(self.text_buffer) == self.max_line-1:
            self.text_buffer = self.text_buffer[1:]
        self.text_buffer.append(string)

    def insert_log(self, string):
        # reserve 1 line for the input display
        if len(self.text_buffer) == self.max_line-1:
            self.text_buffer = self.text_buffer[1:]
        self.text_buffer.append('  ::  '+string)

    def insert_file(self, file):
        lines = file.readlines()
        for line in lines:
            self.insert_text(line[:-1]) # get rid of \n

    def print_help(self):
        help_text = [
            '=== HELP TEXT ===',
            'Hi! Looking for help?',
            'Mouse Left: create a new node or drag an existing node',
            'Mouse Right: delete a node or drag to link two nodes',
            'Mouse Wheel: zoom in and out',
            'Keyboard ESC: exit the engine',
            'Run: start the optimization engine',
            'Undo: go back the optimization process for one step',
            'Clear: clear the whole node grid',
            'Benchmark: type a number from 1-20 to load the test file',
            'Please connect all the inputs before you RUN!'
        ]
        for text in help_text:
            self.insert_text(text)

    def store_buffer(self):
        command = self.input_buffer
        self.insert_user(self.input_buffer)
        self.input_buffer = ''
        return command

