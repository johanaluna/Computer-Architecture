import sys
import command

class MyClass:

    def __init__(self):
        self.create_branchtable()
    
    def create_branchtable(self):
        self.branchtable = {}
        filename = 'command.py'
        with open(filename) as f:
            for line in f:
                comment_split = line.split("=")
                command_name = comment_split[0].strip()
                command_value= comment_split[1].replace("\n","")

                name_function = 'handle_'+ command_name
                # getattr() let me to use a string as the name of a function 
                # I used (self, name_function) because my function is inside of the same class
                # then basically getattr(self, name_function) is equals self.handle_HLT or self.handle_LD
                # it's going to change depending of the command_name 
                function = getattr(self, name_function)  
                self.branchtable[int(command_value,2)] = function
    
    def handle_HLT(self):
        pass
    def handle_LD(self):
        pass
    def handle_LDI(self):
        pass
    def handle_MUL(self):
        pass
    def handle_POP(self):
        pass
    def handle_PRA(self):
        pass
    def handle_PRN(self):
        pass
    def handle_PUSH(self):
        pass
