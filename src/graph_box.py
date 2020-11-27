from src.node import *
from src.edge import *
import pygame.gfxdraw

class Graph_box:
    def __init__(self, left, top, width, height):
        # get the window DPI and set the size of box
        """
        root = tk.Tk()
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        """
        infoObject = pygame.display.Info()
        self.screen_width = infoObject.current_w
        self.screen_height = infoObject.current_h
        
        
        # initialize the window:
        self.width = width if type(width) is int else int(self.screen_width*width)
        self.height = height if type(height) is int else int(self.screen_height*height)       
        self.left = left if type(left) is int else int(self.screen_width*left)       
        self.top = top if type(top) is int else int(self.screen_height*top)
        self.position = self.left, self.top
        
        self.max_level = 10
        self.grid_size = max(1,int(self.height/self.max_level))
        self.node_size = int(self.height/self.max_level)/3
        self.area = 0
        self.moving_node = None
        self.endanger_node = None
        self.model_name = 'example'
        self.type = TYPE_GRAPH_BOX
        self.grid_memory = []

        self.node_type = NT_AND
        
        # nodes 
        self.nodes = []
        # connnections
        self.connnections = []

    def get_area(self):
        return self.area

    def on_key_down(self, key):
        return SIG_SYS_QUIT, None


    def paint(self, screen):
        """
        # paint background
        pygame.draw.rect(screen, BY, Rect(
            self.left-10, self.top-10, self.width+20, self.height+20))
        """
        # paint background of multiple colors
        pygame.gfxdraw.box(screen, pygame.Rect(
            0, 0, self.left - 20, self.screen_height), SB)

        pygame.gfxdraw.box(screen, pygame.Rect(
            self.left - 20, 0, self.width + 40, self.screen_height), BC)

        pygame.gfxdraw.box(screen, pygame.Rect(
            self.left + self.width + 20, 0, self.screen_width - (self.left + self.width + 10), self.screen_height), SB)

        # paint borders
        leg1_start, leg1_end = [
            (self.left - 20, 0),
            (self.left - 20, self.screen_height+10),
        ]
        pygame.draw.line(screen, GRAY, leg1_start, leg1_end, 1)

        leg2_start, leg2_end = [
            (self.left + self.width + 20, 0),
            (self.left + self.width + 20,self.screen_height+10)
        ]
        pygame.draw.line(screen, GRAY, leg2_start, leg2_end, 1)
        
        leg3_start, leg3_end = [
            (self.left + self.width , self.top),
            (self.left + self.width , self.top + self.height),
        ]
        pygame.draw.line(screen, GRAY, leg3_start, leg3_end, 1)
        

        # paint grid
        self.grid_size = max(1,int(self.height/self.max_level))
        grid_width = int(self.width/self.grid_size)
        grid_height = int(self.height/self.grid_size)
        for _ in range(grid_height+1):
            start, end = [
                (self.left, self.top+_*self.grid_size),
                (self.left+self.width, self.top+_*self.grid_size)
            ]
            pygame.draw.line(screen, GRAY, start, end, 1)
        for _ in range(grid_width+1):
            start, end = [
                (self.left+_*self.grid_size, self.top),
                (self.left+_*self.grid_size, self.top+self.height)
            ]
            pygame.draw.line(screen, GRAY, start, end, 1)
        """
        # paint boundary
        pygame.draw.rect(screen, GRAY, Rect(
            self.left-10, self.top-10, self.width+20, self.height+20), 1)
        """
        # paint connections
        for connection in self.connnections:
            connection.paint(screen, self.node_size)
        # paint nodes
        for node in self.nodes:
            node.paint(screen, self.node_size)

        # paint count board
        # pygame.draw.rect(screen, BB, Rect(
        #    self.left + self.width + 200, self.top - 10, 150, 200))
	
        pygame.gfxdraw.rectangle(screen, Rect(
            self.left + self.width + 110, self.top - 10, 350, 290),BB)
        pygame.gfxdraw.box(screen, pygame.Rect(
            self.left + self.width + 110, self.top - 10, 350, 290), BB)
        font_size = int(self.height*0.1)
        font1 = pygame.font.SysFont('comicsansmsttf', font_size)
        font2 = pygame.font.SysFont('comicsansmsttf', font_size*2)

	# number of nodes
        """
        text_rect1 = font2.render('{0}'.format(self.area), True, WHITE, None)
        if self.area < 10:
            position1 = self.left+self.width+240, self.top+70
        elif 9 < self.area < 100:
            position1 = self.left+self.width+200, self.top+70
        elif 99 <self.area < 1000:
            position1 = self.left+self.width+160, self.top+70
        elif  self.area >= 1000:
            position1 = self.left+self.width+120, self.top+70

        text_rect2 = font1.render('Nodes:', True, WHITE, None)
        position2 = self.left+self.width+180, self.top-20
	"""

	# area
        area = self.area
        for node in self.nodes:
            if node.logic is None or not node.logic:
                area -= 1
        text_rect3 = font2.render('{0}'.format(area), True, WHITE, None)
        if area < 10:
            position3 = self.left+self.width+240, self.top+70
        elif 9 < area < 100:
            position3 = self.left+self.width+200, self.top+70
        elif 99 <area < 1000:
            position3 = self.left+self.width+160, self.top+70
        elif  area >= 1000:
            position3 = self.left+self.width+120, self.top+70
        
        text_rect4 = font1.render('Area:', True, WHITE, None)
        position4 = self.left+self.width+180, self.top-20
		

        #screen.blit(text_rect1, position1)
        #screen.blit(text_rect2, position2)
        screen.blit(text_rect3, position3)
        screen.blit(text_rect4, position4)

    def zoom_to(self, level):
        self.max_level = level
        self.node_size = int(self.height/self.max_level)/3
        self.grid_size = max(1,int(self.height/self.max_level))
        # round it to the closest grid point
        for node in self.nodes:
            if node.position is [0, 0]:
                continue
            if node.grid_position is None:
                continue
            x, y = node.grid_position
            grid_position = [
                x*self.grid_size+self.left,
                y*self.grid_size+self.top
            ]
            node.position = node.x, node.y = grid_position

    def zoom_in(self):
        if self.max_level == 3:
            return
        self.zoom_to(self.max_level-1)

    def zoom_out(self):
        self.zoom_to(self.max_level+1)

    def add_node(self, position):
        node = Node(
            name = 'node{0}'.format(self.area),
            radius = self.node_size,
            position = position,
            node_type = self.node_type
        )

        # assign the grid position to the node
        x, y = position
        node.grid_position = (x-self.left)/self.grid_size, (y-self.top)/self.grid_size

        self.nodes.append(node)
        self.area += 1
        return node

    def add_empty_node(self):
        node = self.add_node(position=[0, 0])
        node.logic = None
        node.grid_position = None
        return node

    def delete_node(self, node):
        while len(node.edges) > 0:
            self.delete_connection(node.edges[0])
        if node in self.nodes:
            if len(node.edges) is 0:
                self.nodes.remove(node)
                self.area -= 1

    def add_connection(self, lower_node, higher_node):
        # priority: left > right
        lower_node.fanouts.append(higher_node)
        if higher_node.fanin_left == None:
            pin_index = 1
            higher_node.fanin_left = lower_node
        elif higher_node.fanin_right == None:
            pin_index = 2
            higher_node.fanin_right = lower_node
        else:
            return False
        edge = Edge(
            lower_node = lower_node,
            higher_node = higher_node,
            pin_index = pin_index
        )
        lower_node.edges.append(edge)
        higher_node.edges.append(edge)
        
        if higher_node.node_type == NT_AND:
            higher_node.logic = [1,1]
        if higher_node.node_type == NT_LN:
            higher_node.logic = [0,1]
        if higher_node.node_type == NT_RN:
            higher_node.logic = [1,0]
        if higher_node.node_type == NT_LRN:
            higher_node.logic = [0,0]

        if edge not in self.connnections:
            self.connnections.append(edge)
        return True
    
    def delete_connection(self, edge):
        if edge in self.connnections:
            self.connnections.remove(edge)
        if edge.lower_node is not None:
            edge.lower_node.edges.remove(edge)
            edge.lower_node.fanouts.remove(edge.higher_node)
        if edge.higher_node is not None:
            edge.higher_node.edges.remove(edge)
            if edge.pin_index == 1:
                edge.higher_node.fanin_left = None
            if edge.pin_index == 2:
                edge.higher_node.fanin_right = None
            if edge.higher_node.fanin_left is None and edge.higher_node.fanin_right is None:
                edge.higher_node.logic = None

    def assign_level(self, node):
        # if reached the leaf
        if node.logic is None:
            node.level = 0
            return 0
        node.level = max(
            self.assign_level(node.fanin_left),
            self.assign_level(node.fanin_right)
        )
        return node.level
    def assign_grid_position(self, node, current_location):
        '''
            find an empty place to store this node which is 
            the closest to current location
        '''
        # return if a node already got its position
        x, y = current_location
        if node.position != [0, 0]:
            return 
        if node.position == [0, 0]:
            # use BFS to find the next position
            queue_of_points = queue.Queue()
            trace_memory = []
            queue_of_points.put([x, y])
            trace_memory.append([x,y])
            while queue_of_points.empty() is False:
                point = x, y = queue_of_points.get()
                # if an empty point is found
                if point not in self.grid_memory:
                    node.grid_position = x, y
                    node.position = node.x, node.y = [
                        x*self.grid_size+self.left,
                        y*self.grid_size+self.top
                    ]
                    self.grid_memory.append( point )
                    break
                '''
                    Don't change the sequence here. If all of the surroundings are empty:
                        1. Down 2. Right 3. Left 4. Up
                '''
                if True:    # no restrictions on y max value
                    if [x,y+1] not in trace_memory:
                        queue_of_points.put([x,y+1])
                        trace_memory.append([x,y+1])
                if True:    # no restrictions on x max value
                    if [x+1,y] not in trace_memory:
                        queue_of_points.put([x+1,y])
                        trace_memory.append([x+1,y])
                if x > 1:   # x should be positive
                    if [x-1,y] not in trace_memory:
                        queue_of_points.put([x-1,y])
                        trace_memory.append([x-1,y])
                if y > 1:   # y should be positive
                    if [x,y-1] not in trace_memory:
                        queue_of_points.put([x,y-1])
                        trace_memory.append([x,y-1])
        # adjust the level if necessary
        if y > self.max_level:
            self.zoom_to(y)
        if x > self.max_level:
            self.zoom_to(x)
        '''
            set the value to the attributes and run the recursion
        '''
        if node.fanin_left is not None:
            self.assign_grid_position(node.fanin_left, [x-1,y+1])
        if node.fanin_right is not None:
            self.assign_grid_position(node.fanin_right, [x+1,y+1])

    def read_blif(self, filename):
        file = open(filename,'r')
        # clean up all the nodes:
        self.nodes.clear()
        self.connnections.clear()
        self.moving_node = None
        self.endanger_node = None
        # first run: initialize all nodes and logic
        nodes = {}
        outputs = []
        while True:
            line = file.readline().split()
            while line[-1] == '\\':
                line.pop()
                for word in file.readline().split():
                    line.append(word)
            if line[0] == '.inputs':
                for inputs in line[1:]:
                    if inputs not in self.nodes:
                        nodes[inputs] = self.add_empty_node()
            if line[0] == '.outputs':
                for output in line[1:]:
                    outputs.append(output)
            if line[0] == '.end':
                break
            if line[0] == '#':
                continue
            if line[0] == '.model':
                self.model_name = line[1]
            if line[0] == '.names':
                output = line[-1]
                # ignore the constants
                if len(line[1:]) is 1:
                    pass
                # add definition of node names
                if len(line[1:]) is 2 or len(line[1:]) is 3:
                    for node_name in line[1:]:
                        if node_name not in nodes:
                            nodes[node_name] = self.add_empty_node()
                if len(line[1:]) is 1:
                    pass
                if len(line[1:]) is 2:
                    nodes[output].logic = [ int(_) for _ in file.readline()[0] ]
                    if nodes[output].logic == [1]:
                        nodes[output].node_type = NT_AND
                    if nodes[output].logic == [0]:
                        nodes[output].node_type = NT_LRN
                # should be <0/1><0/1> 1
                if len(line[1:]) is 3:
                    nodes[output].logic = [ int(_) for _ in file.readline().split()[0] ]
                    if nodes[output].logic == [1,1]:
                        nodes[output].node_type = NT_AND
                    if nodes[output].logic == [0,1]:
                        nodes[output].node_type = NT_LN
                    if nodes[output].logic == [1,0]:
                        nodes[output].node_type = NT_RN
                    if nodes[output].logic == [0,0]:
                        nodes[output].node_type = NT_LRN
        # second run: initialize all the connections
        file.seek(0)
        while True:
            line = file.readline().split()
            while line[-1] == '\\':
                line.pop()
                for word in file.readline().split():
                    line.append(word)
            if line[0] == '.end':
                break
            elif line[0] == '.names':
                '''
                    There are 3 kinds of nodes:
                        1. constant: [IGNORE]
                        2. wire: [IGNORE]
                        3. wire:
                '''
                if len(line[1:]) is 1:
                    # set the logic to None
                    nodes[output].logic = None
                if len(line[1:]) is 2:
                    # add a wire
                    input_node, output = line[1:]
                    left = right = input_node
                    nodes[left].fanouts.append(nodes[output])
                    nodes[right].fanouts.append(nodes[output])
                    self.add_connection(nodes[left] , nodes[output])
                    self.add_connection(nodes[right], nodes[output])
                    nodes[output].fanin_left  = nodes[left]
                    nodes[output].fanin_right = nodes[right]
                    placeholder = file.readline()
                if len(line[1:]) is 3:
                    # add a AND node
                    left, right, output = line[1:]
                    nodes[left].fanouts.append(nodes[output])
                    nodes[right].fanouts.append(nodes[output])
                    self.add_connection(nodes[left] , nodes[output])
                    self.add_connection(nodes[right], nodes[output])
                    nodes[output].fanin_left  = nodes[left]
                    nodes[output].fanin_right = nodes[right]
                    placeholder = file.readline()
            else:
                continue
        file.close()
        # zoom to be able to host all the nodes
        graph_level = 0
        for output in outputs:
            # quit is output is deleted:
            if output not in nodes:
                continue
            root = nodes[output]
            graph_level = max(graph_level, self.assign_level(root))

        # assign position
        self.grid_memory = []
        for output in outputs:
            # quit is output is deleted:
            if output not in nodes:
                continue
            root = nodes[output]
            self.assign_grid_position(root, [2, 1]) # in the middle of first row

    def write_blif(self, filename):
        file = open(filename,'w')
        # set input and output
        inputs = []
        outputs = []
        nodes = []
        # label all inputs  
        for node in self.nodes:
            if node.fanin_right == None and node.fanin_left == None:
                if len(node.fanouts) == 0:
                    return False
                inputs.append(node.name)
            elif node.fanin_left != None and node.fanin_right != None:
                nodes.append(node)
            else:
                return False
            if len(node.fanouts) == 0:
                outputs.append(node.name)
        print('.model '+self.model_name, file=file)
        print('.inputs ' + ' '.join(inputs), file=file)
        print('.outputs ' + ' '.join(outputs), file=file)
        for node in nodes:
            print('.names ' 
                + node.fanin_left.name + ' '
                + node.fanin_right.name + ' '
                + node.name, file=file)
            if node.node_type is NT_AND:
                print('11 1', file=file)
            if node.node_type is NT_LN:
                print('01 1', file=file)
            if node.node_type is NT_RN:
                print('10 1', file=file)
            if node.node_type is NT_LRN:
                print('00 1', file=file)
        print('.end', file=file)
        file.close()

    def clear(self):
        # clear all nodes and connections
        self.nodes = []
        self.connnections = []
        self.area = 0

    def is_over(self, position):
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

    def on_left_down(self, position):
        # do nothing if out side the boundary
        if self.is_over(position) is False:
            return None
        x, y = position
        self.grid_size = max(1,int(self.height/self.max_level))
        # round it to the closest grid point
        grid_position = [
            round((x-self.left)/self.grid_size)*self.grid_size+self.left,
            round((y-self.top)/self.grid_size)*self.grid_size+self.top
        ]
        # if not empty then select that node
        for node in self.nodes:
            if node.is_over(position):
                self.moving_node = node
                node.highlight = True
                return 'Left Down: {0} is selected'.format(node.name)
        # if empty then create a new one
        new_node = self.add_node(grid_position)
        return 'Left Down: {0} is added'.format(new_node.name)

    def on_left_up(self, position):
        # do nothing if already none
        if self.moving_node is None:
            return
        x, y = position
        self.grid_size = max(1,int(self.height/self.max_level))
        # round it to the closest grid point
        grid_position = [
            round((x-self.left)/self.grid_size)*self.grid_size+self.left,
            round((y-self.top)/self.grid_size)*self.grid_size+self.top
        ]
        self.moving_node.move_to(grid_position)
        self.moving_node.highlight = False
        self.moving_node = None

    def on_right_down(self, position):
        # do nothing if out side the boundary
        if self.is_over(position) is False:
            return None
        # if not empty then select that node
        x, y = position
        self.grid_size = max(1,int(self.height/self.max_level))
        # round it to the closest grid point
        grid_position = [
            round((x-self.left)/self.grid_size)*self.grid_size+self.left,
            round((y-self.top)/self.grid_size)*self.grid_size+self.top
        ]
        for node in self.nodes:
            if node.is_over(grid_position):
                node.endanger = True
                self.endanger_node = node
                return 'Right Down: {0} is endanger'.format(node.name)
    
    def on_right_up(self, position):
        # do nothing if already none
        if self.endanger_node is None:
            return
        x, y = position
        self.grid_size = max(1,int(self.height/self.max_level))
        # round it to the closest grid point
        grid_position = [
            round((x-self.left)/self.grid_size)*self.grid_size+self.left,
            round((y-self.top)/self.grid_size)*self.grid_size+self.top
        ]
        for node in self.nodes:
            if node.is_over(grid_position):
                # if click on the same node then delete it
                if node.endanger == True:
                    node.endanger = False
                    message = 'Right Up: {0} is deleted'.format(node.name)
                    self.delete_node(node)
                    self.endanger_node = None
                    return message
                # if not clicking on the same node then link it
                self.endanger_node.endanger = False
                self.add_connection(
                    lower_node = self.endanger_node,
                    higher_node = node
                )
        self.endanger_node.endanger = False
        self.endanger_node = None

    def on_mouse_moving(self, position):
        x, y = position
        self.grid_size = max(1,int(self.height/self.max_level))
        # round it to the closest grid point
        grid_position = [
            round((x-self.left)/self.grid_size)*self.grid_size+self.left,
            round((y-self.top)/self.grid_size)*self.grid_size+self.top
        ]
        # initilize
        for node in self.nodes:
            node.highlight = False
            for _ in range(len(node.edges)):
                node.edges[_].highlight = False
        # light up if mouse is over that node
        for node in self.nodes:
            if node.is_over(grid_position):
                node.highlight = True
                for _ in range(len(node.edges)):
                    node.edges[_].highlight = True
        if self.moving_node is None:
            return
        self.moving_node.move_to(pygame.mouse.get_pos())

