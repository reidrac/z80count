#!/usr/bin/env python3

import pytest

from z80count.z80count import Parser


data = (
    ("ADC A, (HL)", "7"),
    ("ADC A, 10", "7"),
    ("ADC A, 0x10", "7"),
    ("ADC A, CONST", "7"),
    ("ADC A, A", "4"),
    ("ADC A, B", "4"),
    ("ADC A, C", "4"),
    ("ADC A, D", "4"),
    ("ADC A, E", "4"),
    ("ADC A, H", "4"),
    ("ADC A, L", "4"),
    ("ADC HL, BC", "15"),
    ("ADC HL, DE", "15"),
    ("ADC HL, HL", "15"),
    ("ADC HL, SP", "15"),
    ("ADD A, (HL)", "7"),
    ("ADD A, 10", "7"),
    ("ADD A, 0x10", "7"),
    ("ADD A, CONST", "7"),
    ("ADD A, (IX+10)", "19"),
    ("ADD A, (IX+0x10)", "19"),
    ("ADD A, (IX+CONST)", "19"),
    ("ADD A, A", "4"),
    ("ADD A, B", "4"),
    ("ADD A, C", "4"),
    ("ADD A, D", "4"),
    ("ADD A, E", "4"),
    ("ADD A, H", "4"),
    ("ADD A, L", "4"),
    ("ADD HL, BC", "11"),
    ("ADD HL, DE", "11"),
    ("ADD HL, HL", "11"),
    ("ADD HL, SP", "11"),
    ("ADD IX, BC", "15"),
    ("ADD IX, DE", "15"),
    ("ADD IX, SP", "15"),
    ("ADD IY, BC", "15"),
    ("ADD IY, DE", "15"),
    ("ADD IY, SP", "15"),
    ("AND (HL)", "7"),
    ("AND 10", "7"),
    ("AND 0x10", "7"),
    ("AND CONST", "7"),
    ("AND A", "4"),
    ("AND B", "4"),
    ("AND C", "4"),
    ("AND D", "4"),
    ("AND E", "4"),
    ("AND H", "4"),
    ("AND L", "4"),
    ("BIT 0, (HL)", "12"),
    ("BIT 1, (HL)", "12"),
    ("BIT 2, (HL)", "12"),
    ("BIT 3, (HL)", "12"),
    ("BIT 4, (HL)", "12"),
    ("BIT 5, (HL)", "12"),
    ("BIT 6, (HL)", "12"),
    ("BIT 7, (HL)", "12"),
    ("BIT 0, A", "8"),
    ("BIT 0, B", "8"),
    ("BIT 0, C", "8"),
    ("BIT 0, D", "8"),
    ("BIT 0, E", "8"),
    ("BIT 0, H", "8"),
    ("BIT 0, L", "8"),
    ("BIT 1, A", "8"),
    ("BIT 1, B", "8"),
    ("BIT 1, C", "8"),
    ("BIT 1, D", "8"),
    ("BIT 1, E", "8"),
    ("BIT 1, H", "8"),
    ("BIT 1, L", "8"),
    ("BIT 2, A", "8"),
    ("BIT 2, B", "8"),
    ("BIT 2, C", "8"),
    ("BIT 2, D", "8"),
    ("BIT 2, E", "8"),
    ("BIT 2, H", "8"),
    ("BIT 2, L", "8"),
    ("BIT 3, A", "8"),
    ("BIT 3, B", "8"),
    ("BIT 3, C", "8"),
    ("BIT 3, D", "8"),
    ("BIT 3, E", "8"),
    ("BIT 3, H", "8"),
    ("BIT 3, L", "8"),
    ("BIT 4, A", "8"),
    ("BIT 4, B", "8"),
    ("BIT 4, C", "8"),
    ("BIT 4, D", "8"),
    ("BIT 4, E", "8"),
    ("BIT 4, H", "8"),
    ("BIT 4, L", "8"),
    ("BIT 5, A", "8"),
    ("BIT 5, B", "8"),
    ("BIT 5, C", "8"),
    ("BIT 5, D", "8"),
    ("BIT 5, E", "8"),
    ("BIT 5, H", "8"),
    ("BIT 5, L", "8"),
    ("BIT 6, A", "8"),
    ("BIT 6, B", "8"),
    ("BIT 6, C", "8"),
    ("BIT 6, D", "8"),
    ("BIT 6, E", "8"),
    ("BIT 6, H", "8"),
    ("BIT 6, L", "8"),
    ("BIT 7, A", "8"),
    ("BIT 7, B", "8"),
    ("BIT 7, C", "8"),
    ("BIT 7, D", "8"),
    ("BIT 7, E", "8"),
    ("BIT 7, H", "8"),
    ("BIT 7, L", "8"),
    ("CALL 0x10", "17"),
    ("CALL 0xABCD", "17"),
    ("CALL 10", "17"),
    ("CALL 1234", "17"),
    ("CALL CONST", "17"),
    ("CALL NZ, 10", "17/10"),
    ("CALL NZ, 0x10", "17/10"),
    ("CALL NZ, 1234", "17/10"),
    ("CALL NZ, 0xABCD", "17/10"),
    ("CALL NZ, CONST", "17/10"),
    ("CALL Z, 10", "17/10"),
    ("CALL Z, 0x10", "17/10"),
    ("CALL Z, 1234", "17/10"),
    ("CALL Z, 0xABCD", "17/10"),
    ("CALL Z, CONST", "17/10"),
    ("CALL NC, 10", "17/10"),
    ("CALL NC, 0x10", "17/10"),
    ("CALL NC, 1234", "17/10"),
    ("CALL NC, 0xABCD", "17/10"),
    ("CALL NC, CONST", "17/10"),
    ("CALL C, 10", "17/10"),
    ("CALL C, 0x10", "17/10"),
    ("CALL C, 1234", "17/10"),
    ("CALL C, 0xABCD", "17/10"),
    ("CALL C, CONST", "17/10"),
    ("CALL PO, 10", "17/10"),
    ("CALL PO, 0x10", "17/10"),
    ("CALL PO, 1234", "17/10"),
    ("CALL PO, 0xABCD", "17/10"),
    ("CALL PO, CONST", "17/10"),
    ("CALL PE, 10", "17/10"),
    ("CALL PE, 0x10", "17/10"),
    ("CALL PE, 1234", "17/10"),
    ("CALL PE, 0xABCD", "17/10"),
    ("CALL PE, CONST", "17/10"),
    ("CALL P, 10", "17/10"),
    ("CALL P, 0x10", "17/10"),
    ("CALL P, 1234", "17/10"),
    ("CALL P, 0xABCD", "17/10"),
    ("CALL P, CONST", "17/10"),
    ("CALL M, 10", "17/10"),
    ("CALL M, 0x10", "17/10"),
    ("CALL M, 1234", "17/10"),
    ("CALL M, 0xABCD", "17/10"),
    ("CALL M, CONST", "17/10"),
    ("CCF ", "4"),
    ("CP (HL)", "7"),
    ("CP 10", "7"),
    ("CP 0x10", "7"),
    ("CP CONST", "7"),
    ("CP (IX+10)", "19"),
    ("CP (IX+0x10)", "19"),
    ("CP (IX+CONST)", "19"),
    ("CP A", "4"),
    ("CP B", "4"),
    ("CP C", "4"),
    ("CP D", "4"),
    ("CP E", "4"),
    ("CP H", "4"),
    ("CP L", "4"),
    ("CPD ", "16"),
    ("CPDR ", "21/16"),
    ("CPI ", "16"),
    ("CPIR ", "21/16"),
    ("CPL ", "4"),
    ("DAA ", "4"),
    ("DEC (HL)", "11"),
    ("DEC ix", "10"),
    ("DEC A", "4"),
    ("DEC B", "4"),
    ("DEC C", "4"),
    ("DEC D", "4"),
    ("DEC E", "4"),
    ("DEC H", "4"),
    ("DEC L", "4"),
    ("DEC BC", "6"),
    ("DEC DE", "6"),
    ("DEC HL", "6"),
    ("DEC SP", "6"),
    ("DI ", "4"),
    ("DJNZ 10", "13/8"),
    ("DJNZ 0x10", "13/8"),
    ("DJNZ CONST", "13/8"),
    ("EI ", "4"),
    ("EX (SP), ix", "23"),
    ("EX AF, AF'", "4"),
    ("EX DE, HL", "4"),
    ("EXX ", "4"),
    ("HALT ", "4"),
    ("IM 0", "8"),
    ("IM 1", "8"),
    ("IM 2", "8"),
    ("IN A, (10)", "11"),
    ("IN A, (0x10)", "11"),
    ("IN A, (CONST)", "11"),
    ("IN A, (C)", "12"),
    ("IN B, (C)", "12"),
    ("IN C, (C)", "12"),
    ("IN D, (C)", "12"),
    ("IN E, (C)", "12"),
    ("IN H, (C)", "12"),
    ("IN L, (C)", "12"),
    ("INC (HL)", "11"),
    ("INC (IX+10)", "23"),
    ("INC (IX+0x10)", "23"),
    ("INC (IX+CONST)", "23"),
    ("INC ix", "10"),
    ("INC A", "4"),
    ("INC B", "4"),
    ("INC C", "4"),
    ("INC D", "4"),
    ("INC E", "4"),
    ("INC H", "4"),
    ("INC L", "4"),
    ("INC BC", "6"),
    ("INC DE", "6"),
    ("INC HL", "6"),
    ("INC SP", "6"),
    ("IND ", "16"),
    ("INI ", "16"),
    ("INDR ", "21/16"),
    ("INIR ", "21/16"),
    ("JP NZ, 10", "10"),
    ("JP NZ, 0x10", "10"),
    ("JP NZ, 1234", "10"),
    ("JP NZ, 0xABCD", "10"),
    ("JP NZ, CONST", "10"),
    ("JP Z, 10", "10"),
    ("JP Z, 0x10", "10"),
    ("JP Z, 1234", "10"),
    ("JP Z, 0xABCD", "10"),
    ("JP Z, CONST", "10"),
    ("JP NC, 10", "10"),
    ("JP NC, 0x10", "10"),
    ("JP NC, 1234", "10"),
    ("JP NC, 0xABCD", "10"),
    ("JP NC, CONST", "10"),
    ("JP C, 10", "10"),
    ("JP C, 0x10", "10"),
    ("JP C, 1234", "10"),
    ("JP C, 0xABCD", "10"),
    ("JP C, CONST", "10"),
    ("JP PO, 10", "10"),
    ("JP PO, 0x10", "10"),
    ("JP PO, 1234", "10"),
    ("JP PO, 0xABCD", "10"),
    ("JP PO, CONST", "10"),
    ("JP PE, 10", "10"),
    ("JP PE, 0x10", "10"),
    ("JP PE, 1234", "10"),
    ("JP PE, 0xABCD", "10"),
    ("JP PE, CONST", "10"),
    ("JP P, 10", "10"),
    ("JP P, 0x10", "10"),
    ("JP P, 1234", "10"),
    ("JP P, 0xABCD", "10"),
    ("JP P, CONST", "10"),
    ("JP M, 10", "10"),
    ("JP M, 0x10", "10"),
    ("JP M, 1234", "10"),
    ("JP M, 0xABCD", "10"),
    ("JP M, CONST", "10"),
    ("JP (HL)", "4"),
    ("JP (IX)", "8"),
    ("JP 10", "10"),
    ("JP 0x10", "10"),
    ("JP 1234", "10"),
    ("JP 0xABCD", "10"),
    ("JP CONST", "10"),
    ("JR NZ, 10", "12/7"),
    ("JR NZ, 0x10", "12/7"),
    ("JR NZ, CONST", "12/7"),
    ("JR Z, 10", "12/7"),
    ("JR Z, 0x10", "12/7"),
    ("JR Z, CONST", "12/7"),
    ("JR NC, 10", "12/7"),
    ("JR NC, 0x10", "12/7"),
    ("JR NC, CONST", "12/7"),
    ("JR C, 10", "12/7"),
    ("JR C, 0x10", "12/7"),
    ("JR C, CONST", "12/7"),
    ("JR 10", "12"),
    ("JR 0x10", "12"),
    ("JR CONST", "12"),
    ("LD (IX+10), A", "19"),
    ("LD (IX+10), B", "19"),
    ("LD (IX+10), C", "19"),
    ("LD (IX+10), D", "19"),
    ("LD (IX+10), E", "19"),
    ("LD (IX+10), H", "19"),
    ("LD (IX+10), L", "19"),
    ("LD (IX+0x10), A", "19"),
    ("LD (IX+0x10), B", "19"),
    ("LD (IX+0x10), C", "19"),
    ("LD (IX+0x10), D", "19"),
    ("LD (IX+0x10), E", "19"),
    ("LD (IX+0x10), H", "19"),
    ("LD (IX+0x10), L", "19"),
    ("LD (IX+CONST), A", "19"),
    ("LD (IX+CONST), B", "19"),
    ("LD (IX+CONST), C", "19"),
    ("LD (IX+CONST), D", "19"),
    ("LD (IX+CONST), E", "19"),
    ("LD (IX+CONST), H", "19"),
    ("LD (IX+CONST), L", "19"),
    ("LD (IX+10), 10", "19"),
    ("LD (IX+10), 0x10", "19"),
    ("LD (IX+10), CONST", "19"),
    ("LD (IX+0x10), 10", "19"),
    ("LD (IX+0x10), 0x10", "19"),
    ("LD (IX+0x10), CONST", "19"),
    ("LD (IX+CONST), 10", "19"),
    ("LD (IX+CONST), 0x10", "19"),
    ("LD (IX+CONST), CONST", "19"),
    ("LD (10), A", "13"),
    ("LD (0x10), A", "13"),
    ("LD (1234), A", "13"),
    ("LD (0xABCD), A", "13"),
    ("LD (CONST), A", "13"),
    ("LD (10), HL", "16"),
    ("LD (0x10), HL", "16"),
    ("LD (1234), HL", "16"),
    ("LD (0xABCD), HL", "16"),
    ("LD (CONST), HL", "16"),
    ("LD (10), BC", "20"),
    ("LD (10), DE", "20"),
    ("LD (10), SP", "20"),
    ("LD (0x10), BC", "20"),
    ("LD (0x10), DE", "20"),
    ("LD (0x10), SP", "20"),
    ("LD (1234), BC", "20"),
    ("LD (1234), DE", "20"),
    ("LD (1234), SP", "20"),
    ("LD (0xABCD), BC", "20"),
    ("LD (0xABCD), DE", "20"),
    ("LD (0xABCD), SP", "20"),
    ("LD (CONST), BC", "20"),
    ("LD (CONST), DE", "20"),
    ("LD (CONST), SP", "20"),
    ("LD (BC), A", "7"),
    ("LD (DE), A", "7"),
    ("LD (HL), A", "7"),
    ("LD (HL), B", "7"),
    ("LD (HL), C", "7"),
    ("LD (HL), D", "7"),
    ("LD (HL), E", "7"),
    ("LD (HL), H", "7"),
    ("LD (HL), L", "7"),
    ("LD A, (10)", "13"),
    ("LD A, (0x10)", "13"),
    ("LD A, (1234)", "13"),
    ("LD A, (0xABCD)", "13"),
    ("LD A, (CONST)", "13"),
    ("LD A, I", "9"),
    ("LD A, R", "9"),
    ("LD HL, (10)", "16"),
    ("LD HL, (0x10)", "16"),
    ("LD HL, (1234)", "16"),
    ("LD HL, (0xABCD)", "16"),
    ("LD HL, (CONST)", "16"),
    ("LD ix, 10", "14"),
    ("LD ix, 0x10", "14"),
    ("LD ix, 1234", "14"),
    ("LD ix, 0xABCD", "14"),
    ("LD ix, CONST", "14"),
    ("LD A, (IX+10)", "19"),
    ("LD A, (IX+0x10)", "19"),
    ("LD A, (IX+CONST)", "19"),
    ("LD B, (IX+10)", "19"),
    ("LD B, (IX+0x10)", "19"),
    ("LD B, (IX+CONST)", "19"),
    ("LD C, (IX+10)", "19"),
    ("LD C, (IX+0x10)", "19"),
    ("LD C, (IX+CONST)", "19"),
    ("LD D, (IX+10)", "19"),
    ("LD D, (IX+0x10)", "19"),
    ("LD D, (IX+CONST)", "19"),
    ("LD E, (IX+10)", "19"),
    ("LD E, (IX+0x10)", "19"),
    ("LD E, (IX+CONST)", "19"),
    ("LD H, (IX+10)", "19"),
    ("LD H, (IX+0x10)", "19"),
    ("LD H, (IX+CONST)", "19"),
    ("LD L, (IX+10)", "19"),
    ("LD L, (IX+0x10)", "19"),
    ("LD L, (IX+CONST)", "19"),
    ("LD A, (BC)", "7"),
    ("LD A, (DE)", "7"),
    ("LD A, (HL)", "7"),
    ("LD B, (HL)", "7"),
    ("LD C, (HL)", "7"),
    ("LD D, (HL)", "7"),
    ("LD E, (HL)", "7"),
    ("LD H, (HL)", "7"),
    ("LD L, (HL)", "7"),
    ("LD A, 10", "7"),
    ("LD A, 0x10", "7"),
    ("LD A, CONST", "7"),
    ("LD B, 10", "7"),
    ("LD B, 0x10", "7"),
    ("LD B, CONST", "7"),
    ("LD C, 10", "7"),
    ("LD C, 0x10", "7"),
    ("LD C, CONST", "7"),
    ("LD D, 10", "7"),
    ("LD D, 0x10", "7"),
    ("LD D, CONST", "7"),
    ("LD E, 10", "7"),
    ("LD E, 0x10", "7"),
    ("LD E, CONST", "7"),
    ("LD H, 10", "7"),
    ("LD H, 0x10", "7"),
    ("LD H, CONST", "7"),
    ("LD L, 10", "7"),
    ("LD L, 0x10", "7"),
    ("LD L, CONST", "7"),
    ("LD A, A", "4"),
    ("LD A, B", "4"),
    ("LD A, C", "4"),
    ("LD A, D", "4"),
    ("LD A, E", "4"),
    ("LD A, H", "4"),
    ("LD A, L", "4"),
    ("LD B, A", "4"),
    ("LD B, B", "4"),
    ("LD B, C", "4"),
    ("LD B, D", "4"),
    ("LD B, E", "4"),
    ("LD B, H", "4"),
    ("LD B, L", "4"),
    ("LD C, A", "4"),
    ("LD C, B", "4"),
    ("LD C, C", "4"),
    ("LD C, D", "4"),
    ("LD C, E", "4"),
    ("LD C, H", "4"),
    ("LD C, L", "4"),
    ("LD D, A", "4"),
    ("LD D, B", "4"),
    ("LD D, C", "4"),
    ("LD D, D", "4"),
    ("LD D, E", "4"),
    ("LD D, H", "4"),
    ("LD D, L", "4"),
    ("LD E, A", "4"),
    ("LD E, B", "4"),
    ("LD E, C", "4"),
    ("LD E, D", "4"),
    ("LD E, E", "4"),
    ("LD E, H", "4"),
    ("LD E, L", "4"),
    ("LD H, A", "4"),
    ("LD H, B", "4"),
    ("LD H, C", "4"),
    ("LD H, D", "4"),
    ("LD H, E", "4"),
    ("LD H, H", "4"),
    ("LD H, L", "4"),
    ("LD L, A", "4"),
    ("LD L, B", "4"),
    ("LD L, C", "4"),
    ("LD L, D", "4"),
    ("LD L, E", "4"),
    ("LD L, H", "4"),
    ("LD L, L", "4"),
    ("LD BC, (10)", "20"),
    ("LD BC, (0x10)", "20"),
    ("LD BC, (1234)", "20"),
    ("LD BC, (0xABCD)", "20"),
    ("LD BC, (CONST)", "20"),
    ("LD DE, (10)", "20"),
    ("LD DE, (0x10)", "20"),
    ("LD DE, (1234)", "20"),
    ("LD DE, (0xABCD)", "20"),
    ("LD DE, (CONST)", "20"),
    ("LD SP, (10)", "20"),
    ("LD SP, (0x10)", "20"),
    ("LD SP, (1234)", "20"),
    ("LD SP, (0xABCD)", "20"),
    ("LD SP, (CONST)", "20"),
    ("LD BC, 10", "10"),
    ("LD BC, 0x10", "10"),
    ("LD BC, 1234", "10"),
    ("LD BC, 0xABCD", "10"),
    ("LD BC, CONST", "10"),
    ("LD DE, 10", "10"),
    ("LD DE, 0x10", "10"),
    ("LD DE, 1234", "10"),
    ("LD DE, 0xABCD", "10"),
    ("LD DE, CONST", "10"),
    ("LD HL, 10", "10"),
    ("LD HL, 0x10", "10"),
    ("LD HL, 1234", "10"),
    ("LD HL, 0xABCD", "10"),
    ("LD HL, CONST", "10"),
    ("LD SP, 10", "10"),
    ("LD SP, 0x10", "10"),
    ("LD SP, 1234", "10"),
    ("LD SP, 0xABCD", "10"),
    ("LD SP, CONST", "10"),
    ("LD SP, HL", "6"),
    ("LD SP, ix", "10"),
    ("LDD ", "16"),
    ("LDI ", "16"),
    ("LDDR ", "21/16"),
    ("LDIR ", "21/16"),
    ("NEG ", "8"),
    ("NOP ", "4"),
    ("OR (IX+10)", "19"),
    ("OR (IX+0x10)", "19"),
    ("OR (IX+CONST)", "19"),
    ("OR 10", "7"),
    ("OR 0x10", "7"),
    ("OR CONST", "7"),
    ("OR A", "4"),
    ("OR B", "4"),
    ("OR C", "4"),
    ("OR D", "4"),
    ("OR E", "4"),
    ("OR H", "4"),
    ("OR L", "4"),
    ("OTDR ", "21/16"),
    ("OTIR ", "21/16"),
    ("OUT (C), A", "12"),
    ("OUT (C), B", "12"),
    ("OUT (C), C", "12"),
    ("OUT (C), D", "12"),
    ("OUT (C), E", "12"),
    ("OUT (C), H", "12"),
    ("OUT (C), L", "12"),
    ("OUT (10), A", "11"),
    ("OUT (0x10), A", "11"),
    ("OUT (CONST), A", "11"),
    ("OUTD ", "16"),
    ("OUTI ", "16"),
    ("POP AF", "10"),
    ("POP BC", "10"),
    ("POP DE", "10"),
    ("POP HL", "10"),
    ("POP IX", "14"),
    ("POP IY", "14"),
    ("PUSH AF", "11"),
    ("PUSH BC", "11"),
    ("PUSH DE", "11"),
    ("PUSH HL", "11"),
    ("PUSH IX", "15"),
    ("PUSH IY", "15"),
    ("RES 0, (HL)", "15"),
    ("RES 1, (HL)", "15"),
    ("RES 2, (HL)", "15"),
    ("RES 3, (HL)", "15"),
    ("RES 4, (HL)", "15"),
    ("RES 5, (HL)", "15"),
    ("RES 6, (HL)", "15"),
    ("RES 7, (HL)", "15"),
    ("RES 0, (IX+10)", "23"),
    ("RES 0, (IX+0x10)", "23"),
    ("RES 0, (IX+CONST)", "23"),
    ("RES 1, (IX+10)", "23"),
    ("RES 1, (IX+0x10)", "23"),
    ("RES 1, (IX+CONST)", "23"),
    ("RES 2, (IX+10)", "23"),
    ("RES 2, (IX+0x10)", "23"),
    ("RES 2, (IX+CONST)", "23"),
    ("RES 3, (IX+10)", "23"),
    ("RES 3, (IX+0x10)", "23"),
    ("RES 3, (IX+CONST)", "23"),
    ("RES 4, (IX+10)", "23"),
    ("RES 4, (IX+0x10)", "23"),
    ("RES 4, (IX+CONST)", "23"),
    ("RES 5, (IX+10)", "23"),
    ("RES 5, (IX+0x10)", "23"),
    ("RES 5, (IX+CONST)", "23"),
    ("RES 6, (IX+10)", "23"),
    ("RES 6, (IX+0x10)", "23"),
    ("RES 6, (IX+CONST)", "23"),
    ("RES 7, (IX+10)", "23"),
    ("RES 7, (IX+0x10)", "23"),
    ("RES 7, (IX+CONST)", "23"),
    ("RES 0, A", "8"),
    ("RES 0, B", "8"),
    ("RES 0, C", "8"),
    ("RES 0, D", "8"),
    ("RES 0, E", "8"),
    ("RES 0, H", "8"),
    ("RES 0, L", "8"),
    ("RES 1, A", "8"),
    ("RES 1, B", "8"),
    ("RES 1, C", "8"),
    ("RES 1, D", "8"),
    ("RES 1, E", "8"),
    ("RES 1, H", "8"),
    ("RES 1, L", "8"),
    ("RES 2, A", "8"),
    ("RES 2, B", "8"),
    ("RES 2, C", "8"),
    ("RES 2, D", "8"),
    ("RES 2, E", "8"),
    ("RES 2, H", "8"),
    ("RES 2, L", "8"),
    ("RES 3, A", "8"),
    ("RES 3, B", "8"),
    ("RES 3, C", "8"),
    ("RES 3, D", "8"),
    ("RES 3, E", "8"),
    ("RES 3, H", "8"),
    ("RES 3, L", "8"),
    ("RES 4, A", "8"),
    ("RES 4, B", "8"),
    ("RES 4, C", "8"),
    ("RES 4, D", "8"),
    ("RES 4, E", "8"),
    ("RES 4, H", "8"),
    ("RES 4, L", "8"),
    ("RES 5, A", "8"),
    ("RES 5, B", "8"),
    ("RES 5, C", "8"),
    ("RES 5, D", "8"),
    ("RES 5, E", "8"),
    ("RES 5, H", "8"),
    ("RES 5, L", "8"),
    ("RES 6, A", "8"),
    ("RES 6, B", "8"),
    ("RES 6, C", "8"),
    ("RES 6, D", "8"),
    ("RES 6, E", "8"),
    ("RES 6, H", "8"),
    ("RES 6, L", "8"),
    ("RES 7, A", "8"),
    ("RES 7, B", "8"),
    ("RES 7, C", "8"),
    ("RES 7, D", "8"),
    ("RES 7, E", "8"),
    ("RES 7, H", "8"),
    ("RES 7, L", "8"),
    ("RET ", "10"),
    ("RET NZ", "11/5"),
    ("RET Z", "11/5"),
    ("RET NC", "11/5"),
    ("RET C", "11/5"),
    ("RET PO", "11/5"),
    ("RET PE", "11/5"),
    ("RET P", "11/5"),
    ("RET M", "11/5"),
    ("RETI ", "14"),
    ("RETN ", "14"),
    ("RLA ", "4"),
    ("RRA ", "4"),
    ("RLCA ", "4"),
    ("RRCA ", "4"),
    ("RR (HL)", "15"),
    ("RL (HL)", "15"),
    ("RR (IX+10)", "23"),
    ("RR (IX+0x10)", "23"),
    ("RR (IX+CONST)", "23"),
    ("RL (IX+10)", "23"),
    ("RL (IX+0x10)", "23"),
    ("RL (IX+CONST)", "23"),
    ("RR A", "8"),
    ("RR B", "8"),
    ("RR C", "8"),
    ("RR D", "8"),
    ("RR E", "8"),
    ("RR H", "8"),
    ("RR L", "8"),
    ("RL A", "8"),
    ("RL B", "8"),
    ("RL C", "8"),
    ("RL D", "8"),
    ("RL E", "8"),
    ("RL H", "8"),
    ("RL L", "8"),
    ("RRC (HL)", "15"),
    ("RLC (HL)", "15"),
    ("RRC (IX+10)", "23"),
    ("RRC (IX+0x10)", "23"),
    ("RRC (IX+CONST)", "23"),
    ("RLC (IX+10)", "23"),
    ("RLC (IX+0x10)", "23"),
    ("RLC (IX+CONST)", "23"),
    ("RRC A", "8"),
    ("RRC B", "8"),
    ("RRC C", "8"),
    ("RRC D", "8"),
    ("RRC E", "8"),
    ("RRC H", "8"),
    ("RRC L", "8"),
    ("RLC A", "8"),
    ("RLC B", "8"),
    ("RLC C", "8"),
    ("RLC D", "8"),
    ("RLC E", "8"),
    ("RLC H", "8"),
    ("RLC L", "8"),
    ("RRD ", "18"),
    ("RLD ", "18"),
    ("RST 00h", "11"),
    ("RST 08h", "11"),
    ("RST 10h", "11"),
    ("RST 18h", "11"),
    ("RST 20h", "11"),
    ("RST 28h", "11"),
    ("RST 30h", "11"),
    ("RST 38h", "11"),
    ("SBC A, (IX+10)", "19"),
    ("SBC A, (IX+0x10)", "19"),
    ("SBC A, (IX+CONST)", "19"),
    ("SBC A, 10", "7"),
    ("SBC A, 0x10", "7"),
    ("SBC A, CONST", "7"),
    ("SBC A, (HL)", "7"),
    ("SBC HL, BC", "15"),
    ("SBC HL, DE", "15"),
    ("SBC HL, HL", "15"),
    ("SBC HL, SP", "15"),
    ("SBC A", "4"),
    ("SBC B", "4"),
    ("SBC C", "4"),
    ("SBC D", "4"),
    ("SBC E", "4"),
    ("SBC H", "4"),
    ("SBC L", "4"),
    ("SCF ", "4"),
    ("SET 0, (HL)", "15"),
    ("SET 1, (HL)", "15"),
    ("SET 2, (HL)", "15"),
    ("SET 3, (HL)", "15"),
    ("SET 4, (HL)", "15"),
    ("SET 5, (HL)", "15"),
    ("SET 6, (HL)", "15"),
    ("SET 7, (HL)", "15"),
    ("SET 0, (IX+10)", "23"),
    ("SET 0, (IX+0x10)", "23"),
    ("SET 0, (IX+CONST)", "23"),
    ("SET 1, (IX+10)", "23"),
    ("SET 1, (IX+0x10)", "23"),
    ("SET 1, (IX+CONST)", "23"),
    ("SET 2, (IX+10)", "23"),
    ("SET 2, (IX+0x10)", "23"),
    ("SET 2, (IX+CONST)", "23"),
    ("SET 3, (IX+10)", "23"),
    ("SET 3, (IX+0x10)", "23"),
    ("SET 3, (IX+CONST)", "23"),
    ("SET 4, (IX+10)", "23"),
    ("SET 4, (IX+0x10)", "23"),
    ("SET 4, (IX+CONST)", "23"),
    ("SET 5, (IX+10)", "23"),
    ("SET 5, (IX+0x10)", "23"),
    ("SET 5, (IX+CONST)", "23"),
    ("SET 6, (IX+10)", "23"),
    ("SET 6, (IX+0x10)", "23"),
    ("SET 6, (IX+CONST)", "23"),
    ("SET 7, (IX+10)", "23"),
    ("SET 7, (IX+0x10)", "23"),
    ("SET 7, (IX+CONST)", "23"),
    ("SET 0, A", "8"),
    ("SET 0, B", "8"),
    ("SET 0, C", "8"),
    ("SET 0, D", "8"),
    ("SET 0, E", "8"),
    ("SET 0, H", "8"),
    ("SET 0, L", "8"),
    ("SET 1, A", "8"),
    ("SET 1, B", "8"),
    ("SET 1, C", "8"),
    ("SET 1, D", "8"),
    ("SET 1, E", "8"),
    ("SET 1, H", "8"),
    ("SET 1, L", "8"),
    ("SET 2, A", "8"),
    ("SET 2, B", "8"),
    ("SET 2, C", "8"),
    ("SET 2, D", "8"),
    ("SET 2, E", "8"),
    ("SET 2, H", "8"),
    ("SET 2, L", "8"),
    ("SET 3, A", "8"),
    ("SET 3, B", "8"),
    ("SET 3, C", "8"),
    ("SET 3, D", "8"),
    ("SET 3, E", "8"),
    ("SET 3, H", "8"),
    ("SET 3, L", "8"),
    ("SET 4, A", "8"),
    ("SET 4, B", "8"),
    ("SET 4, C", "8"),
    ("SET 4, D", "8"),
    ("SET 4, E", "8"),
    ("SET 4, H", "8"),
    ("SET 4, L", "8"),
    ("SET 5, A", "8"),
    ("SET 5, B", "8"),
    ("SET 5, C", "8"),
    ("SET 5, D", "8"),
    ("SET 5, E", "8"),
    ("SET 5, H", "8"),
    ("SET 5, L", "8"),
    ("SET 6, A", "8"),
    ("SET 6, B", "8"),
    ("SET 6, C", "8"),
    ("SET 6, D", "8"),
    ("SET 6, E", "8"),
    ("SET 6, H", "8"),
    ("SET 6, L", "8"),
    ("SET 7, A", "8"),
    ("SET 7, B", "8"),
    ("SET 7, C", "8"),
    ("SET 7, D", "8"),
    ("SET 7, E", "8"),
    ("SET 7, H", "8"),
    ("SET 7, L", "8"),
    ("SLA (HL)", "15"),
    ("SLA (IX+10)", "23"),
    ("SLA (IX+0x10)", "23"),
    ("SLA (IX+CONST)", "23"),
    ("SLA A", "8"),
    ("SLA B", "8"),
    ("SLA C", "8"),
    ("SLA D", "8"),
    ("SLA E", "8"),
    ("SLA H", "8"),
    ("SLA L", "8"),
    ("SLL (HL)", "15"),
    ("SLL (IX+10)", "23"),
    ("SLL (IX+0x10)", "23"),
    ("SLL (IX+CONST)", "23"),
    ("SLL A", "8"),
    ("SLL B", "8"),
    ("SLL C", "8"),
    ("SLL D", "8"),
    ("SLL E", "8"),
    ("SLL H", "8"),
    ("SLL L", "8"),
    ("SRA (HL)", "15"),
    ("SRA (IX+10)", "23"),
    ("SRA (IX+0x10)", "23"),
    ("SRA (IX+CONST)", "23"),
    ("SRA A", "8"),
    ("SRA B", "8"),
    ("SRA C", "8"),
    ("SRA D", "8"),
    ("SRA E", "8"),
    ("SRA H", "8"),
    ("SRA L", "8"),
    ("SRL (HL)", "15"),
    ("SRL (IX+10)", "23"),
    ("SRL (IX+0x10)", "23"),
    ("SRL (IX+CONST)", "23"),
    ("SRL A", "8"),
    ("SRL B", "8"),
    ("SRL C", "8"),
    ("SRL D", "8"),
    ("SRL E", "8"),
    ("SRL H", "8"),
    ("SRL L", "8"),
    ("SUB (IX+10)", "19"),
    ("SUB (IX+0x10)", "19"),
    ("SUB (IX+CONST)", "19"),
    ("SUB 10", "7"),
    ("SUB 0x10", "7"),
    ("SUB CONST", "7"),
    ("SUB (HL)", "7"),
    ("SUB A", "4"),
    ("SUB B", "4"),
    ("SUB C", "4"),
    ("SUB D", "4"),
    ("SUB E", "4"),
    ("SUB H", "4"),
    ("SUB L", "4"),
    ("XOR (IX+10)", "19"),
    ("XOR (IX+0x10)", "19"),
    ("XOR (IX+CONST)", "19"),
    ("XOR 10", "7"),
    ("XOR 0x10", "7"),
    ("XOR CONST", "7"),
    ("XOR (hl)", "7"),
    ("XOR A", "4"),
    ("XOR B", "4"),
    ("XOR C", "4"),
    ("XOR D", "4"),
    ("XOR E", "4"),
    ("XOR H", "4"),
    ("XOR L", "4"),
)


@pytest.fixture(scope="module")
def parser_table():
    yield Parser()


@pytest.mark.parametrize("instruction,cycles", data)
def test_lookup(instruction, cycles, parser_table):
    entry = parser_table.lookup(instruction)
    assert entry is not None, "Not found: {}".format(instruction)
    assert entry["cycles"] == cycles, "Failed: {} expected '{}' != found '{}'".format(instruction, cycles, entry["cycles"])


@pytest.mark.parametrize("line,operator", (
    ("foo: LD A, 1 ; load accumulator", "LD"),
    ("foo: CALL 0xABCD", "CALL"),
    ("foo: EI", "EI"),
    ("LD A, 1 ; load accumulator", "LD"),
    ("CALL 0xABCE", "CALL"),
    ("EI", "EI"),
    ("foo: ; some label", None),
    ("foo:", None),
    ("; some comment", None),
))
def test_extract_mnemonic(line, operator):
    assert Parser._extract_mnemonic(line) == operator


def test_extract_mnemonic_normalizes_operator():
    assert Parser._extract_mnemonic("call 0xabcd") == "CALL"