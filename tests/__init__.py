import os
import gzip

def datafile(name, ungzip=False):
    f = open(os.path.join(os.path.dirname(__file__), 'files', name))
    if ungzip:
        f = gzip.GzipFile(fileobj=f)
    return f

def eq_(a, b):
    assert a == b, "%r != %r" % (a, b)