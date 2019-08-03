# -*- coding: utf-8 -*-

from z80count.z80count import format_line


def _make_entry(cycles, case=""):
    return {
        "cycles": cycles,
        "case": case,
    }


def _run(line, cycles, total=0, total_cond=0, case="", subt=False,
         update=False, tabstop=2, debug=False):
    entry = _make_entry(cycles, case)
    return format_line(line, entry, total, total_cond, subt, update,
                       tabstop, debug)


def test_adds_comment():
    out = _run("  OPCODE", "5")
    assert out == "  OPCODE\t\t; [5]\n"


def test_subtotal_unconditional_opcode():
    out = _run("  OPCODE", "5", total=42, total_cond=0, subt=True)
    assert out == "  OPCODE\t\t; [5 .. 42]\n"


def test_subtotal_conditional_opcode():
    out = _run("  OPCODE", "7/5", total=42, total_cond=40, subt=True)
    assert out == "  OPCODE\t\t; [7/5 .. 40/42]\n"


def test_adds_case_if_debug_is_True():
    out = _run("  OPCODE", "5", debug=True, case="foo")
    assert out == "  OPCODE\t\t; [5] case{foo}\n"


def test_adds_cycles_in_previous_comment_if_update_is_False():
    out = _run("  OPCODE   ; [3] comment ", "5", update=False)
    assert out == "  OPCODE   ; [5] [3] comment\n"


def test_updates_cycles_in_previous_comment_if_update_is_True():
    out = _run("  OPCODE   ; [3] comment ", "5", update=True)
    assert out == "  OPCODE   ; [5] comment\n"
