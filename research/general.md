# General Info

## Overview
Most of the info i gathered is the result of crossreferencing `Aonatsu line trial` and `Aonatsu line chinese trial` which the later is made in `Unity` and have the source code adapted to c#.\
This make it easy to compare the `bytecode` against the `source code` and check the difference granted it's not totally the same.\
Aonatsu line chinese trial contains various development left over like alot of `enums` that are also used in the c++ version, and the most important in my opinion function names.\
We also get a small view of how the engine might work but again it's not exactly the same.

### About Switch version
Until the release of `Deep One` decompiling the function handler for the NeXAS engine is very hard.\
This is because most of the code in that function is inlined and it's pretty much a huge switch statement so the code jump alot and this create alot of basic blocks and that's something IDA doesn't really like.\
That means you are kinda forced to change the block limit in IDA and restrict yourself to using the graph view.

### Scope
NeXAS engine support different scope (`local`, `global` and `script` wide)

### Types
the NeXAS vm support multiple types but as far as the script goes `int` and `string` are pretty much the only input.\
When a function return something else it will get automatically converted so i don't think we need to worry about this.

### Arrays
The original source code have arrays but in the bytecode those are just represented as normal variables 
ex: `array, array[1], array[2], array[3] etc..`

### Functions
there's 2 type of functions:
 * `built-ins` (native function implemented in the engine).
 * `script` (those functions are implemented in script and have their own sections in the binary file)

While we have the functions name for most of the built-ins, it's a bit harder to get them for the script functions.\
The script function can be `inlined`. \
When that happen the `Set_lineno` instruction will have the same value in the operand multiple time (Because functions dont use that instruction)


### Creating a new functions enum for other games
Since we have Aonatsu line enum which match perfectly with the pc trial version, we have a starting point.

That means we can compare other games with aonatsu line binary and compare various things (functions arity, functions parameter type and order),\
we can also check the inside of the function and check if it's similar, strings inside the binary also contains functions names in order for some part of the enums.

Also some functions will store the parameter value in a map of `string => value` where the string is the name of the parameter and the string being a std::string, so if you xref that string variable a few times you'll end up where the string is defined and get the parameter name