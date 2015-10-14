# -*- coding: utf-8 -*-

# --------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2015 Jonathan Labéjof <jonathan.labejof@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# --------------------------------------------------------------------

from os import walk, utime, makedirs
from os.path import (
    getmtime, getctime, expanduser, join, abspath, splitext, isdir, exists
)

from re import compile as re_compile

from shutil import copyfile

DEFAULT_IPATH = '.'  #: default input directory path.
DEFAULT_OPATH = 'organized'  #: default output directory path.
DEFAULT_PREFIX = 'organized'  #: default organized file prefix.


__all__ = ['mdateorganize']


def mdateorganize(
        ipath=DEFAULT_IPATH, opath=DEFAULT_OPATH, prefix=DEFAULT_PREFIX,
        regex=None, extensions=None, followlinks=False, keepname=False,
        overwrite=False
):
    """Organize files from a directory and sub-directories by modification date
    .

    :param str ipath: input path. Default is DEFAULT_IPATH.
    :param str opath: output path. Default is DEFAULT_OPATH.
    :param str prefix: prefix of organized file names. Default is
        DEFAULT_PREFIX.
    :param str regex: file name regex to organize.
    :param list extensions: file name extensions to organize.
    :param bool followlinks: follow links while pathing sub-directories.
    :param bool keepname: keep source file name in organized file.
    :param bool overwrite: if True (False by default) overwrite existing files.
    """

    path = abspath(expanduser(ipath))  # get input path

    opath = abspath(expanduser(opath))  # get output path

    try:
        makedirs(opath)
    except OSError:
        if not isdir(opath):
            raise

    # compile regex
    compiled_regex = None if regex is None else re_compile(regex)

    for dirname, _, files in walk(path, followlinks=followlinks):

        if dirname == opath:
            continue

        for name in files:

            filepath = join(dirname, name)  # get absolute file path
            _, extension = splitext(filepath)  # get file extension

            if extension:  # get extension
                extension = extension[1:]

            # check extension and regex
            if extensions is None or extension in extensions:
                if regex is None or compiled_regex.match(regex):

                    ctime = getctime(filepath)
                    mtime = getmtime(filepath)  # get modified time
                    # new filename is prefix
                    ofilename = '{0}-{1}'.format(prefix, mtime).replace(
                        '.', '_'
                    )

                    if keepname:  # add filename
                        ofilename = '{0}-{1}'.format(ofilename, name)

                    elif extension:  # add extension
                        ofilename = '{0}.{1}'.format(ofilename, extension)

                    newfilepath = join(opath, ofilename)  # get output filepath

                    if overwrite or not exists(newfilepath):  # copy file
                        copyfile(filepath, newfilepath)

                        times = ctime, mtime  # get output times
                        utime(newfilepath, times)  # set times
