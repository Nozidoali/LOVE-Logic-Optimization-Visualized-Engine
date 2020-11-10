from src.user_interface import *

if __name__ == '__main__':
    '''
    main function
    '''
    # you need to define your UI
    ui = UI(
        background='img/background.jpg',
        version='3.0'
    )

    # Add a monitor
    #ui.add_object(Graph_box(left=0.05, top=0.06, height=0.85, width=0.57))
    ui.add_object(Graph_box(left=0.08, top=0.062, height=0.84, width=0.54))

    # Add a shell 
    ui.add_object(Text_box(left=0.66, top=0.6, height=0.3, width=0.32))
    """
    # Add count box
    ui.add_object(Count_box(left=0.81, top=0.06, height=0.3, width=0.15, text = str(ui.get_graph_box().area)))   
    """
    # Change the mouse cursor
    ui.add_object(Mouse_Cursor())

    # Add an backend engine
    ui.add_object(abc_Optimizer(abc_path='./abc', directory='./tmp'))

    # Add Run button
    ui.add_object(Button(left=0.65, top=0.06, height=0.1, width=0.1, text = 'Run'))

    # Add clear button
    ui.add_object(Button(left=0.65, top=0.25, height=0.1, width=0.1, text = 'Clear'))

    
   
    # Add and button
    ui.add_object(Button(left=0.01, top=0.05, height=0.09, width=0.05, text = 'And'))
    # Add and_leftn button
    ui.add_object(Button(left=0.01, top=0.20, height=0.09, width=0.05, text = 'Leftn'))
    # Add and_rightn button
    ui.add_object(Button(left=0.01, top=0.35, height=0.09, width=0.05, text = 'Rightn'))
    # Add and_LRn button
    ui.add_object(Button(left=0.01, top=0.50, height=0.09, width=0.05, text = 'LRn'))
    
    ui.run()
    #print(pygame.font.get_fonts())
