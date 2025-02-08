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
    NexasInstruction init_code[init_code_count] // As far as i know functions don't have init_code so it's always empty you can skip those (size = 8 bytes * count).
    int32 code_count;
    NexasInstruction code[code_count]
    int32 stringTable_count;
    NexasString stringTable[stringTable_count]
    int32 numeric_variable_count;
    NexasString local_numeric_variables_names[numeric_variable_count]
    int32 string_variable_count;
    NexasString local_string_variables_names[string_variable_count]
    int32 bank_count;
    NeXASBank banks[bank_count]; // As far as i know functions don't have banks so it's always empty you can skip those (size = 68 bytes * count).
};

// Struct for bin and binu8
struct NeXASBin {
    // Those 3 fields only used in later version (After the release of Aquarium PC)
    NexasString MAGIC; // VER-1.00
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
### button.dat
```
0  -  offset_x
1  -  offset_y
2  -  range_unsure   // used with sliders
3  -  button_on_id;
4  -  button_off_id;
5  -  button_type
6  -  tooltip_text
```
### buttonex.dat
```
0  -  unk
1  -  unk1
2  -  unk2
3  -  unk3
4  -  unk4
5  -  offset_x
6  -  offset_y
7  -  range_unsure   // used with sliders
8  -  button_on_id;
9  -  button_off_id;
10  -  button_type
11  -  tooltip_text
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
3  -  face_pos_x
4  -  face_pos_y
5  -  spm_name
6  -  ano            // animation number ???
7  -  pattern        // default to -1
8  -  pattern_page   // default to -1
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

type could also be load_order where the lowest number get loaded last
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
```
0  -  system_voice_filename
1  -  system_voice_filename_variant
2  -  system_voice_filename_variant2
3  -  system_voice_filename_variant3
4  -  system_voice_filename_variant4
5  -  system_voice_filename_variant5
6  -  system_voice_filename_variant6
7  -  system_voice_filename_variant7
8  -  system_voice_filename_variant8
9  -  system_voice_filename_variant9
10  -  system_voice_filename_variant10
11  -  system_voice_filename_variant11
12  -  system_voice_filename_variant12
13  -  system_voice_filename_variant13
14  -  system_voice_filename_variant14
15  -  system_voice_filename_variant15
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

## SPM
```
struct SPMRect {
        int left;
        int top;
        int right;
        int bottom;   
};
struct SPMChipData {
        int imageNo;
        SPMRect dstRect;
        int chipWidth;
        int chipHeight;
        SPMRect srcRect;
        uint drawOption;
        uint drawOptionValue;
        int option;
        //byte unk5; // add for SPM 2.02
};
struct SPMPageData {
    	int numChipData;
	int pageWidth;
	int pageHeight;
	SPMRect pageRect;
	uint pageOption;
	int rotateCenterX;
	int rotateCenterY;
	uint hitFlag;
        local int i = 0;
        for( i = 0; i < 32; i++ ) {
	    if((1 << (1 & 31)) & hitFlag != 0){
                SPMRect hitRect[i];
                int unk0;
                int unk1;
                int unk2;
            }
        }
        //byte unk3;  // add for SPM 2.02
        SPMChipData chipData[numChipData];
        
};
struct SPMImageData {
        char imageName[];  
};
struct SPMPatData {
        int waitFrame;
        int pageNo[patPageNum];
};
struct SPMAnimData {
        char animName[];
        int numPat;
        int animRotateDirection;
        int animReverseDirection;
        local int num = numPat & 65535;
        SPMPatData patData[num];
};
struct SPMData {
        char spmVersion[];
        int numPageData;
        SPMPageData pageData[numPageData];
        int numImageData;
        SPMImageData imageData[numImageData];
        int patPageNum;
        int numAnimData;
        SPMAnimData animData[numAnimData];
};
```
