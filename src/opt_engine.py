from src.global_definition import *

class abc_Optimizer:
    def __init__(self, abc_path: str, directory: str):
        '''
        The Optimizer Initialize with a directory to store the files, function will make directory for you if the directory did not exist
        '''
        self.directory = directory
        self.abc_path = abc_path
        self.type = TYPE_OPTIMIZER
        if not os.path.exists(directory):
            os.mkdir(directory)

    def run(self, command: str):
        '''
        1. store to prev.blif
        2. write to curr.blif
        '''
        abc_commands = self.abc_path, '-c', ';'.join([
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
        abc_commands = self.abc_path, '-c', ';'.join[
            'read_blif {}/prev.blif'.format(self.directory),
            'write_blif {}/curr.blif'.format(self.directory)
        ]
        subprocess.run(abc_commands)

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
