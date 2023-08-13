import hackassembler.code
import hackassembler.symbol


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
    valid_dest = dest in hackassembler.code.DEST_MNEMONICS
    valid_comp = comp in hackassembler.code.COMP_MNEMONICS
    valid_jump = jump in hackassembler.code.JUMP_MNEMONICS

    return right_parts and valid_dest and valid_comp and valid_jump


def valid_L_command(command: str) -> bool:
    parentheses = command.startswith('(') and command.endswith(')')
    return parentheses and command[1].isalpha()


def add_leading_zeros(string, num_digits: int) -> str:
    num_zeros = num_digits - len(string)
    zeros = num_zeros * '0'
    return zeros + string


def int_to_binary(decimal: int, num_digits: int) -> str:
    bin_string = format(decimal, 'b')
    return add_leading_zeros(bin_string, num_digits)


def str_to_binary(string: str, num_digits: int) -> str:
    return int_to_binary(int(string), num_digits)


class Parser():

    def __init__(self, file_path: str):
        with open(file_path, 'r') as asm_file:
            asm_contents = asm_file.read()

        rough_asm_lines = asm_contents.splitlines()
        clean_lines = [(line.split('//')[0]).strip()
                       for line in rough_asm_lines]

        self._asm_lines = [line for line in clean_lines
                           if line != '']
        self._current_index = 0
        self._num_commands = len(self._asm_lines)
        self.sym_tab = hackassembler.symbol.SymbolTable()

    def has_more_commands(self):
        return self._current_index < self._num_commands

    def command(self):
        return self._asm_lines[self._current_index]

    def advance(self):
        self._current_index += 1

    def reset(self):
        self._current_index = 0

    def command_type(self):
        c_type = None
        if valid_A_command(self.command()):
            c_type = 'A_COMMAND'
        elif valid_C_command(self.command()):
            c_type = 'C_COMMAND'
        elif valid_L_command(self.command()):
            c_type = 'L_COMMAND'
        return c_type

    def symbol(self) -> str:
        symbol = None
        if self.command()[1].isalpha():
            if self.command_type() == 'A_COMMAND':
                symbol = self.command()[1:]
            elif self.command_type() == 'L_COMMAND':
                symbol = self.command()[1:-1]
        return symbol

    def get_L_command_symbols(self):
        L_count = 0
        for line_num in range(len(self._asm_lines)):
            if self.command_type() == 'L_COMMAND':
                symbol = self.symbol()
                if self.sym_tab.contains(symbol):
                    raise ValueError(f'Line {line_num} symbol not unique.')
                self.sym_tab.add_ROM_entry(symbol, line_num - L_count)
                L_count += 1
            self.advance()
        self.reset()

    def _translate_a_command(self) -> str:
        command = self.command()
        if (symbol := self.symbol()):
            if not self.sym_tab.contains(symbol):
                self.sym_tab.add_RAM_entry(symbol)
            address = int_to_binary(self.sym_tab.get_address(symbol), 16)
        else:
            address = str_to_binary(command[1:], 16)
        return address

    def _translate_c_command(self) -> str:
        command = self.command()
        rest_of_command, jump = command.partition(';')[::2]
        dest, comp = rest_of_command.rpartition('=')[::2]
        comp = hackassembler.code.COMP_MNEMONICS[comp]
        dest = hackassembler.code.DEST_MNEMONICS[dest]
        jump = hackassembler.code.JUMP_MNEMONICS[jump]
        return '111' + comp + dest + jump

    def translate_line(self) -> str:
        command = self.command()
        trans = None
        if valid_A_command(command):
            trans = self._translate_a_command() + '\n'
        elif valid_C_command(command):
            trans = self._translate_c_command() + '\n'
        return trans
