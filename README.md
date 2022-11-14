# NeXAS Switch script dumper/importer
### Modified from https://github.com/Yggdrasill-Moe/Niflheim/tree/master/NeXAS to support binu8 and datu8
</br>

### Only tested on Aquarium might require some modification for other games

</br>
</br>

## String dumper/importer for binu8 and datu8 files

### How to use
> Dump the game romfs, then copy the Script folder and Config folder to the root directory
> 
> Create Output/Script and Output/Config folder structure

```> python binu8_dumper.py```
> Extract the strings from Script folder binu8 files into .txt files

```> python binu8_importer.py```
>Create a new binu8 files based on the modified txt files and put them in the ./Output/Script/ folder

```> python datu8_dumper.py```
> Extract the strings from Config folder datu8 files into .txt files

```> python datu8_importer.py```
>Create a new datu8 files based on the modified txt files and put them in the ./Output/Config/ folder


### How to import the modified files into the game

> Create a Folder structure such as this
> 
> titleID > ModName > romfs
> 
> Example : 0100D11018A7E000\English Translation\romfs\
> Inside the folder structure replicate the original game folder structure and put your modified files in those folders
> 
> Example : 0100D11018A7E000\English Translation\romfs\Script\aqu_01_01.binu8


### Yuzu

> Put that folder inside %appdata%/yuzu/load/

### Ryujinx

> Put that folder inside %appdata%/Ryujinx/mods/contents/





