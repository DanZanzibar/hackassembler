from sys import argv
import hackassembler.parser


test_parser = hackassembler.parser.Parser(argv[1])

print(test_parser.asm_lines)
