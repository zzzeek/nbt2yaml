========
nbt2yaml
========

Synopsis
========

nbt2yaml presents a Python parser/writer for Minecraft NBT files.   It then includes a system that can marshal
this format to/from Yaml files.   Finally, it provides simple shell commands to provide these transformations,
including ``editnbt``, which will shell out the Yaml version of the file to your editor of choice, allowing
easy command-line editing of NBT files.

NBT format:  http://www.minecraft.net/docs/NBT.txt
Yaml: http://www.yaml.org/

Installation
============

Install via pip is easiest::

    pip install http://bitbucket.org/zzzeek/nbt2yaml

Usage
=====

Once installed, the ``nbtedit`` command should be available::

    nbtedit --help

    nbtedit <file>

The script uses the standard ``EDITOR`` environment variable to determine which
text editor should be invoked.


