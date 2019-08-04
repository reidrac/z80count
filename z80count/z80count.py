# -*- coding: utf-8 -*-

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

import json
import sys
import re
import argparse
from os import path

version = "0.6.0"

OUR_COMMENT = re.compile(r"(\[[0-9.\s/]+\])")


def z80count(line,
             parser,
             total,
             subt,
             no_update,
             tabstop=2,
             debug=False,
             ):
    out = line.rstrip() + "\n"
    entry = parser.lookup(line)
    if entry:
        total, total_cond = update_counters(entry, total)
        out = format_line(
            line, entry, total, total_cond, subt, not no_update, tabstop=2, debug=False
        )
    return (out, total)


def update_counters(entry, total):
    if entry["_t_states_met"]:
        total_cond = total + entry["_t_states_met"]
    else:
        total_cond = 0
    total = total + entry["_t_states_or_not_met"]

    return (total, total_cond)


def format_line(line, entry, total, total_cond, subt, update, tabstop, debug):
    cycles = entry["cycles"]
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

    return out


def parse_command_line():
    parser = argparse.ArgumentParser(
        description='Z80 Cycle Count',
        epilog="Copyright (C) 2019 Juan J Martinez <jjm@usebox.net>")

    parser.add_argument(
        "--version", action="version", version="%(prog)s " + version)
    parser.add_argument('-d', dest='debug', action='store_true',
                        help="Enable debug (show the matched case)")
    parser.add_argument('-s', dest='subt', action='store_true',
                        help="Include subtotal")
    parser.add_argument('-n', dest='no_update', action='store_true',
                        help="Do not update existing count if available")
    parser.add_argument('-t', dest='tabstop', type=int,
                        help="Number of tabs for new comments", default=2)
    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType('r'), default=sys.stdin,
        help="Input file")
    parser.add_argument(
        "outfile", nargs="?", type=argparse.FileType('w'), default=sys.stdout,
        help="Output file")

    return parser.parse_args()


class Parser(object):

    """Simple parser based on a table of regexes.

    """

    # [label:] OPERATOR [OPERANDS] [; comment]
    _LINE_RE = re.compile(r"^([\w]+:)?\s*(?P<operator>\w+)(\s+.*)?$")

    def __init__(self):
        self._table = self._load_table()

    def lookup(self, line):
        mnemo = self._extract_mnemonic(line)
        if mnemo is None or mnemo not in self._table:
            return None
        for entry in self._table[mnemo]:
            if "_inited" not in entry:
                self._init_entry(entry)
            if entry["cregex"].search(line):
                return entry
        return None

    @classmethod
    def _load_table(cls):
        table_file = path.join(
            path.dirname(path.realpath(__file__)), "z80table.json")
        with open(table_file, "rt") as fd:
            table = json.load(fd)

        table.sort(key=lambda o: o["w"])
        res = {}
        for i in table:
            mnemo = cls._extract_mnemonic(i["case"])
            assert mnemo is not None
            if mnemo not in res:
                res[mnemo] = []
            res[mnemo].append(i)
        return res

    @classmethod
    def _extract_mnemonic(cls, line):
        match = cls._LINE_RE.match(line)
        if match:
            return match.group("operator").upper()
        return None

    @staticmethod
    def _init_entry(entry):
        entry["cregex"] = re.compile(r"^\s*" + entry["regex"] + r"\s*(;.*)?$", re.I)
        cycles = entry["cycles"]
        if "/" in cycles:
            c = cycles.split("/")
            t_states_or_not_met = int(c[1])
            t_states_met = int(c[0])
        else:
            t_states_or_not_met = int(cycles)
            t_states_met = 0
        entry["_t_states_or_not_met"] = t_states_or_not_met
        entry["_t_states_met"] = t_states_met
        entry["_inited"] = True


def main():
    args = parse_command_line()
    in_f = args.infile
    out_f = args.outfile
    parser = Parser()
    total = 0
    for line in in_f:
        output, total = z80count(
            line, parser, total, args.subt, args.no_update, args.tabstop, args.debug)
        out_f.write(output)
