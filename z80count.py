#!/usr/bin/env python3
#
# Copyright (C) 2019 by Juan J. Martinez <jjm@usebox.net>
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
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

__version__ = "0.4.2"

import json
import sys
import re
import argparse
from os import path

OUR_COMMENT = re.compile(r"(\[[0-9.\s/]+\])")


def z80count(line, table, total, total_cond, subt, update, tabstop=2, debug=False):
    out = line.rstrip() + "\n"
    for entry in table:
        if entry["cregex"].search(line):
            cycles = entry["cycles"]
            if "/" in cycles:
                c = cycles.split("/")
                total += int(c[1])
                total_cond += total + int(c[0])
            else:
                total += int(cycles)
                total_cond = 0

            line = line.rstrip().rsplit(";", 1)
            comment = "; [%s" % cycles
            if subt:
                if total_cond:
                    comment += " .. %d/%d]" % (total_cond, total)
                else:
                    comment += " .. %d]" % total
            else:
                comment += "]"
            if debug:
                comment += " case{%s}" % entry["case"]

            if len(line) == 1:
                comment = "\t" * tabstop + comment
            out = line[0] + comment
            if len(line) > 1:
                if update:
                    m = OUR_COMMENT.search(line[1])
                    if m:
                        line[1] = line[1].replace(m.group(0), "")
                out += " "
                out += line[1].lstrip()
            out += "\n"
            found = True
            break

    return (out, total, total_cond)

def init_table(table_file="z80table.json"):
    table_file = path.join(
        path.dirname(path.realpath(__file__)), table_file)
    with open(table_file, "rt") as fd:
        table = json.load(fd)

    for i in range(len(table)):
        table[i]["cregex"] = re.compile(table[i]["regex"] + r"\s?(;.*)?", re.I)

    return sorted(table, key=lambda o: o["w"])

def parse_command_line():
    parser = argparse.ArgumentParser(
        description='Z80 Cycle Count', epilog="Copyright (C) 2019 Juan J Martinez <jjm@usebox.net>")

    parser.add_argument(
        "--version", action="version", version="%(prog)s " + __version__)
    parser.add_argument('-d', dest='debug', action='store_true',
                        help="Enable debug (show the matched case)")
    parser.add_argument('-s', dest='subt', action='store_true',
                        help="Include subtotal")
    parser.add_argument('-u', dest='update', action='store_true',
                        help="Update existing count if available")
    parser.add_argument('-t', dest='tabstop', type=int,
                        help="Number of tabs for new comments", default=2)
    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType('r'), default=sys.stdin,
            help="Input file")
    parser.add_argument(
        "outfile", nargs="?", type=argparse.FileType('w'), default=sys.stdout,
            help="Output file")

    return parser.parse_args()


def lookup(line, table):
    for entry in table:
        if entry["cregex"].search(line):
            return entry
    return None


def main():
    args = parse_command_line()
    in_f = args.infile
    out_f = args.outfile
    table = init_table()
    total = total_cond = 0
    while True:
        line = in_f.readline()
        if not line:
            break

        output, total, total_cond = z80count(
            line, table, total, total_cond, args.subt, args.update, args.tabstop, args.debug)
        out_f.write(output)


if __name__ == "__main__":
    main()
