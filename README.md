# PyC4D_Helpers
A list of useful python functions and resources for Cinema4D. 
This repository aims to be a concentrated collection of useful scripts for common everyday C4D problems.
Hopefully at some point we won't have to dig into old posts in forums anymore.

Topics covered so far:
  - [UserData Handling (adding, removing, searching, setting)](https://github.com/GeorgeAdamon/pyc4d_helpers/tree/master/scripts/pyc4d_helpers)
  - [Material and Shader Creation](https://github.com/GeorgeAdamon/pyc4d_helpers/tree/master/scripts/pyc4d_helpers)
  - [Hierarchy Navigation (Selecting, Deselecting, Selecting Children etc)](https://github.com/GeorgeAdamon/pyc4d_helpers/tree/master/scripts/pyc4d_helpers)
  - [OBJ Sequential / Batch Importing](https://github.com/GeorgeAdamon/pyc4d_helpers/tree/master/scripts/ObjSequenceReader)
  - [Importing Transformation Matrices From Other Software](https://github.com/GeorgeAdamon/pyc4d_helpers/tree/master/src/standalone_scripts/RhinoMatrixLoader)

### Installation Notes
In order to be able to use the pyc4d_helpers functions inside Cinema4D, you need to Copy / Paste the **pyc4d_helpers** folder in: 

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

### Included Dependencies

* pyshull

```
pyshull.py : S-Hull Delaunay triangulation implemented in pure Python. Based on S-hull: a fast sweep-hull routine for Delaunay triangulation by David Sinclair. This implementation is 10-100 times slower than the reported results of S-HULL implemented in C.

earclipping.py : Based on Triangulation by Ear Clipping by David Eberly. Triangularisation of a simple polygon (no self intersections) with holes.

Tested on Python 2.7 and 3.4

Copyright (c) 2014-2016, Tim Sheerman-Chase

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
