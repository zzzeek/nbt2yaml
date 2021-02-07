from __future__ import absolute_import
from __future__ import print_function

import argparse
import os
import shutil
import sys
import tempfile

import editor

from . import compat
from . import dump_nbt
from . import dump_yaml
from . import parse_nbt
from . import parse_yaml
from .compat import BytesIO
from .compat import StringIO


def nbtedit():
    parser = argparse.ArgumentParser(
        description="Edit an nbt file in-place in yaml format."
    )
    parser.add_argument("filename", type=str, help="filename")
    parser.add_argument(
        "-n", "--no-gzip", action="store_true", help="Don't use gzip"
    )

    options = parser.parse_args()

    struct = parse_nbt(
        open(options.filename, "rb"), gzipped=not options.no_gzip
    )

    edit_file = tempfile.NamedTemporaryFile(
        delete=False, suffix=".yml", mode="w"
    )
    edit_file.write(dump_yaml(struct))
    edit_file.close()
    edit_filename = edit_file.name
    editor.edit(edit_filename)

    edit_file = open(edit_filename, "rb")
    new_struct = parse_yaml(edit_file)
    edit_file.close()
    os.remove(edit_filename)

    if new_struct == struct:
        sys.stderr.write("No changes made\n")
        sys.exit()

    save_counter = 0
    while True:
        if save_counter == 0:
            savefile = os.extsep.join([options.filename, "saved"])
        else:
            savefile = os.extsep.join(
                [options.filename, str(save_counter), "saved"]
            )
        if not os.path.exists(savefile):
            break
        save_counter += 1

    shutil.move(options.filename, savefile)
    sys.stderr.write("Saving old file as %s\n" % savefile)
    write_file = open(options.filename, "wb")
    sys.stderr.write("Writing %s\n" % options.filename)
    dump_nbt(new_struct, write_file, gzipped=not options.no_gzip)
    write_file.close()


def nbt2yaml():
    parser = argparse.ArgumentParser(
        description="Dump an nbt file or stream to yaml."
    )
    parser.add_argument(
        "filename",
        type=str,
        help="Filename.  Specify as '-' to read from stdin.",
    )
    parser.add_argument(
        "-n", "--no-gzip", action="store_true", help="Don't use gzip"
    )
    options = parser.parse_args()
    if options.filename == "-":
        if compat.py3k:
            in_ = sys.stdin.buffer
        else:
            in_ = sys.stdin
        input_ = BytesIO(in_.read())
    else:
        input_ = open(options.filename, "rb")

    try:
        struct = parse_nbt(input_, gzipped=not options.no_gzip)
        print(dump_yaml(struct))
    finally:
        input_.close()


def yaml2nbt():
    parser = argparse.ArgumentParser(
        description="Dump a yaml file or stream to nbt."
    )
    parser.add_argument(
        "filename",
        type=str,
        help="Filename.  Specify as '-' to read from stdin.",
    )
    parser.add_argument(
        "-n", "--no-gzip", action="store_true", help="Don't use gzip"
    )
    options = parser.parse_args()
    if options.filename == "-":
        input_ = StringIO(sys.stdin.read())
    else:
        input_ = open(options.filename, "rb")

    try:
        struct = parse_yaml(input_)

        if compat.py3k:
            out = sys.stdout.buffer
        else:
            out = sys.stdout
        dump_nbt(struct, out, gzipped=not options.no_gzip)
    finally:
        input_.close()
