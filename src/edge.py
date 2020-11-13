from src.global_definition import *

class Edge(object):
    def __init__(self, lower_node, higher_node, pin_index):
        self.lower_node = lower_node
        self.higher_node = higher_node
        self.pin_index = pin_index # left: 1; right: 2
        self.highlight = False
        self.endanger = False

    def paint(self, screen, node_size):
        # figure out the position:
        lower_x, lower_y = self.lower_node.position
        lower_node_pos = [
            lower_x,  lower_y-node_size*1.75,
        ]
        higher_x, higher_y = self.higher_node.position
        if self.pin_index == 1:
            higher_node_pos = [
                higher_x-node_size/2,  higher_y+node_size*1.75,
            ]
        elif self.pin_index == 2:
            higher_node_pos = [
                higher_x+node_size/2,  higher_y+node_size*1.75,
            ]
        else:
            return
        # priority: red > white > gray
        if self.endanger is True:
            color = COLOR_EDGE_ENDANGER
        elif self.highlight is True:
            color = COLOR_EDGE_HIGHLIGHT
        else:
            color = COLOR_EDGE_NORMAL
        pygame.draw.line(screen, color, lower_node_pos, higher_node_pos, 1)