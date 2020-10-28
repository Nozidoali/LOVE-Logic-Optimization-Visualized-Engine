# Logic Optimization Visualized Engine

## Getting Started
First, you need to make sure you have at least the following files ready under this folder:
```
    ./
        img/
            background.jpg
        src/
            button.py
            edge.py
            example.py
            global_definition.py
            graph_box.py
            mouse_cursor.py
            node.py
            opt_engine.py
            text_box.py
            user_interface.py
        main.py
        abc
        abc.rc
        requirement.txt
```

Then, you need to make sure your python version is above `python3` and you need to install the dependancies by running
```
    pip install -r requirement.txt
```

## Run Program
After installing packages using `pip`, you will be able to run the program by:
```
    python main.py
```

## Code Guide
The whole program starts from calling the main function in `main.py`
```python
    if __name__ == '__main__':
        '''
        main function
        '''
        # you need to define your UI
        ui = UI(
            background='img/b.png',
            version='3.0'
        )
```

Then serveral pre-defined objects are defined in `main.py`, for instance, the monitor:
```python
    # Add a monitor
    ui.add_object(Graph_box(left=0.05, top=0.05, height=0.85, width=0.57))
```

Those objects will be the components in the UI window and the whole UI loops while running by calling the function in `src/user_interface.py`
```python
    def run(self):
        '''
        the main function of UI
        '''
        while(True):
            signal = self.get_signal()
            self.parse_command(signal)
            self.paint()   
``` 

The function iteratively run the following command:  
1. get_signal(): listen to the events send by either mouse or keyboard and return the signal  
2. parse_command(): receive the signal send by user and react correspondingly  
3. paint(): update the window by re-painting each object   

## How to Contribute
The predefined objects consist of:  
1. Graph Box: the monitor of logic network  
2. Text Box: the Command Line Input (CLI)  
3. Button: 
4. Mouse Cursor: replace the mouse cursor with a new one  
5. Optimizer: the backend engine used to optimize the network  

To customize your own GUI, you can either **call ui.add_object()** or **implement your own object**. In the following 2 sub-sections, I will introduce you how to implement a new object

### Implement a simple object: Mouse Cursor

#### Step 1: Copy-Paste
To begin with, you need to create a file under `./src` called `mouse_cursor.py`, and copy-paste the definitions in `./src/example.py` as shown below:
```python
from src.global_definition import *

class Example(object):
    def __init__(self):
        self.type = TYPE_DEFAULT
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

    def on_key_down(self, key):
        pass
```
Keep in mind that you can only modify but not delete the functions above, since those are required in the `user_interface.py`. 


### Step 2: Modify initializing function
Now we first modify the initialize function:
```python
class Mouse_Cursor(object):
    def __init__(self):
        self.position = 0, 0
        self.type = TYPE_MOUSE_CURSOR
        # disable original mouse cursor
        pygame.mouse.set_visible(False)
        pass
```
We simply change the class name and add a `type` attribute for this object. And then, since the function of this object is to replace the original mouse cursor, you can disable (set invisible) the old mouse. Then, since the type name `TYPE_MOUSE_CURSOR` is not defined yet, we have to add something to `./src/global_definition`:
```python
...
    '''
    types
    '''
    TYPE_DEFAULT = -1
    TYPE_GRAPH_BOX = 0
    TYPE_TEXT_BOX = 1
    TYPE_BUTTON = 2
    TYPE_MOUSE_CURSOR = 3 # this line
    TYPE_OPTIMIZER = 4
...
```

### Step 3: Define Paint function
In this step, we define the paint function of our new mouse cursor. Why not change to a red circle?
```python
    def paint(self, screen):
        pygame.draw.circle(screen, RED, self.position, 25, 1)
```

### Step 4: Define Mouse Following funtion
To replace the old mouse cursor, we have to enable our mouse cursor to follow the trajectory of our mouse. To achieve that, we modify the function as below:
```python
    def on_mouse_moving(self, position):
        self.position = position
```

## Implement a complex object: Optimization Button

### Step 1: Create an object as before
Since I have already introduced how to define an object, we just skip this part. At the end of the day we should create a new file under `./src` called `button.py` and copy-paste the following code:
```python
from src.global_definition import *

class Button(object):
    def __init__(self, left, top, width, height,text):
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

        font_size = math.floor(self.height/3)
        pygame.draw.rect(screen, color, Rect(
            self.left, self.top, self.width, self.height), 2)
        font = pygame.font.SysFont('comicsansms', font_size)
        text_rect = font.render(self.text, True, color, None)
        position = self.left+self.width/3, self.top+self.height/3
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

    def on__key_down(self, key):
        pass
```

Please note that you can define your arguments of `__init__` function, it will not be a problem. In this example, I pass the position to the class, which is the location of that button, and the text to show.  

Then, I have modified the function `is_over()` so that it will return if a position is inside the button. This definition is very important for the correctness of `get_event()` function in `./src/user_interface.py`.  

At last, I defined the `paint()` function so that a button would be displayed on the screen.

By the way, do not forget to define the type name `TYPE_BUTTON` in `global_definition.py`

### Step 2: Define the function of that button
As a button, at least something should happen after clicking it, so we have to modify the function `on_left_down()` and `on_left_up()`. Here is the code:
```python
    def on_left_down(self, position):
        self.highlight = True

    def on_left_up(self, position):
        self.highlight = False
        return SIG_OPT, None
```

The attribute `self.highlight` is changed so that the color of this button will change to RED if clicked.  

The return value `SIG_OPT, None` is the key of functionality: this return value will be returned as `signal` and captured by the function `parse_command`. This return value should be a list consists of 2 elements:  
1.  Signal Name  
2.  list of arguments  

By the way, **please return the signal when left button is released, so that users can undo their clicking by dragging outside the button**.

### Step 3: Define your signal response
After sending a signal to the user interface, you have to define the reaction. Note that your reaction usually needs the participation of other object (graph box, text box, etc. ), you need to implement the function `parse_command` in `./src/user_interface.py`. Below is the code:
```python
...
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
                    # read the result
                    graph_box.read_blif('{}/curr.blif'.format(optimizer.directory))
...
```
This function will enumarate all the signals send by `get_event`, `command[0]` is the signal mentioned in previous section. Similar to type definition, we have to add the definition of signal `SIG_OPT` in `./src/global_definition.py`:
```python
...
'''
    signals
'''
SIG_SYS_QUIT = 0
PRINT_HELP = 1
SIG_WRITE_FILE = 2
SIG_READ_FILE = 3
SIG_OPT = 4 # < defined here
...
```

Then, you can catch this signal in `parse_command` and implement the function you want. Here, the button requests help from both `graph box` and `optimizer`, in order to write/read the network and run the optimization script. 