import re
import pandas as pd
from kharvunic.rules import RULES

class Evolver:
    def __init__(self):
        self.rules = RULES

    def evolve(self, word, register='common'):
        result = word.lower()
        trace = [result]

        for pattern, repl in self.rules['common']:
            result = re.sub(pattern, repl, result)

        if register in self.rules:
            for pattern, repl in self.rules[register]:
                result = re.sub(pattern, repl, result)

        trace.append(result)
        return {
            'source': word,
            'register': register,
            'result': result,
            'trace': trace
        }

if __name__ == '__main__':
    e = Evolver()
    print(e.evolve('misericordia', 'temple'))
