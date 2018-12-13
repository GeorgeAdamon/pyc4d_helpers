
# Installation Notes
## pyc4d_helpers Scripts
### Installation
In order to be able to use the functions inside the Cinema4D Python Editor, you need to copy/paste the **pyc4d_helpers** folder in: 

* For versions prior to R20: *Your Cinema4D Preferences Folder* / library / python / packages / *your operating system*
* For R20 or later: *Your Cinema4D Preferences Folder* /python27/libs

Example R19: 
```
C:\Users\George\AppData\Roaming\MAXON\Cinema 4D R19_BFE04C39\library\python\packages\win64\
```
Example R20: 
```
C:\Users\George\AppData\Roaming\MAXON\Cinema 4D R20_4FA5020E\python27\libs
```

## OBJ Sequence Reader Scripts

### Internal Dependencies
ObjSequenceReader needs the pyc4d_helpers scripts. [See how to install them.](https://github.com/GeorgeAdamon/pyc4d_helpers/blob/master/scripts/README.md#installation)

### External Dependencies
ObjSequenceReader scripts need the [pyshull](https://github.com/TimSC/pyshull) library to be pasted in: *Your Cinema4D Preferences Folder* / library / python / packages / *your operating system*

### Usage
#### ObjSequenceReader_PythonGeneratorMode:
Create a Python Generator object and load the ObjSequenceReader_PythonGenerator script.
#### ObjSequenceReader_PythonTagMode:
Create a Null object, attach a Python Tag to it and load the ObjSequenceReader_PythonTag script.
