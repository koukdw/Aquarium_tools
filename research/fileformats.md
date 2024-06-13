# Fileformats

## stringType
Make sure to select the correct stringType depending on your engine version/platform
```c
// encoding = utf-8
struct NexasStringSwitch {
    int32 size; // Size is only present in the switch version
    char str[]; // Null terminated
};

// Before aquarium PC 
// encoding = shift-jis
// After aquarium PC
// encoding = utf-8
struct NexasStringPC {
    char str[]; // Null terminated
};
```

## bin/binu8

```c

// Instruction are always occupy 8 bytes
struct NexasInstruction {
    int32 Opcode;
    int32 Operand;
};

struct NeXASBank {
    int32 id;                           // The id of the bank, used with the START instruction and also by some function for switching scripts/bank
    int32 argsIndex[8];                 // Index into bank_numeric_variables_names to get the name of the argument
    int32 defaultValue[8];              // Default value of that argument (probably if one isn't passed in)
};

struct NeXASFunction {
    int32 id;           // Id used by the Call instruction. You need to add the sign bit if you want to search for that function in the bytecode.
    int32 init_code_count;
    NexasInstruction init_code[init_code_count]
    int32 code_count;
    NexasInstruction code[code_count]
    int32 stringTable_count;
    NexasString stringTable[stringTable_count]
    int32 numeric_variable_count;
    NexasString local_numeric_variables_names[numeric_variable_count]
    int32 string_variable_count;
    NexasString local_string_variables_names[string_variable_count]
    int32 optionalPadding;
    byte pad[optionalPadding*68]
};

// Struct for bin and binu8
struct NeXASBin {
    // Those 3 fields only used in later version (After the release of Aquarium PC)
    char MAGIC[9]; // VER-1.00
    int32 unk_count; // always set to 1, maybe it's major version
    int32 unk[unk_count]; // always set to 0, maybe it's minor version

    // 2 code sections

    // 'init_code' isn't used alot so the size will most of the time be zero, when i saw it used it 
    //  was mostly for setting up variables i'm still not quite sure why it exist.

    // 'code' is where the main script is located
    int32 init_code_count;
    NexasInstruction init_code[init_code_count];
    int32 code_count;
    NexasInstruction code[code_count];

    // Remember to use the correct stringType and encoding for your platform
    // constant strings
    int32 stringTable_count;
    NexasString stringTable[stringTable_count];

    // Symbols for variables (int and string)
    int32 numeric_variable_count;
    NexasString bank_numeric_variables_names[numeric_variable_count];
    int32 string_variable_count;
    NexasString bank_string_variables_names[string_variable_count];

    // entrypoints parameters and default value
    int32 bank_count;
    NeXASBank banks[bank_count];

    // Read NexasFunction until end of file
    while( !FEof() ) {
        NeXASFunction func;
    }
};

struct NeXASGlobalBin {
    // Symbols for variables (int and string)
    int32 numeric_variable_count;
    NexasString global_numeric_variables_names[numeric_variable_count];
    int32 string_variable_count;
    NexasString global_string_variables_names[string_variable_count];

    // constant strings
    int32 stringTable_count;
    NexasString stringTable[stringTable_count];

    int32 code_count;
    NexasInstruction code[code_count];
}
```

## dat/datu8
Dat files all have similar structures but they don't reveal information about what their purpose are, so i'll list the actual names of the fields for the most common dat files below.
```c
struct NeXASDat {
    int32 element_count;
    // types is an array that contains a list of types encoded as integer
    // String = 1  Use correct string type
    // Int32 = 2
    // Int8 = 3
    // Int64 = 4
    // Int16 = 5
    // StringKey = 6  This is a key (which itself is a string) to a string defined in those .lngt files
    int32 types[element_count];

    // While the file isn't Eof read the types defined in the array in order
    void* csvFile[][];
    int32 col = 0;
    int32 row = 0;
    while( !FEof() ) {
        for(int col = 0; col < element_count; col++) {
            csvFile[row][col] = readType(types[col]);
        }
        row++;
    }

}
```
### System.dat
this file contains most configuration values but it's very big and change alot and i don't have any documentation on this.
### BGM.dat
```
0  -  fileName
1  -  musicName
2  -  loopPoint
3  -  volume
```
### char.dat
Note: `fontColor` is an index
```
0  -  name
1  -  font_color
2  -  voice_no
3  -  voice_volume
4  -  unknown_flag
5  -  facedef0
6  -  facedef1
7  -  facedef2
8  -  facedef3
9  -  facedef4
10 -  facedef5
11 -  facedef6
12 -  facedef7
```
### fontcolor.dat
Note: Color channel are mapped from 0 to 16 
```
0  -  name
1  -  unknown_name
2  -  red
3  -  green
4  -  blue
```
### fontresource.dat
```
0  -  file_name
1  -  font_name
```
### stand.dat
```
0  -  char_index
1  -  animation_name
2  -  face_name
3  -  x
4  -  y
5  -  spm_name
6  -  pattern_no
7  -  param1
8  -  param2
```
### standpos.dat
```
0  -  x
1  -  y
2  -  remove_flag
```
### visual.dat
```
0  -  red
1  -  green
2  -  blue
3  -  x_scroll_position
4  -  y_scroll_position
5  -  x_scroll_percent
6  -  y_scroll_percent
7  -  scale
8  -  file_name
9  -  diff_file_name
10 -  diff_x_position
11 -  diff_y_position
12 -  width
13 -  height
```
### event.dat
```
0  -  unknown
1  -  event_name
2  -  unknown1
3  -  unknown2
4  -  file_name
5  -  bank_number
6  -  unknown3
7  -  param0
8  -  param1
9  -  param2
10 -  param3
11 -  param4
12 -  param5
13 -  param6
14 -  param7
```
### eventtype.dat
Note: Maybe the unknown are color value since there's 3 of them and are always byte value
```
0  -  event_name
1  -  unknown
2  -  unknown1
3  -  unknown2
```
### cgmode.dat
Note: Each row with the same char_id just add a new box in the cg menu, then after column 1 starting with column 2,\
 it's a list of image index that will be in the same box
```
0  -  char_id
1  -  unknown
2  -  image_index
... repeat 2 until the end of the row
```
### key.dat
```
0  -  key_char
```
### keycommand.dat
Note: It's a list of flag value corresponding to various command it's pretty easy to figure them out i'll do that later not really the priority since it's pretty much useless since you can change those in the config menu
```
...  -  list_of_flags
```
### packlist.dat
Note: Just guessing\
type 0 = "Update",\
type 1 = "Data",\
type 2 = "Resource",\
type 3 = "Video"
```
0  -  pack_name
1  -  type
```
### systemvoice.dat
```
0  -  system_voice_id
1  -  chara_id
```
### systemvoicefilename.dat
Note: I'm not sure how it works
```
0  -  system_voice_filename
1  -  unknown0
2  -  unknown1
3  -  unknown2
4  -  unknown3
5  -  unknown4
6  -  unknown5
7  -  unknown6
8  -  unknown7
9  -  unknown8
10  -  unknown9
11  -  unknown10
12  -  unknown11
13  -  unknown12
14  -  unknown13
15  -  unknown14
```
### watchflg.dat
```
0  -  id
1  -  name
```
### watchsystemflg.dat
```
0  -  id
1  -  name
```
