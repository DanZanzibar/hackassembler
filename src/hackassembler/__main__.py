from sys import argv
import os
import hackassembler.parser


def abs_file_path(cli_file_arg):
    cwd = os.getcwd()
    rough_file_path = os.path.join(cwd, os.path.expanduser(cli_file_arg))
    return os.path.normpath(rough_file_path)


asm_file_path = abs_file_path(argv[1])
asm_file_name = os.path.basename(asm_file_path)
dir_path = os.path.dirname(asm_file_path)
hack_file_name = asm_file_name.split('.')[0] + '.hack'
hack_file_path = os.path.join(dir_path, hack_file_name)

parser = hackassembler.parser.Parser(asm_file_path)

parser.get_L_command_symbols()

output = ''

while parser.has_more_commands():
    if parser.translate_line():
        output += parser.translate_line()
    parser.advance()

with open(hack_file_path, 'w') as hack_file:
    hack_file.write(output)
