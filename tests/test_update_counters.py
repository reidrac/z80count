# -*- coding: utf-8 -*-

from z80count.z80count import update_counters


def _make_entry(states, states_met=0):
    return {
        "_t_states_met": states_met,
        "_t_states_or_not_met": states,
    }


def test_unconditional_instruction():
    total, total_cond = update_counters(_make_entry(3), 8)
    assert total == 11
    assert total_cond == 0


def test_conditional_instruction():
    total, total_cond = update_counters(_make_entry(7, 5), 35)
    assert total == 42
    assert total_cond == 40
