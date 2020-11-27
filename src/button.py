from src.global_definition import *
import pygame.gfxdraw

class Button(object):
    def __init__(self, left, top, width, height, text):
        """
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        """
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

        color = RED if self.highlight else WHITE
        color_rec = RED if self.highlight else Ma
        font_size = math.floor(self.height/1.8)
        node_size = int(self.height/3.5)
        x, y = self.left + self.width/2 , self.top + self.height/2
        #pygame.draw.rect(screen, BB, Rect(
        #    self.left, self.top, self.width, self.height))
        #pygame.draw.rect(screen, BB, Rect(
        #   self.left, self.top, self.width, self.height),2)
        pygame.gfxdraw.rectangle(screen, Rect(
            self.left, self.top, self.width, self.height),color_rec)
        pygame.gfxdraw.box(screen, pygame.Rect(
            self.left, self.top, self.width, self.height), BB)
        
        """
        if (self.text == 'Count'):
            font1 = pygame.font.SysFont('comicsansms', font_size)
            font2 = pygame.font.SysFont('comicsansms', font_size*2)
            text_rect1 = font2.render('{0}'.format(self.text), True, WHITE, None)
            position1 = self.left+self.width+253, self.top+25
            text_rect2 = font1.render('Nodes', True, WHITE, None)
            position2 = self.left+self.width+233, self.top+105
            self.screen.blit(text_rect1, position1)
            self.screen.blit(text_rect2, position2)
        """
        
        if (self.text == 'And'):
            pygame.draw.arc(screen, color, [x-node_size,y-node_size,node_size*2,node_size*2], 1.57*0, 1.57*2, 3)
            points = [
                (x-node_size,  y),
                (x-node_size,  y+node_size),
                (x+node_size,  y+node_size),
                (x+node_size,  y)
            ]
            pygame.draw.lines(screen, color, False, points, 3)
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
            pygame.draw.line(screen, color, leg1_start, leg1_end, 3)
            pygame.draw.line(screen, color, leg2_start, leg2_end, 3)
            pygame.draw.line(screen, color, leg3_start, leg3_end, 3)

        elif (self.text == 'Leftn'):
            pygame.draw.arc(screen, color, [x-node_size,y-node_size,node_size*2,node_size*2], 1.57*0, 1.57*2, 3)
            points = [
                (x-node_size,  y),
                (x-node_size,  y+node_size),
                (x+node_size,  y+node_size),
                (x+node_size,  y)
            ]
            pygame.draw.circle(screen, color, [int(x-node_size/2),  int(y+node_size*1.25)], int(node_size*0.25), 2)

            pygame.draw.lines(screen, color, False, points, 3)
            leg1_start, leg1_end = [
                (x-node_size/2,  y+node_size*1.5),
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
            pygame.draw.line(screen, color, leg1_start, leg1_end, 3)
            pygame.draw.line(screen, color, leg2_start, leg2_end, 3)
            pygame.draw.line(screen, color, leg3_start, leg3_end, 3)
        
        elif (self.text == 'Rightn'):
            pygame.draw.arc(screen, color, [x-node_size,y-node_size,node_size*2,node_size*2], 1.57*0, 1.57*2, 3)
            points = [
                (x-node_size,  y),
                (x-node_size,  y+node_size),
                (x+node_size,  y+node_size),
                (x+node_size,  y)
            ]
            pygame.draw.circle(screen, color, [int(x+node_size/2),  int(y+node_size*1.25)], int(node_size*0.25), 2)

            pygame.draw.lines(screen, color, False, points, 3)
            leg1_start, leg1_end = [
                (x-node_size/2,  y+node_size),
                (x-node_size/2,  y+node_size*1.75),
            ]
            leg2_start, leg2_end = [
                (x+node_size/2,  y+node_size*1.5),
                (x+node_size/2,  y+node_size*1.75),
            ]
            leg3_start, leg3_end = [
                (x,  y-node_size),
                (x,  y-node_size*1.75),
            ]
            pygame.draw.line(screen, color, leg1_start, leg1_end, 3)
            pygame.draw.line(screen, color, leg2_start, leg2_end, 3)
            pygame.draw.line(screen, color, leg3_start, leg3_end, 3)

        elif (self.text == 'LRn'):
            pygame.draw.arc(screen, color, [x-node_size,y-node_size,node_size*2,node_size*2], 1.57*0, 1.57*2, 3)
            points = [
                (x-node_size,  y),
                (x-node_size,  y+node_size),
                (x+node_size,  y+node_size),
                (x+node_size,  y)
            ]
            pygame.draw.circle(screen, color, [int(x-node_size/2),  int(y+node_size*1.25)], int(node_size*0.25), 2)
            pygame.draw.circle(screen, color, [int(x+node_size/2),  int(y+node_size*1.25)], int(node_size*0.25), 2)

            pygame.draw.lines(screen, color, False, points, 3)
            leg1_start, leg1_end = [
                (x-node_size/2,  y+node_size*1.5),
                (x-node_size/2,  y+node_size*1.75),
            ]
            leg2_start, leg2_end = [
                (x+node_size/2,  y+node_size*1.5),
                (x+node_size/2,  y+node_size*1.75),
            ]
            leg3_start, leg3_end = [
                (x,  y-node_size),
                (x,  y-node_size*1.75),
            ]
            pygame.draw.line(screen, color, leg1_start, leg1_end, 3)
            pygame.draw.line(screen, color, leg2_start, leg2_end, 3)
            pygame.draw.line(screen, color, leg3_start, leg3_end, 3)
        
        elif (self.text == 'Run'):
            font = pygame.font.SysFont('comicsansmsttf', font_size)
            text_rect = font.render(self.text, True, color, None)
            position = self.left+self.width/3.5, self.top+self.height/6-3
            screen.blit(text_rect, position)

        elif (self.text == 'Undo'):
            font = pygame.font.SysFont('comicsansmsttf', font_size)
            text_rect = font.render(self.text, True, color, None)
            position = self.left+self.width/4, self.top+self.height/6-3
            screen.blit(text_rect, position)
        
        elif (self.text == 'Clear'):
            font = pygame.font.SysFont('comicsansmsttf', font_size)
            text_rect = font.render(self.text, True, color, None)
            position = self.left+10, self.top+self.height/6-3
            screen.blit(text_rect, position)
        elif (self.text == 'Benchmark:'):
            font = pygame.font.SysFont('comicsansmsttf', font_size-9)
            text_rect = font.render(self.text, True, color, None)
            position = self.left+40, self.top+self.height/6-3
            screen.blit(text_rect, position)
        elif (self.text == '(1-20)'):
            font = pygame.font.SysFont('comicsansmsttf', font_size-3)
            text_rect = font.render(self.text, True, color, None)
            position = self.left+40, self.top+self.height/6-6
            screen.blit(text_rect, position)
        else:
            font = pygame.font.SysFont('comicsansmsttf', font_size)
            text_rect = font.render(self.text, True, color, None)
            position = self.left+self.width/7, self.top+self.height/6
            screen.blit(text_rect, position)

    def on_left_down(self, position):
        self.highlight = True

    def on_left_up(self, position):
        self.highlight = False
        if (self.text == 'Run'):
            return SIG_OPT, None
        if (self.text == 'Undo'):
            return SIG_UNDO, None
        if (self.text == 'Clear'):
            return SIG_CLR, None
        if (self.text == 'And'):
            return SIG_AND, None
        if (self.text == 'Leftn'):
            return SIG_LEN, None
        if (self.text == 'Rightn'):
            return SIG_RIN, None
        if (self.text == 'LRn'):
            return SIG_LRN, None

    def on_right_down(self, position):
        pass

    def on_right_up(self, position):
        pass

    def on_mouse_moving(self, position):
        pass

    def on__key_down(self, key):
        pass
