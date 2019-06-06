### ObjSequenceReader Installation Notes

#### Internal Dependencies
ObjSequenceReader needs the pyc4d_helpers scripts. [See how to install them.](https://github.com/GeorgeAdamon/pyc4d_helpers/blob/master/README.md#installation-notes)

#### External Dependencies
ObjSequenceReader scripts use the [pyshull](https://github.com/TimSC/pyshull) library, which is included in pyc4d_helpers.

### Usage
#### ObjSequenceReader_PythonGeneratorMode:
Create a Python Generator object and load the ObjSequenceReader_PythonGenerator script.
#### ObjSequenceReader_PythonTagMode:
Create a Null object, attach a Python Tag to it and load the ObjSequenceReader_PythonTag script.

### TO DO
* Add option to import separate objects present in the .obj file as separate c4d objects, instead of merging them into one mesh.
