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

version = "0.7.0"

OUR_COMMENT = re.compile(r"(\[[0-9.\s/]+\])")


def z80count(line,
             parser,
             total,
             subt,
             no_update,
             column=50,
             use_tabs=False,
             tab_width=8,
             debug=False,
             ):
    out = line.rstrip() + "\n"
    entry = parser.lookup(line)
    if entry:
        total, total_cond = update_counters(entry, total)
        out = format_line(
            line, entry, total, total_cond, subt, update=not no_update,
            column=column, debug=debug, use_tabs=use_tabs,
            tab_width=tab_width,
        )
    return (out, total)


def update_counters(entry, total):
    if entry["_t_states_met"]:
        total_cond = total + entry["_t_states_met"]
    else:
        total_cond = 0
    total = total + entry["_t_states_or_not_met"]

    return (total, total_cond)


def format_line(line, entry, total, total_cond, subt, update, column,
                debug, use_tabs, tab_width):
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
        comment = comment_alignment(line[0], column, use_tabs, tab_width) + comment
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


def comment_alignment(line, column, use_tabs=False, tab_width=8):
    """Calculate the spacing required for comment alignment.

    :param str line: code line
    :param int column: column in which we want the comment to start
    :param bool use_tabs: use tabs instead of spaces
    :param int tab_width: tab width

    :returns: the spacing
    :rtype: str

    """

    expected_length = column - 1
    length = line_length(line, tab_width)
    if length >= expected_length:
        return " "  # add an space before the colon

    if use_tabs:
        tab_stop = (expected_length // tab_width) * tab_width + 1
        if tab_stop > length:
            extra_tabs = (tab_stop - length) // tab_width
            if length % tab_width > 1:
                extra_tabs += 1  # complete partial tab
            extra_spaces = expected_length - tab_stop
        else:
            extra_tabs = 0
            extra_spaces = expected_length - length
    else:
        extra_tabs = 0
        extra_spaces = expected_length - length

    return "\t" * extra_tabs + " " * extra_spaces


def line_length(line, tab_width):
    """Calculate the length of a line taking TABs into account.

    :param str line: line of code
    :param int tab_width: tab width

    :returns: The length of the line
    :rtype: int

    """
    length = 0
    for i in line:
        if i == "\t":
            length = ((length + tab_width) // tab_width) * tab_width
        else:
            length += 1
    return length


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
    parser.add_argument('-t', dest='tab_width', type=int,
                        help="Number of spaces for each tab", default=8)
    parser.add_argument('--use-spaces', dest='use_spaces', action='store_true',
                        help="Use spaces to align newly added comments", default=True)
    parser.add_argument('--use-tabs', dest='use_spaces', action='store_false',
                        help="Use tabs to align newly added comments")
    parser.add_argument('-c', '--column', dest='column', type=int,
                        help="Column to align newly added comments", default=50)

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
            if "_initialized" not in entry:
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
        entry["_initialized"] = True


def main():
    args = parse_command_line()
    in_f = args.infile
    out_f = args.outfile
    parser = Parser()
    total = 0
    for line in in_f:
        output, total = z80count(
            line, parser, total, args.subt, args.no_update,
            args.column, not args.use_spaces, args.tab_width,
            args.debug,
        )
        out_f.write(output)
