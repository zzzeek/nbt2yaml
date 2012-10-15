import argparse
import sys
from nbt2yaml import parse_nbt, dump_yaml, parse_yaml, dump_nbt
import tempfile
import shutil
import StringIO
import os

def nbtedit():
    parser = argparse.ArgumentParser(description="Edit an nbt file in-place in yaml format.")
    parser.add_argument("filename", type=str, help="filename")
    parser.add_argument("-n", "--no-gzip",
                        action="store_true",
                        help="Don't use gzip"
                        )

    options = parser.parse_args()

    struct = parse_nbt(
                    open(options.filename, 'rb'),
                    gzipped=not options.no_gzip)
    try:
        editor = os.environ['EDITOR']
    except KeyError:
        sys.exit("Environment variable EDITOR is not set")

    edit_file = tempfile.NamedTemporaryFile(delete=False, suffix='.yml')
    edit_file.write(dump_yaml(struct))
    edit_file.close()
    edit_filename = edit_file.name
    os.system("%s %s" % (editor, edit_filename))


    edit_file = open(edit_filename, 'rb')
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
            savefile = os.extsep.join([options.filename, str(save_counter), "saved"])
        if not os.path.exists(savefile):
            break
        save_counter += 1

    shutil.move(options.filename, savefile)
    sys.stderr.write("Saving old file as %s\n" % savefile)
    write_file = open(options.filename, 'wb')
    sys.stderr.write("Writing %s\n" % options.filename)
    dump_nbt(new_struct, write_file, gzipped=not options.no_gzip)
    write_file.close()

def nbt2yaml():
    parser = argparse.ArgumentParser(description="Dump an nbt file or stream to yaml.")
    parser.add_argument("filename", type=str, help="Filename.  Specify as '-' to read from stdin.")
    parser.add_argument("-n", "--no-gzip",
                        action="store_true",
                        help="Don't use gzip"
                        )
    options = parser.parse_args()
    if options.filename == '-':
        input_ = StringIO.StringIO(sys.stdin.read())
    else:
        input_ = open(options.filename, 'rb')

    struct = parse_nbt(input_, gzipped=not options.no_gzip)
    print dump_yaml(struct)

def yaml2nbt():
    parser = argparse.ArgumentParser(description="Dump a yaml file or stream to nbt.")
    parser.add_argument("filename", type=str, help="Filename.  Specify as '-' to read from stdin.")
    parser.add_argument("-n", "--no-gzip",
                        action="store_true",
                        help="Don't use gzip"
                        )
    options = parser.parse_args()
    if options.filename == '-':
        input_ = StringIO.StringIO(sys.stdin.read())
    else:
        input_ = open(options.filename, 'rb')

    struct = parse_yaml(input_)
    dump_nbt(struct, sys.stdout, gzipped=not options.no_gzip)
