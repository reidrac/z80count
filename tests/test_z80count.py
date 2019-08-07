# -*- coding: utf-8 -*-

import pytest

from z80count.z80count import Parser
from z80count.z80count import z80count


@pytest.mark.parametrize("line,expected", (
    ("PLY_InterruptionOn: call PLY_Init",
     "PLY_InterruptionOn: call PLY_Init ; [17]\n"),
    ("$PLY_Interruption.On: call PLY_Init",
     "$PLY_Interruption.On: call PLY_Init ; [17]\n"),
    ("PLY_ReplayFrequency:\tld de,0",
     "PLY_ReplayFrequency:\tld de,0 ; [10]\n"),

))
def test_issue_11(line, expected):
    parser = Parser()
    output, _ = z80count(line, parser, total=0, subt=False,
                         no_update=True, column=1, use_tabs=False,
                         tab_width=4, debug=False)
    assert output == expected
