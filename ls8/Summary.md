# Sumary

## Logical operators

logical operations are necessary because they can be used to model the way that information flows through electrical circuits, such as the circuits inside a CPU. These types of operations are called boolean operations.


## CPU
The Central Processing Unit handles all instructions it receives from hardware and software running on the computer.

In the CPU, there are two primary components.

* Mother board allows all the parts of the computer connect each other

* CU (control unit) - directs all the processors operations.
receive the instructions from ram and break into specific command for the other components example for the ALU

* ALU (arithmetic logic unit) - performs mathematical, logical(bitwise logic), and decision operations. and it set flag to let to the CU decide what to do with that flag 

* Registers are inside the cpu and acts as the ram, they are faster and more useful to store a number temporally 

* Cache is used by the (CPU) to reduce the average cost (time or energy) to access data from the main memory. A cache is a smaller, faster memory, closer to a processor core, which stores copies of the data from frequently used main memory locations.


* RAM (Random Access Memory) has all data that is being process by the cpu
  - RAm has addresses(ones and zeros 10001010)  whose contain data (ones and zeros 00101011) that can be instructions
    - load : a number from ram into cpu
    - add : two numbers together
    - store : a number from cpu back out to ram
    - compare : one number with another
    - jump : to another address in ram
    - out : put to anpther device in ram
    - in : put from a device such as a keyboard

* Bus is a group of wires that conect the components in the moder board

* Flags  is a wire that turn on/off depending of certain conditions are true 
  - There are 4 conditions in the flags
    A is Larger than B
    Equal
    B is Larger than B


After a compare instruction there is always jump 
need to say to the ram where to go to next piece of data 

  




Interrupt is a signal from a device attached to a computer or from a program within the computer that requires the operating system to *stop and figure out what to do next*

A single computer can perform only one computer instruction at a time. But, because it can be interrupted, it can take turns in which programs or sets of instructions that it performs. This is known as multitasking. 



# STACK
## PUSH
It inserts the data word at specified address to the top of the stack.
sp stack pointer

- decrement SP by 1
    SP <-- SP - 1 
- store the content of specified memory address 
- into SP; i.e, at top of stack
    SP <-- (memory address) 

## POP
 deleting one operand from the top of the stack and it increase the stack pointer register.
 It deletes the data word at the top of the stack to the specified address
- transfer the content of  SP (i.e, at top most data) 
- into specified memory location                   
    (memory address) <-- SP
- increment SP by 1
    SP <-- SP + 1 

# call stack 
is a stack data structure that stores information about the active subroutines of a computer program. 