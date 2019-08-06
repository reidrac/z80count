# -*- coding: utf-8 -*-

import pytest

from z80count.z80count import comment_alignment
from z80count.z80count import format_line
from z80count.z80count import line_length


##########################################################################
# test support funtions                                                  #
##########################################################################

@pytest.mark.parametrize("line,tab_width,expected", (
    ("",      8, 0),
    (" ",     8, 1),
    ("a",     8, 1),
    ("á",     8, 1),

    ("\t",    8, 8),
    (" \t",   8, 8),
    ("  \t",  8, 8),
    ("\t ",   8, 9),
    ("\t\t",  8, 16),
    ("\t \t", 8, 16),

    ("\t",    3, 3),
    (" \t",   3, 3),
    ("  \t",  3, 3),
    ("\t ",   3, 4),
    ("\t\t",  3, 6),
    ("\t \t", 3, 6),

    ("\tadd hl,de", 4, 13),
))
def test_line_length(line, tab_width, expected):
    assert line_length(line, tab_width) == expected


@pytest.mark.parametrize("line,column,expected", (
    ("foo",      8, "    "),
    (" foo",     8, "   "),
    ("foo  ",    8, "  "),
    ("foo\t",    8, " "),
    ("foo     ", 8, " "),

    ("foo",      9, "\t"),
    (" foo",     9, "\t"),
    ("foo  ",    9, "\t"),
    ("foo\t",    9, " "),
    ("foo     ", 9, " "),

    ("longer than tab stop", 9, " "),
))
def test_comment_alignment_with_tabs(line, column, expected):
    assert comment_alignment(line, column, use_tabs=True, tab_width=8) == expected


def test_comment_alignment_bug_001():
    line = "\tld hl,PLY_Interruption_Convert"
    out = comment_alignment(line, column=50, use_tabs=True, tab_width=4)
    assert out == "\t\t\t\t"


def test_comment_alignment_bug_002():
    line = "\tadd hl,de"
    out = comment_alignment(line, column=50, use_tabs=True, tab_width=4)
    assert out == "\t\t\t\t\t\t\t\t\t"


def test_comment_alignment_bug_003():
    line = "\tjp #bce0"
    out = comment_alignment(line, column=50, use_tabs=True, tab_width=4)
    assert out == "\t\t\t\t\t\t\t\t\t"


@pytest.mark.parametrize("line,column,expected", (
    ("foo",      8, "    "),
    (" foo",     8, "   "),
    ("foo  ",    8, "  "),
    ("foo\t",    8, " "),
    ("foo    ",  8, " "),
    ("foo     ", 8, " "),

    ("foo",       9, "     "),
    (" foo",      9, "    "),
    ("foo  ",     9, "   "),
    ("foo\t",     9, " "),
    ("foo    ",   9, " "),
    ("foo     ",  9, " "),
    ("foo      ", 9, " "),

    ("longer than tab stop", 9, " "),
))
def test_comment_alignment_with_spaces(line, column, expected):
    assert comment_alignment(line, column, use_tabs=False, tab_width=8) == expected


##########################################################################
# test format_line                                                       #
##########################################################################


def _make_entry(cycles, case=""):
    return {
        "cycles": cycles,
        "case": case,
    }


def _run(line, cycles, total=0, total_cond=0, case="", subt=False,
         update=False, column=15, debug=False, use_tabs=False,
         tab_width=4):
    entry = _make_entry(cycles, case)
    return format_line(line, entry, total, total_cond, subt, update,
                       column, debug, use_tabs, tab_width)


def test_adds_comment():
    out = _run("  OPCODE", "5")
    assert out == "  OPCODE      ; [5]\n"


def test_subtotal_unconditional_opcode():
    out = _run("  OPCODE", "5", total=42, total_cond=0, subt=True)
    assert out == "  OPCODE      ; [5 .. 42]\n"


def test_subtotal_conditional_opcode():
    out = _run("  OPCODE", "7/5", total=42, total_cond=40, subt=True)
    assert out == "  OPCODE      ; [7/5 .. 40/42]\n"


def test_adds_case_if_debug_is_True():
    out = _run("  OPCODE", "5", debug=True, case="foo")
    assert out == "  OPCODE      ; [5] case{foo}\n"


def test_adds_cycles_in_previous_comment_if_update_is_False():
    out = _run("  OPCODE   ; [3] comment ", "5", update=False)
    assert out == "  OPCODE   ; [5] [3] comment\n"


def test_updates_cycles_in_previous_comment_if_update_is_True():
    out = _run("  OPCODE   ; [3] comment ", "5", update=True)
    assert out == "  OPCODE   ; [5] comment\n"


def test_line_longer_than_comment_column():
    out = _run("  A VERY LONG LINE", "5", update=True)
    assert out == "  A VERY LONG LINE ; [5]\n"
