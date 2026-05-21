from pathlib import Path
import pandas as pd

from kharvunic.evolution_v2 import EvolutionEngineV2

DIAGNOSTIC_ROOTS = Path('data/diagnostic_roots.csv')


def run_diagnostics(path: Path = DIAGNOSTIC_ROOTS):
    roots = pd.read_csv(path).fillna('')
    engine = EvolutionEngineV2()

    rows = []

    for _, row in roots.iterrows():
        root = row['root']
        for register in ['temple', 'boardroom', 'trade']:
            result = engine.evolve(root, register)
            diag = result['diagnostics']
            rows.append({
                'root': root,
                'meaning': row['meaning'],
                'register': register,
                'result': result['result'],
                'ipa': result['ipa'],
                'rules_fired': len(result['rules_fired']),
                'source_similarity': diag['source_similarity'],
                'warnings': '; '.join(diag['warnings']),
            })

    return pd.DataFrame(rows)
