from src.global_definition import *

class Optimizer:
    def __init__(self, file_path: str, directory: str):
        '''
        The Optimizer Initialize with a directory to store the files, function will make directory for you if the directory did not exist
        '''
        self.directory = directory
        self.file_path = file_path
        self.type = TYPE_OPTIMIZER
        self.temperature = 100
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

SIG_OPT_ACCEPT = 1
SIG_OPT_REJECT = 0

class user_Optimizer(Optimizer):

    def run(self, node_name:str):

        self.temperature *= 0.99

        commands = self.file_path, '-f', '{}/curr.blif'.format(self.directory), '-t', str(self.temperature), '-o', '{}/curr.blif'.format(self.directory), '-n', node_name

        # TODO: build the cpp process
        cpp_process = Popen(commands, stdin=PIPE, stdout=PIPE)
        stats = cpp_process.stdout.readline();
        ngain = cpp_process.stdout.readline();
        rewrite_node_name = cpp_process.stdout.readline();

        # TODO: get the information of gain
        print('---')
        print('currect network: ', stats)
        print('rewrite_node_name: ', rewrite_node_name)
        print('gain = ', ngain, 'Accept(1)? Reject(0)?')
        print('---')

        # TODO: wait the user's feed back
        input_signal = str(input())
        # ? Button
        # @param input() -> SIG

        signal = SIG_OPT_ACCEPT if input_signal is '1' else SIG_OPT_REJECT

        # TODO: pass the signal to the cpp process
        if signal is SIG_OPT_ACCEPT:
            cpp_process.stdin.write('1\n'.encode())
            cpp_process.stdin.flush()
        else:
            cpp_process.stdin.write('0\n'.encode())
            cpp_process.stdin.flush()
        cpp_process.wait()


class sa_Optimizer(Optimizer):

    def run(self, command: str):
        self.temperature *= 0.99
        sa_commands = self.file_path, '-f', '{}/curr.blif'.format(self.directory), '-t', str(self.temperature), '-o', '{}/curr.blif'.format(self.directory), '-r', command
        process = Popen(sa_commands)
        process.wait()

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
        process = Popen(abc_commands)
        process.wait()
    
    def undo(self):
        '''
        load prev.blif to curr.blif
        '''
        abc_commands = self.file_path, '-c', ';'.join([
            'read_blif {}/prev.blif'.format(self.directory),
            'write_blif {}/curr.blif'.format(self.directory)
        ])
        run(abc_commands)

