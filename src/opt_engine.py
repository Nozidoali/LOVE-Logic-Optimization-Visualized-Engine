from src.global_definition import *

class Optimizer:
    def __init__(self, file_path: str, directory: str):
        '''
        The Optimizer Initialize with a directory to store the files, function will make directory for you if the directory did not exist
        '''
        self.directory = directory
        self.file_path = file_path
        self.type = TYPE_OPTIMIZER
        self.temperature = 0
        if not os.path.exists(directory):
            os.mkdir(directory)


    def run():
        pass

    def undo():
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

class sa_Optimizer(Optimizer):

    def run(self, command: str):
        self.temperature *= 0.99
        sa_commands = self.file_path, '-f', '{}/curr.blif'.format(self.directory), '-t', str(self.temperature), '-o', '{}/curr.blif'.format(self.directory), '-r', command
        subprocess.run(sa_commands)

class abc_Optimizer(Optimizer):

    def run(self, command: str):
        '''
        1. store to prev.blif
        2. write to curr.blif
        '''
        abc_commands = self.file_path, '-c', ';'.join([
            'read_blif {}/curr.blif'.format(self.directory),
            'write_blif {}/prev.blif'.format(self.directory),
            'strash',
            command,
            'write_blif {}/curr.blif'.format(self.directory)
        ])
        subprocess.run(abc_commands)
    
    def undo(self):
        '''
        load prev.blif to curr.blif
        '''
        abc_commands = self.file_path, '-c', ';'.join([
            'read_blif {}/prev.blif'.format(self.directory),
            'write_blif {}/curr.blif'.format(self.directory)
        ])
        subprocess.run(abc_commands)
