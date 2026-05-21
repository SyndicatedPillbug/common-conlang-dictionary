import pandas as pd

from kharvunic.diagnostic_runner import run_diagnostics
from kharvunic.evolution_v2 import EvolutionEngineV2
from kharvunic.workflows import save_word_entry


def test_ambulare_does_not_silently_pass_as_success():
    engine = EvolutionEngineV2()
    result = engine.evolve('ambulare', 'temple')

    warnings = result['diagnostics']['warnings']
    unchanged = result['result'].lower() == 'ambulare'

    assert len(result['trace']) > 1 or warnings
    assert not (unchanged and not warnings)


def test_ambulare_has_visible_v2_lineage_when_rules_apply():
    engine = EvolutionEngineV2()
    result = engine.evolve('ambulare', 'temple')
    forms = [step.form for step in result['trace']]
    notes = [step.note for step in result['trace']]

    assert forms[0] == 'ambulare'
    assert result['result'] != 'ambulare' or result['diagnostics']['warnings']
    joined_notes = '\n'.join(notes)
    assert 'c090' in joined_notes
    assert 'c140' in joined_notes
    assert 't010' in joined_notes


def test_compare_registers_returns_all_v2_diagnostics():
    engine = EvolutionEngineV2()
    comparison = engine.compare('misericordia')

    assert set(comparison) == {'temple', 'boardroom', 'trade'}
    assert all('diagnostics' in result for result in comparison.values())
    assert all('health' in result['diagnostics'] for result in comparison.values())

    outputs = {result['result'] for result in comparison.values()}
    warnings = [
        warning
        for result in comparison.values()
        for warning in result['diagnostics']['warnings']
    ]
    assert len(outputs) > 1 or warnings


def test_diagnostic_runner_reports_root_health():
    results = run_diagnostics()

    assert {'root', 'register', 'health', 'warnings'}.issubset(results.columns)
    assert set(results['health']).issubset({'passing', 'weak', 'failing'})
    assert 'ambulare' in set(results['root'])


def test_save_v2_entry_writes_dictionary_and_history(tmp_path):
    dictionary_path = tmp_path / 'dictionary.csv'
    history_path = tmp_path / 'dictionary_history.csv'
    dictionary_path.write_text('word,ipa,register,meaning,source_root,domain,notes\n')

    engine = EvolutionEngineV2()
    result = engine.evolve('ambulare', 'temple')

    saved = save_word_entry(
        word=result['result'],
        ipa=result['ipa'],
        register=result['register'],
        meaning='walk',
        source_root=result['source'],
        domain='body',
        notes='test save from v2 result',
        path=dictionary_path,
        history_path=history_path,
        reason='test v2 save workflow',
    )

    dictionary = pd.read_csv(dictionary_path).fillna('')
    history = pd.read_csv(history_path).fillna('')

    assert saved['word'] == result['result']
    assert dictionary.iloc[0]['word'] == result['result']
    assert dictionary.iloc[0]['ipa'] == result['ipa']
    assert dictionary.iloc[0]['register'] == 'temple'
    assert dictionary.iloc[0]['meaning'] == 'walk'
    assert dictionary.iloc[0]['source_root'] == 'ambulare'
    assert dictionary.iloc[0]['domain'] == 'body'
    assert history.iloc[0]['word'] == result['result']
    assert history.iloc[0]['reason'] == 'test v2 save workflow'
