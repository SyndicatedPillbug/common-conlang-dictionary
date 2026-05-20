from kharvunic.evolution import EvolutionEngine


def compare_registers(source_root: str):
    engine = EvolutionEngine()

    out = {}

    for register in ['temple', 'boardroom', 'trade']:
        result = engine.evolve(source_root, register)
        out[register] = {
            'result': result.result,
            'ipa': result.ipa,
            'trace': [
                {
                    'stage': step.stage,
                    'form': step.form,
                    'note': step.note,
                }
                for step in result.trace
            ],
        }

    return out
