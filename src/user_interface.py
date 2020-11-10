from src.text_box import *
from src.graph_box import *
from src.count_box import *
from src.button import *
from src.mouse_cursor import *
from src.opt_engine import *

class UI(object):
    def __init__(self, background='img/background.jpg', version='unknown'
                    ):
        '''
        1. initialize the screen
        2. set the width and hight
        3. load the background image
        4. initialize all the elements
            - log textbox
            - network graphbox
        '''
        pygame.init()

        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.size = screen_width, screen_height

        #infoObject = pygame.display.Info()
        #self.size = infoObject.current_w, infoObject.current_h

        self.version = version
        self.screen = pygame.display.set_mode(self.size, flags = pygame.FULLSCREEN)
        self.background = pygame.image.load(background)
        pygame.display.set_caption('VE450 Demo: {0}'.format(self.version))
        """
        background = pygame.Surface(self.size)
        self.background = background.convert()
        self.background.fill(SB)
        """

        # objects
        self.objects = []

    def add_object(self, obj):
        '''
        add the object to UI:  
            1. Graph Box  
            2. Text Box  
            3. Button  
            4. Mouse Cursor  
            5. Optimizer  
            6. Count Box
        '''
        self.objects.append(obj)
    
    def get_graph_box(self):
        '''
        Find the first graph box to operate graph operations
        '''
        # find the prior graph box
        graph_box = None
        for obj in self.objects:
            if obj.type is TYPE_GRAPH_BOX:
                graph_box = obj
                break
        return graph_box

    def get_optimizer(self):
        '''
        Find the first graph box to operate graph operations
        '''
        # find the prior graph box
        optimizer = None
        for obj in self.objects:
            if obj.type is TYPE_OPTIMIZER:
                optimizer = obj
                break
        return optimizer

    def parse_command(self, command):
        '''
        parse the signal generated by 
        '''
        if command is None:
            return

        
        # SIG_SYS_QUIT
        if command[0] == SIG_SYS_QUIT:
            sys.exit()

        # SIG_WRITE_FILE
        if command[0] == SIG_WRITE_FILE:
            graph_box = self.get_graph_box()
            if graph_box is not None:
                graph_box.write_blif(command[1])

        # SIG_READ_FILE
        if command[0] == SIG_READ_FILE:
            graph_box = self.get_graph_box()
            if graph_box is not None:
                graph_box.read_blif(command[1])

        # SIG_OPT
        if command[0] == SIG_OPT:
            graph_box = self.get_graph_box()
            if graph_box is not None: 
                # optimizer
                optimizer = self.get_optimizer()
                if optimizer is not None:
                    # store the old network
                    graph_box.write_blif('{}/curr.blif'.format(optimizer.directory))
                    # run optimize
                    optimizer.run('compress2rs')
                    # clear area
                    graph_box.area = 0
                    # read the result
                    graph_box.read_blif('{}/curr.blif'.format(optimizer.directory))

        #SIG_CLR
        if command[0] == SIG_CLR:
            graph_box = self.get_graph_box()
            if graph_box is not None:
                # clear all nodes and connections
                graph_box.clear()
        
        #SIG_AND
        if command[0] == SIG_AND:
            graph_box = self.get_graph_box()
            graph_box.node_type = NT_AND

        #SIG_LEN
        if command[0] == SIG_LEN:
            graph_box = self.get_graph_box()
            graph_box.node_type = NT_LN

        #SIG_RIN
        if command[0] == SIG_RIN:
            graph_box = self.get_graph_box()
            graph_box.node_type = NT_RN

        #SIG_LRN
        if command[0] == SIG_LRN:
            graph_box = self.get_graph_box()
            graph_box.node_type = NT_LRN
                
    def get_signal(self):
        '''
        Update based on all the:
            1. mouse moving
            2. mouse actions
            3. keyboard actions

        Return the returned signal of the events
        '''

        '''
        # Step 1: handle the mouse moving event for all the objects
        '''
        mouse_position = pygame.mouse.get_pos()
        for obj in self.objects:
            obj.on_mouse_moving(mouse_position)

        '''
        # Step 2: handle the mouse clicking event and keyboard event for the selected objects
        '''
        # find the selected object that covers by the mouse
        selected_object = None
        for obj in self.objects:
            if obj.is_over(mouse_position):
                selected_object = obj
                break
        for event in pygame.event.get():
            # quit
            if event.type == pygame.QUIT:
                sys.exit()
            # mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN:
                if selected_object is None:
                    return None
                if event.button == 1:
                    # left botton
                    return selected_object.on_left_down(mouse_position)
                if event.button == 3:
                    # right botton
                    return selected_object.on_right_down(mouse_position)
                # scroll up
                if event.button == 4:
                    return selected_object.zoom_in()
                # scroll down
                if event.button == 5:
                    return selected_object.zoom_out()
            # mouse button up
            if event.type == pygame.MOUSEBUTTONUP:
                if selected_object is None:
                    return None
                if event.button == 1:
                    # left botton
                    return selected_object.on_left_up(mouse_position)
                if event.button == 3:
                    # right botton
                    return selected_object.on_right_up(mouse_position)
            # key board
            if event.type == pygame.KEYDOWN:
                if selected_object is None:
                    return None
                return selected_object.on_key_down(event.key)

    def paint(self):
        '''
        Paint all the elements on the screen, including:
            1. backgrond
            2. objects
        '''
        # background image
        if self.background is None:
            # fill with pure color if background image is not correct
            self.screen.fill([255, 255, 255])
        else:
            self.screen.blit(self.background, [0, 0])

        # objects
        for obj in self.objects:
            obj.paint(self.screen)

        pygame.display.flip()

    def run(self):
        '''
        the main function of UI
        '''
        while(True):
            signal = self.get_signal()
            self.parse_command(signal)
            self.paint()         
