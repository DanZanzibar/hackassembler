import os
import hackassembler.code as code


def abs_file_path(cli_file_arg):
    cwd = os.getcwd()
    rough_file_path = os.path.join(cwd, os.path.expanduser(cli_file_arg))
    return os.path.normpath(rough_file_path)


def valid_A_command(command: str) -> bool:
    a_comm = False
    if command.startswith('@') and len(command) > 1:
        num_addr = command[1:].isdigit() and int(command[1:]) < 32768
        sym_addr = command[1].isalpha()
        a_comm = num_addr or sym_addr
    return a_comm


def valid_C_command(command: str) -> bool:
    rest_of_command, jump = command.partition(';')[::2]
    dest, comp = rest_of_command.rpartition('=')[::2]
    right_parts = (dest != '' or jump != '') and comp != ''
    valid_dest = dest in code.DEST_MNEMONICS
    valid_comp = comp in code.COMP_MNEMONICS
    valid_jump = jump in code.JUMP_MNEMONICS

    return right_parts and valid_dest and valid_comp and valid_jump


def valid_L_command(command: str) -> bool:
    parentheses = command.startswith('(') and command.endswith(')')
    return parentheses and command[1].isupper()


class Parser():

    def __init__(self, cli_file_arg: str):
        file_path = abs_file_path(cli_file_arg)
        with open(file_path, 'r') as asm_file:
            asm_contents = asm_file.read()

        rough_asm_lines = asm_contents.splitlines()
        clean_lines = [(line.split('//')[0]).strip()
                       for line in rough_asm_lines]

        self._asm_lines = [line for line in clean_lines
                           if line != '']
        self._current_index = 0
        self._max_index = len(self._asm_lines) - 1
        self.command = self._asm_lines[self._current_index]

    def has_more_commands(self):
        return self._current_index < self._max_index

    def advance(self):
        self._current_index += 1
        self.command = self._asm_lines[self._current_index]

    def command_type(self):
        c_type = None
        if valid_A_command(self.command):
            c_type = 'A_COMMAND'
        elif valid_C_command(self.command):
            c_type = 'C_COMMAND'
        elif valid_L_command(self.command):
            c_type = 'L_COMMAND'
        return c_type

    def symbol(self) -> str:
        symbol = None
        if self.command[1].isalpha():
            if self.command_type() == 'A_COMMAND':
                symbol = self.command[1:]
            elif self.command_type() == 'L_COMMAND':
                symbol = self.command[1:-1]
        return symbol

