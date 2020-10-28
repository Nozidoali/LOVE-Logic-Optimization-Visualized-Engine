from src.user_interface import *

if __name__ == '__main__':
    '''
    main function
    '''
    # you need to define your UI
    ui = UI(
        background='img/b.png',
        version='3.0'
    )

    # Add a monitor
    ui.add_object(Graph_box(left=0.05, top=0.05, height=0.85, width=0.57))

    # Add a shell 
    ui.add_object(Text_box(left=0.67, top=0.6, height=0.3, width=0.32))

    # Change the mouse cursor
    ui.add_object(Mouse_Cursor())

    # Add an backend engine
    ui.add_object(abc_Optimizer(abc_path='./abc', directory='./tmp'))

    # Add a button
    ui.add_object(Button(left=0.65, top=0.05, height=0.15, width=0.15, text = 'Run'))
    
    ui.run()