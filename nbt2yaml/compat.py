import sys

py3k = sys.version_info > (3,)

if py3k:
    long_ = int
else:
    long_ = long  # noqa F821


if py3k:
    from io import StringIO
    from io import BytesIO
else:
    from StringIO import StringIO  # noqa

    BytesIO = StringIO

if py3k:

    def u(s):
        return s

    def ue(s):
        return s

    def utf8unicode(s):
        assert isinstance(s, str)
        return s

    def utf8str(s):
        assert isinstance(s, str)
        return s


else:

    def u(s):
        return unicode(s, "utf-8")  # noqa

    def ue(s):
        return unicode(s, "unicode_escape")  # noqa

    def utf8unicode(s):
        return s.decode("utf-8")

    def utf8str(s):
        return s.encode("utf-8")


if py3k:
    range = range  # noqa A001
else:
    range = xrange  # noqa F821
