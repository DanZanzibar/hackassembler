DEFAULT_SYMBOLS = {
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
    'SCREEN': 16384,
    'KBD': 24576
    }


class SymbolTable():

    def __init__(self):
        self._table = DEFAULT_SYMBOLS
        self._next_ram_entry = 16

    def add_ROM_entry(self, symbol, address):
        self._table[symbol] = address

    def add_RAM_entry(self, symbol):
        self._table[symbol] = self._next_ram_entry
        self._next_ram_entry += 1

    def contains(self, symbol):
        return symbol in self._table

    def get_address(self, symbol):
        return self._table.get(symbol)

