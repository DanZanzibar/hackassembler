import os


def abs_file_path(cli_file_arg):
    cwd = os.getcwd()
    rough_file_path = os.path.join(cwd, cli_file_arg)
    return os.path.normpath(rough_file_path)


def valid_A_command(command: str) -> bool:
    num_addr = command[1:].isdigit()
    sym_addr = not command[1].isdigit()
    return command.startswith('@') and (num_addr or sym_addr)


def valid_C_command_sep(command: str) -> bool:
    right_order = True
    if '=' in command and ';' in command:
        right_order = command.index('=') < command.index(';')
    at_least_one = '=' in command or ';' in command
    return right_order and at_least_one


def valid_C_command_dest(command: str) -> bool:
    dest = command.split('=')[0]
    return all(c in ('A', 'D', 'M') for c in dest) if '=' in command else True


def 


class Parser():

    def __init__(self, cli_file_arg:str):
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

    def has_more_commands(self):
        return self._current_index < self._max_index

    def advance(self):
        self._current_index += 1

    def 
