# -*- coding: utf-8 -*-
#
#  Copyright 2011 Sybren A. Stüvel <sybren@stuvel.eu>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
'''Large file support

    - break a file into smaller blocks, and encrypt them, and store the
      encrypted blocks in another file.

    - take such an encrypted files, decrypt its blocks, and reconstruct the
      original file.

The encrypted file format is as follows, where || denotes byte concatenation:

    FILE := VERSION || BLOCK || BLOCK ...

    BLOCK := LENGTH || DATA

    LENGTH := varint-encoded length of the subsequent data. Varint comes from
    Google Protobuf, and encodes an integer into a variable number of bytes.
    Each byte uses the 7 lowest bits to encode the value. The highest bit set
    to 1 indicates the next byte is also part of the varint. The last byte will
    have this bit set to 0.

This file format is called the VARBLOCK format, in line with the varint format
used to denote the block sizes.

'''

VARBLOCK_VERSION = 1

def read_varint(infile):
    '''Reads a varint from the file.

    When the first byte to be read indicates EOF, (0, 0) is returned. When an
    EOF occurs when at least one byte has been read, an EOFError exception is
    raised.

    @param infile: the file-like object to read from. It should have a read()
        method.
    @returns (varint, length), the read varint and the number of read bytes.
    '''

    varint = 0
    read_bytes = 0

    while True:
        char = infile.read(1)
        if len(char) == 0:
            if read_bytes == 0:
                return (0, 0)
            raise EOFError('EOF while reading varint, value is %i so far' %
                    varint)

        byte = ord(char)
        varint += (byte & 0x7F) << (7 * read_bytes)

        read_bytes += 1

        if not byte & 0x80:
            return (varint, read_bytes)


def write_varint(outfile, value):
    '''Writes a varint to a file.

    @param outfile: the file-like object to write to. It should have a write()
        method.
    @returns the number of written bytes.
    '''

    # there is a big difference between 'write the value 0' (this case) and
    # 'there is nothing left to write' (the false-case of the while loop)

    if value == 0:
        outfile.write('\x00')
        return 1

    written_bytes = 0
    while value > 0:
        to_write = value & 0x7f
        value = value >> 7

        if value > 0:
            to_write |= 0x80

        outfile.write(chr(to_write))
        written_bytes += 1

    return written_bytes


def yield_varblocks(infile):
    '''Generator, yields each block in the input file.
    
    @param infile: file to read, is expected to have the VARBLOCK format as
        described in the module's docstring.
    @yields the contents of each block.
    '''

    # Check the version number
    version = ord(infile.read(1))
    if version != VARBLOCK_VERSION:
        raise ValueError('VARBLOCK version %i not supported' % version)

    while True:
        (block_size, read_bytes) = read_varint(infile)

        # EOF at block boundary, that's fine.
        if read_bytes == 0 and block_size == 0:
            break

        block = infile.read(block_size)

        read_size = len(block)
        if read_size != block_size:
            raise EOFError('Block size is %i, but could read only %i bytes' %
                    (block_size, read_size))


        yield block

