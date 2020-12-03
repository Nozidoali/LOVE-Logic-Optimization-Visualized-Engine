# ! make sure you have abc in your directory
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
        abc/
            ...
            src/
            libabc.a
        Game/
            src/
            Makefile
        main.py
        bin/
            abc
            abc.rc
            sa
        requirement.txt
```
# ! check your dependencies
```
    pip install -r requirement.txt
```

# ! change to Game's diretory and run make
```
    cd Game
    make
    cd ..
```

# ! now you can run demo by
```
    python main.py
```

