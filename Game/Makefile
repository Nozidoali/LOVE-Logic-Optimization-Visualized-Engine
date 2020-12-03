CC = g++
CFLAG = 
TARGET = main

INC_DIR = ../abc/src
LIB_DIR = ../abc
SRC_DIR = ./src
OBJ_DIR = ./obj

INC = -I$(INC_DIR)
LIB =  -pthread -lm -L$(LIB_DIR) -labc -ldl -lreadline
SRC = ${wildcard $(SRC_DIR)/*.cpp}
OBJ = ${patsubst $(SRC_DIR)/%.cpp, $(OBJ_DIR)/%.o, $(SRC)}

.PHONY: all test clean

all: clean init $(TARGET) test

init:
	if [ ! -d "obj" ]; then mkdir obj; fi

clean:
	if [ -d "obj" ]; then rm -rf obj; fi
	if [ -d "*.out"]; then rm *.out; fi
	if [ -f $(TARGET)]; then rm $(TARGET); fi

	
$(TARGET) : $(OBJ)
	$(CC) $(CFLAG) $? -o $@ $(LIB) $(INC)

$(OBJ_DIR)/%.o : $(SRC_DIR)/%.cpp
	$(CC) $(CFLAG) -c $< -o $@ $(LIB) $(INC)
