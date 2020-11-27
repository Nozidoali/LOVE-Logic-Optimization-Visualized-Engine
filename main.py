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
    ui.add_object(Graph_box(left=0.105, top=0.062, height=0.85, width=0.516))

    # Add a shell 
    ui.add_object(Text_box(left=0.67, top=0.6, height=0.3, width=0.306))
    # Add benchmark input rect
    ui.add_object(Benchmark(left=0.9, top=0.49, height=0.056, width=0.055))
    """
    # Add count box
    ui.add_object(Count_box(left=0.81, top=0.06, height=0.3, width=0.15, text = str(ui.get_graph_box().area)))   
    """
    # Change the mouse cursor
    ui.add_object(Mouse_Cursor())

    # Add an backend engine
    ui.add_object(sa_Optimizer(file_path='./sa', directory='./tmp'))

    # Add Run button
    ui.add_object(Button(left=0.65, top=0.4, height=0.07, width=0.1, text = 'Run'))
    # Add Undo button
    ui.add_object(Button(left=0.65, top=0.49, height=0.07, width=0.1, text = 'Undo'))

    # Add clear button
    ui.add_object(Button(left=0.012, top=0.8, height=0.07, width=0.071, text = 'Clear'))
    
    # Add Benchmark button
    ui.add_object(Button(left=0.78, top=0.4, height=0.0897, width=0.2, text = 'Benchmark:'))
    ui.add_object(Button(left=0.78, top=0.49, height=0.07, width=0.2, text = '(1-20)'))
    
   
    # Add and button
    ui.add_object(Button(left=0.012, top=0.06, height=0.12, width=0.071, text = 'And'))
    # Add and_leftn button
    ui.add_object(Button(left=0.012, top=0.24, height=0.12, width=0.071, text = 'Leftn'))
    # Add and_rightn button
    ui.add_object(Button(left=0.012, top=0.42, height=0.12, width=0.071, text = 'Rightn'))
    # Add and_LRn button
    ui.add_object(Button(left=0.012, top=0.60, height=0.12, width=0.071, text = 'LRn'))

    
    ui.run()
    #print(pygame.font.get_fonts())
