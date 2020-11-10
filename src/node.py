from src.global_definition import *

class Node(object):
    def __init__(self, name, position, radius, node_type):
        self.name = name
        # connections: fanin, fanout
        self.fanin_left = self.fanin_right = None
        self.fanouts = []
        self.edges = []
        self.logic = []
        self.x, self.y = self.position = position
        self.radius = radius
        self.highlight = False
        self.endanger = False
        self.level = None
        self.node_type = node_type

    def is_over(self, position):
        x, y = position
        if self.x < x-self.radius:
            return False
        if self.x > x+self.radius:
            return False
        if self.y < y-self.radius:
            return False
        if self.y > y+self.radius:
            return False
        return True

    def move_to(self, position):
        self.x, self.y = self.position = position

    def paint(self, screen, node_size):
        x, y = self.position
        # priority: red > white > gray
        if self.endanger is True:
            color = RED
        elif self.highlight is True:
            color = WHITE
        else:
            color = GRAY
        # paint input
        if self.fanin_left == None and self.fanin_right == None:
            pygame.draw.arc(screen, color, [x-node_size,y-node_size,node_size*2,node_size*2], 1.57*0, 1.57*2, 2)
            bot_start, bot_end = [
                (x-node_size,  y),
                (x+node_size,  y),
            ]
            pygame.draw.aaline(screen, color, bot_start, bot_end, 2)
            leg_start, leg_end = [
                (x,  y-node_size),
                (x,  y-node_size*1.75),
            ]
            pygame.draw.aaline(screen, color, leg_start, leg_end, 2)
            return

        # the and gate
        pygame.draw.arc(screen, color, [x-node_size,y-node_size,node_size*2,node_size*2], 1.57*0, 1.57*2, 2)
        points = [
            (x-node_size,  y),
            (x-node_size,  y+node_size),
            (x+node_size,  y+node_size),
            (x+node_size,  y)
        ]



        pygame.draw.aalines(screen, color, False, points, 2)
        leg1_start, leg1_end = [
            (x-node_size/2,  y+node_size),
            (x-node_size/2,  y+node_size*1.75),
        ]
        leg2_start, leg2_end = [
            (x+node_size/2,  y+node_size),
            (x+node_size/2,  y+node_size*1.75),
        ]
        leg3_start, leg3_end = [
            (x,  y-node_size),
            (x,  y-node_size*1.75),
        ]

        # the left not gate
        if self.node_type in [NT_LN, NT_LRN]:
            pygame.draw.circle(screen, color, [int(x-node_size/2),  int(y+node_size*1.25)], int(node_size*0.25), 1)
            # shorten the left leg
            leg1_start = (x-node_size/2, y+node_size*1.5)
        
        # the right not gate
        if self.node_type in [NT_RN, NT_LRN]:
            pygame.draw.circle(screen, color, [int(x+node_size/2),  int(y+node_size*1.25)], int(node_size*0.25), 1)
            # shorten the left leg
            leg2_start = (x+node_size/2, y+node_size*1.5)

        pygame.draw.aaline(screen, color, leg1_start, leg1_end, 2)
        pygame.draw.aaline(screen, color, leg2_start, leg2_end, 2)
        pygame.draw.aaline(screen, color, leg3_start, leg3_end, 2)
