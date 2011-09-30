import re
import glob
from nose.tools import *

import asciitable
if asciitable.has_numpy:
    import numpy as np

from test.common import has_numpy_and_not_has_numpy, has_numpy

@has_numpy_and_not_has_numpy
def test_read_normal(numpy):
    """Nice, typical fixed format table"""
    table = """
# comment (with blank line above)
|  Col1  |  Col2   |
|  1.2   | "hello" |
|  2.4   |'s worlds|
"""
    reader = asciitable.get_reader(Reader=asciitable.FixedWidth)
    dat = reader.read(table)
    print dat
    assert_equal(reader.header.colnames, ('Col1', 'Col2'))
    assert_almost_equal(dat[1][0], 2.4)
    assert_equal(dat[0][1], '"hello"')
    assert_equal(dat[1][1], "'s worlds")

@has_numpy_and_not_has_numpy
def test_read_normal_names(numpy):
    """Nice, typical fixed format table with col names provided"""
    table = """
# comment (with blank line above)
|  Col1  |  Col2   |
|  1.2   | "hello" |
|  2.4   |'s worlds|
"""
    reader = asciitable.get_reader(Reader=asciitable.FixedWidth,
                                   names=('name1', 'name2'))
#                                   include_names=('name1'))
    dat = reader.read(table)
    print dat
    assert_equal(reader.header.colnames, ('name1', 'name2'))
    assert_almost_equal(dat[1][0], 2.4)

@has_numpy_and_not_has_numpy
def test_read_normal_names_include(numpy):
    """Nice, typical fixed format table with col names provided"""
    table = """
# comment (with blank line above)
|  Col1  |  Col2   |  Col3 |
|  1.2   | "hello" |     3 |
|  2.4   |'s worlds|     7 |
"""
    reader = asciitable.get_reader(Reader=asciitable.FixedWidth,
                                   names=('name1', 'name2', 'name3'),
                                   include_names=('name1', 'name3'))
    dat = reader.read(table)
    print dat
    assert_equal(reader.header.colnames, ('name1', 'name3'))
    assert_almost_equal(dat[1][0], 2.4)
    assert_equal(dat[0][1], 3)

@has_numpy_and_not_has_numpy
def test_read_normal_exclude(numpy):
    """Nice, typical fixed format table with col name excluded"""
    table = """
# comment (with blank line above)
|  Col1  |  Col2   |
|  1.2   | "hello" |
|  2.4   |'s worlds|
"""
    reader = asciitable.get_reader(Reader=asciitable.FixedWidth,
                                   exclude_names=('Col1',))
    dat = reader.read(table)
    print dat
    # import pdb; pdb.set_trace()
    assert_equal(reader.header.colnames, ('Col2',))
    assert_almost_equal(dat[1][0], "'s worlds")

@has_numpy_and_not_has_numpy
def test_read_weird(numpy):
    """Weird input table with data values chopped by col extent """
    table = """
  Col1  |  Col2 |
  1.2       "hello" 
  2.4   sdf's worlds
"""
    reader = asciitable.get_reader(Reader=asciitable.FixedWidth)
    dat = reader.read(table)
    print dat
    assert_equal(reader.header.colnames, ('Col1', 'Col2'))
    assert_almost_equal(dat[1][0], 2.4)
    assert_equal(dat[0][1], '"hel')
    assert_equal(dat[1][1], "df's wo")
    
@has_numpy_and_not_has_numpy
def test_read_double(numpy):
    """Table with double delimiters"""
    table = """
|| Name ||   Phone ||         TCP||
|  John  | 555-1234 |192.168.1.10X|
|  Mary  | 555-2134 |192.168.1.12X|
|   Bob  | 555-4527 | 192.168.1.9X|
"""
    dat = asciitable.read(table, Reader=asciitable.FixedWidth, guess=False)
    print dat
    assert_equal(tuple(dat.dtype.names), ('Name', 'Phone', 'TCP'))
    assert_equal(dat[1][0], "Mary")
    assert_equal(dat[0][1], "555-1234")
    assert_equal(dat[2][2], "192.168.1.9")
    
@has_numpy_and_not_has_numpy
def test_read_no_header_autocolumn(numpy):
    """Table with no header row and auto-column naming"""
    table = """
|  John  | 555-1234 |192.168.1.10|
|  Mary  | 555-2134 |192.168.1.12|
|   Bob  | 555-4527 | 192.168.1.9|
"""
    dat = asciitable.read(table, Reader=asciitable.FixedWidth, guess=False,
                          header_start=None, data_start=0)
    print dat
    assert_equal(tuple(dat.dtype.names), ('col1', 'col2', 'col3'))
    assert_equal(dat[1][0], "Mary")
    assert_equal(dat[0][1], "555-1234")
    assert_equal(dat[2][2], "192.168.1.9")
    
@has_numpy_and_not_has_numpy
def test_read_no_header_names(numpy):
    """Table with no header row and with col names provided.  Second
    and third rows also have hanging spaces after final |."""
    table = """
|  John  | 555-1234 |192.168.1.10|
|  Mary  | 555-2134 |192.168.1.12|  
|   Bob  | 555-4527 | 192.168.1.9|  
"""
    dat = asciitable.read(table, Reader=asciitable.FixedWidth, guess=False,
                          header_start=None, data_start=0,
                          names=('Name', 'Phone', 'TCP'))
    print dat
    assert_equal(tuple(dat.dtype.names), ('Name', 'Phone', 'TCP'))
    assert_equal(dat[1][0], "Mary")
    assert_equal(dat[0][1], "555-1234")
    assert_equal(dat[2][2], "192.168.1.9")
    
