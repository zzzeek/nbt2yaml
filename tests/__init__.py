import contextlib
import gzip
import os


@contextlib.contextmanager
def datafile(name, ungzip=False):
    with open(
        os.path.join(os.path.dirname(__file__), "files", name), mode="rb"
    ) as f:

        if ungzip:
            with gzip.GzipFile(fileobj=f) as gz:
                yield gz
        else:
            yield f


def eq_(a, b):
    assert a == b, "%r != %r" % (a, b)


def file_as_bytes(name, ungzip=False):
    with datafile(name, ungzip=ungzip) as file_:
        return file_.read()


def file_as_string(name, ungzip=False):
    with open(
        os.path.join(os.path.dirname(__file__), "files", name), mode="r"
    ) as f:
        return f.read()
