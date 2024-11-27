

# Opcode table
This is mostly for relatively new version of the engine.
the early 2010 and earlier version have different opcodes

I am still not understanding opcode 0x49, but i have a few idea. It will be easier once i find a game where they actually use it.

**Important: All instruction increment the program counter by 1 including jump and branch. This mean Jump index are always 1 less than their actual value.**

| Opcode  (u32)| Mnemonic         | Operand  (u32)     | Description                |
| :----------- | :--------------  | :--------------    | :------------------------- |
| 0x0          | Val              | Value              | Set `R0` to value            |
| 0x4          | Push             | Register Number    | Push value at `registers[register_number]` into the stack |
| 0x5          | Param            | Type               | Add value at `R0` to the argument array |
|              |                  |                    | Type 0 is a `number`, `R0` contains the `number` |
|              |                  |                    | Type 1 is a `string`, `R0` contains an `index` into a stringArray then `GET_STRING(index)` |
|              |                  |                    | `Param_min` and `Param_max` instruction can be used after the `Param` instruction to mark the parameter to be bound checked when the call instruction is executed |
| 0x6          | Pop              | Register Number    | Pop value at the top of the stack into `registers[register_number]` |
| 0x7          | Call             | FunctionID & Arity | Call the function at `FunctionID` using the parameters from the arguments array |
|              |                  |                    | The operand is split into 2 u16 (`FunctionID` and `Arity`) in that order |
|              |                  |                    | If `FunctionID` doesn't have the sign bit set (the value is `positive or zero`) the call  instruction will call a `Native` function (implemented in the Engine) |
|              |                  |                    | If `FunctionID` does have the sign bit set (the value is `negative`) the call instruction will call a `Script` function (implemented in the .bin files) |
|              |                  |                    | If there's a return value it will be in `R0` |
| 0x8          | Load             | Register Number    | Load the value (`int` or `index to the string`) of a variable at index `registers[register_number]` into `registers[register_number]` |
|              |                  |                    | The register will contain an `index` to a `variable array` combined with an `optional flag` that determine if the scope is `global` |
|              |                  |                    | `registers[register_number] = GET_INT_VARIABLE(registers[register_number])` |
| 0x9          | Add              | Type               | Addition/Concat operation: |
|              |                  |                    | If type is 0 (`number`). `R0 = R0 + R1` |
|              |                  |                    | If type is 1 (`string`). It is an Concat operation, in that case both `R0` and `R1` contains an index to a string array (Variable or stringTable). |
|              |                  |                    | `str2 = GET_STRING(r0);` |
|              |                  |                    | `str1 = GET_STRING(r1);` |
|              |                  |                    | `ret_val = String::concat(str1, str2)` |
|              |                  |                    | `R0 = CREATE_TEMP_STRING_VARIABLE(0, ret_val)` |
| 0xA          | Sub              | None               | Subtraction operation: `R0 = R1 - R0` |
| 0xB          | Mul              | None               | Multiplication operation: `R0 = R0 * R1` |
| 0xC          | Div              | None               | Division operation: `R0 = R1 / R0` |
| 0xD          | Mod              | None               | Modulo operation: `R0 = R1 % R0` |
| 0xE          | Store            | Index              | Store a value (`int`/`string`) into a variable |
|              |                  |                    | We need 2 parameters the index and the value |
|              |                  |                    | There is 2 way to get them. |
|              |                  |                    | If `Operand` is -1 then `R0` will contain the `index` of the destination variable and `R1` will contains the `value` or the `index to the string` |
|              |                  |                    | Else the `operand` will be the `index` of the destination variable and `R0` will be the `value` or the `index to the string` |
|              |                  |                    | If `Index` >= 0 we get the `number` variable and set it to `value` |
|              |                  |                    | If `Index` is negative we get the `source `string using `GET_STRING(value)` and the `destination` string variable using `GET_STRING_VARIABLE(index ^ 0x80000000)` |
|              |                  |                    | We can then set the `destination` variable to the value of the `source` string |
| 0xF          | Or               | None               | Or operation: `R0 = R0 \|\| R1` |
| 0x10         | And              | None               | And operation: `R0 = R0 && R1` |
| 0x11         | Bit_Or           | None               | Bitwise Or operation: `R0 = R0 \| R1` |
| 0x12         | Bit_And          | None               | Bitwise And operation: `R0 = R0 & R1` |
| 0x13         | Xor              | None               | Xor operation: `R0 = R0 ^ R1` |
| 0x14         | Not              | None               | Not operation: `R0 = !R0` |
| 0x15         | Cmp_Le           | None               | Compare less or equal operation: `R0 = R0 <= R1` |
| 0x16         | Cmp_Ge           | None               | Compare greater or equal operation: `R0 = R0 >= R1` |
| 0x17         | Cmp_Lt           | None               | Compare less than operation: `R0 = R0 < R1` |
| 0x18         | Cmp_Gt           | None               | Compare greater than operation: `R0 = R0 > R1` |
| 0x19         | Cmp_Eq           | Type               | Compare equal operation: |
|              |                  |                    | If type is 0 (`number`) `R0 = R0 == R1` |
|              |                  |                    | If type is 1 (`string`). `R0 = Compare_String_Equal(R1, R0)` |
| 0x1A         | Cmp_Ne           | Type               | Compare not equal operation:  |
|              |                  |                    | If type is 0 (`number`) `R0 = R0 != R1` |
|              |                  |                    | If type is 1 (`string`). `R0 = Compare_String_NotEqual(R1, R0)` |
| 0x1B         | Start            | BankNumber         | Mark `entrypoints` or `banks` of the script, `BankNumber` can be used to search into the bank parameters array.|
|              |                  |                    | It is also used by some functions like : |
|              |                  |                    | LoadScript(scriptName, bankNumber, param...), |
|              |                  |                    | LoadEvent(eventNumber, param...),  scriptName, bankNumber and params defined in event.dat in that case |
|              |                  |                    | ChangeBank(bankNumber, param...), |
|              |                  |                    | CallScript(scriptName, bankNumber, param...), |
|              |                  |                    | CallBank(bankNumber, param...) |
| 0x1C         | End              | None               | Mark the end of the current bank |
| 0x1D         | Marker           | Value              | This is only used in the `main script` (those are probably autogenerated readmarker(so the game can track which marker have already been read and the game can stop at the unread lines, the number of readmarker as well as current readmarker is saved in Save\\Script.dat), everytime that instruction is executed it index into an array of byte with the value in the operand and set the value from 0 to 1 |
| 0x22         | Inc              | Index              | Increment the variable at index by 1 |
|              |                  |                    | If `Operand` is -1 then `R0` will contain the `index` of the variable |
|              |                  |                    | If `Operand` is positive then the operand will be the `index` of the variable |
| 0x23         | Dec              | Index              | Decrement the variable at index by 1 |
|              |                  |                    | If `Operand` is -1 then `R0` will contain the `index` of the variable |
|              |                  |                    | If `Operand` is positive then the operand will be the `index` of the variable |
| 0x2B         | Cmp_Zero         | None               | Compare zero operation: `R0 = R0 == 0` |
| 0x2C         | Set_lineno       | Value              | Set the `line number` of the current `statement`, only used in `main_script` |
|              |                  |                    | Note that when a `Script` function is inlined the same `line number` will repeat |
| 0x2D         | Sar              | None               | Shift Arithmetic Right operation: `R0 = R1 >> R0` |
| 0x2E         | Shl              | None               | Shift Logical Left operation: `R0 = R1 << R0` |
| 0x2F         | Shr              | None               | Shift Logical Right operation: `R0 = (u32)R1 >> R0` |
| 0x30         | Store.add        | Index              | Add/Append value to variable located at index |
|              |                  |                    | It works exactly like the store instruction, so please look at Store instruction for more details |
|              |                  |                    | if index >= 0 it's an number operation |
|              |                  |                    | `int_var = GET_INT_VARIABLE(index);` |
|              |                  |                    | `int_var += value` |
|              |                  |                    | if index < 0  it's an string operation |
|              |                  |                    | `right = GET_STRING(value);` |
|              |                  |                    | `left = GET_STRING_VARIABLE(index ^ 0x80000000);` |
|              |                  |                    | `string::append(left, right, 0, 0xFFFFFFFF);` |
| 0x31         | Store.sub        | Index              | Subtract `value` to variable located at `index`  |
|              |                  |                    | if operand == -1, `R0` contains the `index` and `R1` contains the `value` |
|              |                  |                    | if operand >= 0, `operand` contains the `index` and `R0` contains the `value` |
|              |                  |                    | `int_var = GET_INT_VARIABLE(index);` |
|              |                  |                    | `int_var += value` |
| 0x32         | Store.mul        | Index              | Multiply `value` to variable located at `index`  |
|              |                  |                    | if operand == -1, `R0` contains the `index` and `R1` contains the `value` |
|              |                  |                    | if operand >= 0, `operand` contains the `index` and `R0` contains the `value` |
|              |                  |                    | `int_var = GET_INT_VARIABLE(index);` |
|              |                  |                    | `int_var *= value` |
| 0x33         | Store.div        | Index              | Divide `value` to variable at `index` |
|              |                  |                    | if operand == -1, `R0` contains the `index` and `R1` contains the `value` |
|              |                  |                    | if operand >= 0, `operand` contains the `index` and `R0` contains the `value` |
|              |                  |                    | `if(value == 0) return ERROR` |
|              |                  |                    | `int_var = GET_INT_VARIABLE(index);` |
|              |                  |                    | `int_var /= value` |
| 0x34         | Store.mod        | Index              | Mod `value` to variable at `index` |
|              |                  |                    | if operand == -1, `R0` contains the `index` and `R1` contains the `value` |
|              |                  |                    | if operand >= 0, `operand` contains the `index` and `R0` contains the `value` |
|              |                  |                    | `if(value == 0) return ERROR` |
|              |                  |                    | `int_var = GET_INT_VARIABLE(index);` |
|              |                  |                    | `int_var %= value` |
| 0x35         | Store.or         | Index              | Or `value` to variable at `index` |
|              |                  |                    | if operand == -1, `R0` contains the `index` and `R1` contains the `value` |
|              |                  |                    | if operand >= 0, `operand` contains the `index` and `R0` contains the `value` |
|              |                  |                    | `int_var = GET_INT_VARIABLE(index);` |
|              |                  |                    | `int_var \|= value` |
| 0x36         | Store.and        | Index              | And `value` to variable at `index` |
|              |                  |                    | if operand == -1, `R0` contains the `index` and `R1` contains the `value` |
|              |                  |                    | if operand >= 0, `operand` contains the `index` and `R0` contains the `value` |
|              |                  |                    | `int_var = GET_INT_VARIABLE(index);` |
|              |                  |                    | `int_var &= value` |
| 0x37         | Store.xor        | Index              | Xor `value` to variable at `index` |
|              |                  |                    | if operand == -1, `R0` contains the `index` and `R1` contains the `value` |
|              |                  |                    | if operand >= 0, `operand` contains the `index` and `R0` contains the `value` |
|              |                  |                    | `int_var = GET_INT_VARIABLE(index);` |
|              |                  |                    | `int_var ^= value` |
| 0x38         | Store.sar        | Index              | Shift arithmetic right `value` to variable at `index` |
|              |                  |                    | if operand == -1, `R0` contains the `index` and `R1` contains the `value` |
|              |                  |                    | if operand >= 0, `operand` contains the `index` and `R0` contains the `value` |
|              |                  |                    | `int_var = GET_INT_VARIABLE(index);` |
|              |                  |                    | `int_var >>= value` |
| 0x39         | Store.shl        | Index              | Shift logical left `value` to variable at `index` |
|              |                  |                    | if operand == -1, `R0` contains the `index` and `R1` contains the `value` |
|              |                  |                    | if operand >= 0, `operand` contains the `index` and `R0` contains the `value` |
|              |                  |                    | `int_var = GET_INT_VARIABLE(index);` |
|              |                  |                    | `int_var <<= value` |
| 0x3A         | Store.shr        | Index              | Shift logical right `value` to variable at `index` |
|              |                  |                    | if operand == -1, `R0` contains the `index` and `R1` contains the `value` |
|              |                  |                    | if operand >= 0, `operand` contains the `index` and `R0` contains the `value` |
|              |                  |                    | `int_var = (u32)GET_INT_VARIABLE(index);` |
|              |                  |                    | `int_var >>= value` |
| 0x3F         | To_String        | Register Number    | Convert int `registers[register_num]` to string and return the variable index to `registers[register_num]` |
| 0x40         | Return           | Type               | Return the value, `R0` is the register that contains the return value, if the return type is a `string` a temp string variable is created and the index is set into `R0`, if it's just an `int` then nothing happen the value already in `R0` is the value that gets returned. |
|              |                  |                    | type 0 (`number`) |
|              |                  |                    | type 1 (`string`) |
| 0x41         | Jump             | Index              | Jump to code[index]        |
| 0x42         | Branch.false     | Index              | Branch to code[index] if `R0` is `false` (0) |
| 0x43         | Branch.true      | Index              | Branch to code[index] if `R0` is `true` (1) |
| 0x44         | To_Int           | Register Number    | Convert string register[register_num] to int and return the value to register[register_num] |
| 0x47         | Param_min        | None               | Mark the last parameter added for bound check (MINIMUM) when the function is executed, the value in the `R0` will be the value to compare against |
| 0x48         | Param_max        | None               | Mark the last parameter added for bound check (MAXIMUM) when the function is executed, the value in the `R0` will be the value to compare against |
| 0x49         | Param_flag       | None               | Add a special flag to the last parameter added when the function is executed, the value in the `R0` will be the value of the flag, the meaning of that flag depends on the function that gets executed, the most common one is to decide if the value should be added to the previous value or if it should replace the previous value ("+=" vs "=") |


To simplify the opcode table above, i'll list some pseudocode on the more complicated functions.

```c
int GET_INT_VARIABLE(int input) {
    int index = input;
    int* start;
    bool isValidIndex;
    // Check if the global flag is present (0x40000000)
    if ( (index & 0x40000000) != 0 )
    {
        // Set the global variable array to the start variable
        start = vm->global_variables.int.container.start;
        // Remove the global flag
        index = input ^ 0x40000000;
        // Check if the index is within the Array bounds
        isValidIndex = index < vm->global_variables.int.container.length;
    }
    else
    {
        // If callStack is not zero, it means we are in a function and we should get local variables instead
        if ( vm->callStack.size)
        {
            // If we are in the function just return the integer from the locals at that index
            // Simplified for the example, since it's full of c++ optimized template code
            return get_integer_local_variable(index);
        }
        // Set the script variable array to the start variable
        start = vm->bank_variables.int.container.start;
        // Check if the index is within the Array bounds
        isValidIndex = index < vm->bank_variables.int.container.length;

    }
  // Shouldn't happen
  if ( !isValidIndex )
    return ERROR;

  // return the number
  return &start[index];
}

string GET_STRING_VARIABLE(int input) {
  int index;
  string *start;
  int length;

  index = input;
  // Circular buffer of strings (length 4) used for return value by the Call, Add, Int_To_String conversion and Return Instruction 
  // Indexed from the end 
  // input is always a negative index
  // The pseudo code not very logical, but that's how it works (confirmed in the debugger)
  // Can't decipher the STL library optimization
  if ( input >= 0x7FFFFFFC ){                      
    return &vm->bank_variables.string.container.start[input + vm->bank_variables.string.container.length];
  }
  // Check if input have the global flag
  if ( (input & 0x40000000) != 0 )
  {
    start = vm->global_variables.string.container.start;
    // Remove the global flag
    index = input ^ 0x40000000;
    length = vm->global_variables.string.container.length
  }
  else
  {
    // If callStack is not zero, it means we are in a function and we should get local variables instead
    if ( vm->callStack.size )
    {
        // If we are in the function just return the string from the locals at that index
        // Simplified for the example, since it's full of c++ optimized template code
        return get_string_local_variable(index);
    }
    start = vm->bank_variables.string.container.start;
    length = vm->bank_variables.string.container.length
  }
  // Check if the index is within the Array bounds
  if ( index >= length )
    return ERROR
  // Return the string
  return &start[index];
}

string GET_STRING(int input) {
  // The sign bit tell get string that the input is a variable
  if ( input < 0 )
    return GET_STRING_VARIABLE(input ^ 0x80000000);
  if ( vm->callStack.size )
  {
    if ( input >= vm->current_function->string_table.length )
      return ERROR
    return vm->current_function->string_table.start[input];
  }
  else
  {
    start = vm->main_script->string_table.start;
    if ( input >= vm->main_script->string_table.length )
      return ERROR
    return &start[input];
  }
}

int CREATE_TEMP_STRING_VARIABLE(int index, string *str)
{
  if ( !index )
  {
    index = vm->rotatingStrBufferIndex;
    // Increment the rotating index
    vm->rotatingStrBufferIndex = index % 3 + 1;
  }
  string::assign(
    &vm->bank_variables.string.container.start[vm->bank_variables.string.container.length - index], // dest
    str,                                                                                            // src
    0,
    -1);
  return -index; // We negate so that GET_STRING know it's a variable
}
```
