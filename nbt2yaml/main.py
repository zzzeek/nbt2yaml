import argparse
import sys
from nbt2yaml import parse_nbt, to_yaml
import tempfile
import shutil
import StringIO
import os

def nbtedit():
    parser = argparse.ArgumentParser(description="Edit an nbt file in-place in Yaml format.")
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

    edit_file = tempfile.NamedTemporaryFile(delete=False)
    edit_file.write(to_yaml(struct))
    edit_file.close()
    edit_filename = edit_file.name
    os.system("%s %s" % (editor, edit_filename))

    save_counter = 0
    while True:
        if save_counter == 0:
            savefile = os.extsep.join([options.filename, "saved"])
        else:
            savefile = os.extsep.join([options.filename, str(save_counter), "saved"])
        if not os.path.exists(savefile):
            break
        save_counter += 1

    shutil.copy(options.filename, savefile)
    #shutil.move(output, options.filename)
    os.remove(edit_filename)

def nbt2yaml():
    parser = argparse.ArgumentParser(description="Dump an nbt file or stream to yaml.")
    parser.add_argument("-f", "--file", type=str, help="Filename.  If omitted, file is read from stdin.")
    parser.add_argument("-n", "--no-gzip", 
                        action="store_true", 
                        help="Don't use gzip"
                        )
    options = parser.parse_args()
    if options.file:
        input_ = open(options.file, 'rb')
    else:
        input_ = StringIO.StringIO(sys.stdin.read())
    struct = parse_nbt(input_, gzipped=not options.no_gzip)
    print to_yaml(struct)

def yaml2nbt():
    parser = argparse.ArgumentParser(description="Dump a yaml file or stream to nbt.")
    parser.add_argument("-f", "--file", type=str, help="Filename.  If omitted, file is read from stdin.")
    parser.add_argument("-n", "--no-gzip", 
                        action="store_true", 
                        help="Don't use gzip"
                        )
    raise NotImplementedError()