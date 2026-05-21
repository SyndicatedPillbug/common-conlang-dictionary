from kharvunic.evolution_v3 import EvolutionEngineV3


def test_manana_does_not_silently_pass_through():
    engine = EvolutionEngineV3()
    result = engine.evolve('mañana', 'morning', 'temple')

    assert result['result'] != 'mañana'
    assert result['result'] != 'mañan'
    assert result['diagnostics']['health'] in {'passing', 'weak'}
    assert len(result['rules_fired']) >= 2


def test_ambulare_gets_epochal_lineage():
    engine = EvolutionEngineV3()
    result = engine.evolve('ambulare', 'walk', 'temple')

    assert result['result'] != 'ambulare'
    assert len(result['trace']) == 5
    assert len(result['rules_fired']) >= 2


def test_compare_returns_three_registers():
    engine = EvolutionEngineV3()
    comparison = engine.compare('misericordia', 'mercy')

    assert set(comparison) == {'temple', 'boardroom', 'trade'}
    assert all(value['result'] for value in comparison.values())
