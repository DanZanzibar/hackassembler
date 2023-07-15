class SymbolTable():

    def __init__(self):
        self._table = {}

    def add_entry(self, symbol, address):
        self._table[symbol] = address

    
