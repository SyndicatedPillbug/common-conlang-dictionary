from kharvunic.evolution import EvolutionEngine


def test_engine_returns_result():
    engine = EvolutionEngine()
    result = engine.evolve('misericordia', 'temple')

    assert result.result
    assert result.ipa.startswith('/')
    assert len(result.trace) >= 1


def test_register_comparison():
    engine = EvolutionEngine()
    comparison = engine.compare_registers('caelestis')

    assert 'temple' in comparison
    assert 'boardroom' in comparison
    assert 'trade' in comparison
