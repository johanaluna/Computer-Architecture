
_Objetivo_: comprensión profunda de cómo funciona una CPU.

Esta es una computadora de 8 bits con direccionamiento de memoria de 8 bits.

### CPU de 8 bits
tiene 8 cables disponibles para direcciones (especificando donde esta algo en la memoria), cálculos e instrucciones. 

La CPU tiene un total de 256 bytes de memoria y solo puede calcular valores de hasta 255.
La CPU también podría soportar 256 instrucciones.

Ejecutaremos código que almacena el valor 8 en un registro, luego lo imprime:

```
# print8.ls8: Print the number 8 on the screen

10000010 # LDI R0,8
00000000
00001000
01000111 # PRN R0
00000000
00000001 # HLT
```

The binary numeric value on the left in the `print8.ls8` code above is either:

* the machine code value of the instruction (e.g. `10000010` for `LDI`), also
  known as the _opcode_

or

* one of the opcode's arguments (e.g. `00000000` for `R0` or `00001000` for the
  value `8`), also known as the _operands_.

Este código anterior requiere la implementación de tres instrucciones:

* `LDI`: carga, almacena un valor en un registro o  fija este registro en este valor.
* `PRN`: es una pseudo-instruction que imprime el valor numerico almacenado en un registro
* `HLT`: detiene la CPU y sale del emulator.

El programa anterior ya está codificado en el archivo fuente `cpu.py`. Para ejecutarlo: 
```
python3 ls8.py
```


## Step 1: Add the constructor to `cpu.py`

Agregue propiedades a la clase `CPU` para contener 256 bytes de memoria y 8 registros. 

Agregue propiedades para cualquier registro interno que necesite, p. `PC`, setting the initial value of the stack pointer.

## Step 2: Add RAM functions

En `CPU`, agregue el método` ram_read () `y` ram_write () `para acceder a la RAM
El objeto `CPU`.

`ram_read ()` debería aceptar la address para leer y devolver el valor almacenado allí.

`raw_write()` debería aceptar un valor para escribir, y la address para escribirlo.

> eEntro de la cpu CPU, hay dos internal registers usados para memory operations:
>>> the _Memory Address Register_ (MAR) and the _Memory Data Register_ (MDR). 


> MAR contiene la dirección que se está leyendo o escribiendo
> MDR continen los datos que se leyeron o los datos que se escribirán.

 You don't need to add the MAR or MDR to your `CPU` class, but they would make handy paramter names for
> `ram_read()` and `ram_write()`, if you wanted.

We'll make use of these helper function later.

Later on, you might do further initialization here, e.g. setting the initial
value of the stack pointer.

 ## Step 3: Implement the core of `CPU`'s `run()` method

This is the workhorse function of the entire processor. It's the most difficult part to write.

Necesita leer la dirección de memoria que está almacenada en el registro `PC`, 

y almacenar ese resultado en `IR`, el _Instruction Register_. Esto puede ser una variable local en `run ()`.

Some instructions requires up to the next two bytes of data _after_ the `PC` in memory to perform operations on. 

Sometimes the byte value is a register number,
other times it's a constant value (in the case of `LDI`). 

Using `ram_read()` read the bytes at `PC+1` and `PC+2` from RAM into variables `operand_a` and
`operand_b` in case the instruction needs them.

Luego, dependiendo del valor del código de operación, realice las acciones necesarias para cada instrucción según la especificación LS-8. 
Tal vez una cascada 'if-elif' ...? Hay otros
opciones, también.

Después de ejecutar el código para cualquier instrucción en particular, la `PC` necesita ser actualizada
para apuntar a la siguiente instrucción para la próxima iteración del bucle en `run ()`.
El número de bytes que usa una instrucción se puede determinar a partir de los dos bits altos
(bits 6-7) del código de operación de la instrucción. Vea la especificación LS-8 para más detalles.