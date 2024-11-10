#!/usr/bin/env python3
#
# This program parses an SQLite3 database for deleted entires and
# places the output into either and TSV file, or text file
#
# The SQLite file format, offsets etc is described at
# sqlite.org/fileformat.html
#
#
# Copyright (C) 2015 Mari DeGrazia (arizona4n6@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You can view the GNU General Public License at <http://www.gnu.org/licenses/>
#
# Version History:
# v1.1 2013-11-05
#
# v1.2 2015-06-20
# support added in to print out non b-tree pages
#
# v1.3 2015-06-21
# minor changes / comments etc.
#
# v2.0 2024-11-08
# Updated for python3 by Corey Forman - github.com/digitalsleuth

import struct
import argparse
import sys
import os

__version__ = "2.0"
__maintainer__ = "Corey Forman - github.com/digitalsleuth"
__author__ = "Mari DeGrazia, Corey Forman"
__description__ = (
    f"Python 3 SQLite Carver for deleted records from an SQLite database v{__version__}"
)
__usage__ = f"\n\
{os.path.basename(__file__)} -f /home/sanforensics/smsmms.db -o report.tsv\n\
{os.path.basename(__file__)} -f /home/sanforensics/index.db -r -o report.txt \n"


# function to remove the non-printable characters, tabs and white spaces
def remove_ascii_non_printable(chunk):
    chunk = b" ".join(chunk.split())
    printable = []
    for ch in chunk:
        if (31 < ch < 127) or ch == 9:
            printable.append(chr(ch))
    return "".join(printable)


def parse_db_file(args, output):
    # write the column header if not outputting to text file
    stats = os.stat(args.infile)
    filesize = stats.st_size

    f = open(args.infile, "rb")

    if not args.raw:
        output.write("Type\tOffset\tLength\tData\n")

    # be kind, rewind (to the beginning of the file, that is)
    f.seek(0)

    # verify the file is an sqlite db; read the first 16 bytes for the header
    header = f.read(16)

    if b"SQLite" not in header:
        print("File does not appear to be an SQLite File")
        sys.exit(0)

    # The pagesize is stored at offset 16 at is 2 bytes long

    pagesize = struct.unpack(">H", f.read(2))[0]

    # According to SQLite.org/fileformat.html, all the data is contained in the table-b-trees leaves.
    # Let's go to each Page, read the B-Tree Header, and see if it is a table b-tree, which is designated by the flag 13
    # set the offset to 0, so we can also process any strings in the first page
    offset = 0

    while offset < filesize:

        # move to the beginning of the page and read the b-tree flag, if it's 13, its a leaf table b tree and we want to process it
        f.seek(offset)
        flag = struct.unpack(">b", f.read(1))[0]

        if flag == 13:
            freeblock_offset = struct.unpack(">h", f.read(2))[0]
            num_cells = struct.unpack(">h", f.read(2))[0]
            cell_offset = struct.unpack(">h", f.read(2))[0]
            _ = struct.unpack(">b", f.read(1))[0]

            # start after the header (8 bytes) and after the cell pointer array. The cell pointer array will be the number of cells x 2 bytes per cell
            start = 8 + (num_cells * 2)

            # the length of the unallocated space will be the difference between the start and the cell offset
            length = cell_offset - start

            # unallocated is the space after the header information and before the first cell starts
            # move to start of unallocated, then read the data (if any) in unallocated - remember, we already read in the first 8 bytes, so now we just need to move past the cell pointer array
            f.read(num_cells * 2)
            unallocated = f.read(length)
            if args.raw:
                output.write(
                    f"Unallocated, Offset {str(offset + start)}, Length {str(length)}\n"
                )
                output.write("Data:\n")
                output.write(str(unallocated))
                output.write("\n\n")

            else:
                unallocated = remove_ascii_non_printable(unallocated)
                if unallocated != "":
                    output.write(
                        f"Unallocated\t{str(offset + start)}\t{str(length)}\t{str(unallocated)}\n"
                    )

            # if there are freeblocks, lets pull the data

            while freeblock_offset != 0:

                # move to the freeblock offset
                f.seek(offset + freeblock_offset)

                # get next freeblock chain
                next_fb_offset = struct.unpack(">h", f.read(2))[0]

                # get the size of this freeblock
                free_block_size = struct.unpack(">hh", f.read(4))[0]

                # move to the offset so we can read the free block data
                f.seek(offset + freeblock_offset)

                # read in this freeblock
                free_block = f.read(free_block_size)

                if args.raw:
                    output.write(
                        f"Free Block, Offset {str(offset + freeblock_offset)}, Length {str(free_block_size)}\n"
                    )
                    output.write("Data:\n")
                    output.write(str(free_block))
                    output.write("\n\n")

                else:
                    free_block = remove_ascii_non_printable(free_block)
                    if unallocated != "":
                        output.write(
                            f"Free Block\t{str(offset + freeblock_offset)}\t{str(free_block_size)}\t{str(free_block)}\n"
                        )

                freeblock_offset = next_fb_offset

        # Cheeky's Change: Extract strings from non-Leaf-Table B-tree pages to handle re-purposed/re-used pages
        # According to docs, valid flag values are 2, 5, 10, 13 BUT pages containing string data have also been observed with flag = 0
        elif args.printpages:
            f.seek(
                -1, 1
            )  # since flag is not 13, we don't care what the flag is, lets go back and get that byte for output
            pagestring = f.read(pagesize)
            printable_pagestring = remove_ascii_non_printable(pagestring)

            if args.raw:
                output.write(
                    f"Non-Leaf-Table-Btree-Type_{str(flag)}, Offset {str(offset)}, Length {str(pagesize)}\n"
                )
                output.write(
                    "Data: (ONLY PRINTABLE STRINGS ARE SHOWN HERE. FOR RAW DATA, CHECK FILE IN HEX VIEWER AT ABOVE LISTED OFFSET):\n\n"
                )
                output.write(printable_pagestring)
                output.write("\n\n")
            else:
                output.write(
                    f"Non-Leaf-Table-Btree-Type_{str(flag)}\t{str(offset)}\t{str(pagesize)}\t{printable_pagestring}\n"
                )
        offset = offset + pagesize
    output.close()


def main():
    parser = argparse.ArgumentParser(description=__description__, usage=__usage__)
    parser.add_argument(
        "-f",
        "--file",
        dest="infile",
        help="sqlite database file",
        metavar="<db>",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="outfile",
        help="Output to a tsv file. Strips white space, tabs and non-printable characters from data field",
        metavar="output.tsv",
        required=True,
    )
    parser.add_argument(
        "-r",
        "--raw",
        action="store_true",
        dest="raw",
        help="Optional. Will out put data field in a raw format and text file.",
    )
    parser.add_argument(
        "-p",
        "--printpages",
        action="store_true",
        dest="printpages",
        help="Optional. Will print any printable non-whitespace chars from all non-leaf b-tree pages (in case page has been re-purposed). WARNING: May output a lot of string data.",
    )

    args = parser.parse_args()

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()

    if not os.path.isfile(args.infile):
        print("File not found, check your path and try again.")
        sys.exit(1)

    try:
        output = open(args.outfile, "w", encoding="utf-8")
    except (FileNotFoundError, IsADirectoryError):
        print("Error opening output file")
        sys.exit(0)

    parse_db_file(args, output)


if __name__ == "__main__":
    main()
