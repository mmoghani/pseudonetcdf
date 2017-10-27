__all__ = ['getreader']

import unittest
import os
from warnings import warn
from PseudoNetCDF.netcdf import NetCDFFile

_readers = [('netcdf', NetCDFFile)]
def testreader(reader, *args, **kwds):
    try:
        reader(*args, **kwds)
        return True
    except:
        return False

def getreader(*args, format = None, **kwds):
    global _readers
    if not os.path.isfile(args[0]):
        warn('The first argument (%s) does not exist as a file.  First arguments are usually paths' % (args[0],))
    
    if format is None:
        _myreaders = _readers
    else:
        _myreaders = [(k, v) for k, v in _readers if format == k]
    
    for rn, reader in _myreaders:
        if getattr(reader, 'isMine', lambda *args, **kwds: testreader(reader, *args, **kwds))(*args, **kwds):
            return reader
    else:
        raise TypeError('No reader could open a file with these arguments %s %s' % (args, kwds))

def registerreader(name, reader):
    global _readers
    _readers.insert(0, (name, reader))

def pncopen(*args, format = None, addcf = True, **kwds):
    """
    Open any PNC supported format using args and kwds, which
    are format specific. format is not passed to the reader
    """
    reader =  getreader(*args, format = format, **kwds)
    outfile = reader(*args, **kwds)
    if addcf:
        try:
            from .conventions.ioapi import add_cf_from_ioapi
            add_cf_from_ioapi(outfile)
        except:
            pass
    return outfile

anyfile = pncopen

def getreaderdict():
    return dict(_readers)
    
class TestPNCOPEN(unittest.TestCase):
    def runTest(self):
        pass
    def setUp(self):
        pass
    def testPNCOPENFMT(self):
        import PseudoNetCDF.testcase
        for format, path in PseudoNetCDF.testcase.self_described_paths.items():
            print('Test open with ', format, path)
            f = pncopen(path, format = format)

    def testPNCOPENNOFMT(self):
        import PseudoNetCDF.testcase
        for format, path in PseudoNetCDF.testcase.self_described_paths.items():
            print('Test open unspecified ', path)
            f = pncopen(path)

