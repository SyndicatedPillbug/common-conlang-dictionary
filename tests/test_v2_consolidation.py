import pandas as pd
import pytest

from kharvunic.diagnostic_runner import run_diagnostics
from kharvunic.domains import suggest_domains
from kharvunic.evolution_v2 import EvolutionEngineV2
from kharvunic.workflows import save_blocker_reason, save_evolution_result, save_word_entry


def test_ambulare_temple_evolves_to_expected_v2_form():
    engine = EvolutionEngineV2()
    result = engine.evolve('ambulare', 'temple')
    forms = [step.form for step in result['trace']]
    joined_notes = '\n'.join(step.note for step in result['trace'])

    assert result['result'] == 'amvulār'
    assert result['diagnostics']['health'] == 'passing'
    assert result['diagnostics']['warnings'] == []
    assert result['result'] != 'ambulār'
    assert result['rules_fired'] == ['c090', 'c140', 't010']
    assert forms == ['ambulare', 'amvulare', 'amvular', 'amvulār']
    assert 'c090' in joined_notes
    assert 'c140' in joined_notes
    assert 't010' in joined_notes
    assert 't040' not in joined_notes


def test_ambulare_does_not_silently_pass_as_unchanged_source():
    engine = EvolutionEngineV2()
    result = engine.evolve('ambulare', 'temple')

    unchanged = result['result'].lower() == 'ambulare'
    warnings = result['diagnostics']['warnings']

    assert len(result['trace']) > 1 or warnings
    assert not (unchanged and not warnings)


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


def test_explicit_override_can_be_canonical_saveable():
    result = EvolutionEngineV2().evolve('misericordia', 'temple')

    assert result['override_applied'] is True
    assert result['result'] == 'mezhera'
    assert result['diagnostics']['health'] == 'passing'
    assert result['diagnostics']['warnings'] == []
    assert save_blocker_reason(result) == ''


def test_weak_or_failing_results_are_not_canonical_saveable():
    weak_result = {
        'diagnostics': {
            'health': 'weak',
            'warnings': ['Result remains too close to source form.'],
        }
    }

    blocker = save_blocker_reason(weak_result)

    assert blocker
    assert 'not passing' in blocker


def test_save_evolution_result_rejects_weak_candidate(tmp_path):
    dictionary_path = tmp_path / 'dictionary.csv'
    history_path = tmp_path / 'dictionary_history.csv'
    dictionary_path.write_text('word,ipa,register,meaning,source_root,domain,notes\n')

    weak_result = {
        'result': 'ambulār',
        'ipa': '/ambulaːr/',
        'register': 'temple',
        'source': 'ambulare',
        'diagnostics': {
            'health': 'weak',
            'warnings': ['Result remains too close to source form.'],
        },
    }

    with pytest.raises(ValueError):
        save_evolution_result(
            result=weak_result,
            meaning='walk',
            domain='body',
            path=dictionary_path,
            history_path=history_path,
        )

    dictionary = pd.read_csv(dictionary_path).fillna('')
    assert dictionary.empty
    assert not history_path.exists()


def test_walk_domain_is_suggested_for_save_form_defaults():
    assert suggest_domains('walk') == ['body']


def test_diagnostic_runner_reports_root_health():
    results = run_diagnostics()

    assert {'root', 'register', 'health', 'warnings'}.issubset(results.columns)
    assert set(results['health']).issubset({'passing', 'weak', 'failing'})
    assert 'ambulare' in set(results['root'])

    ambulare_temple = results[
        (results['root'] == 'ambulare') &
        (results['register'] == 'temple')
    ].iloc[0]
    assert ambulare_temple['result'] == 'amvulār'
    assert ambulare_temple['health'] == 'passing'


def test_save_v2_entry_writes_dictionary_and_history(tmp_path):
    dictionary_path = tmp_path / 'dictionary.csv'
    history_path = tmp_path / 'dictionary_history.csv'
    dictionary_path.write_text('word,ipa,register,meaning,source_root,domain,notes\n')

    result = EvolutionEngineV2().evolve('ambulare', 'temple')

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


def test_save_evolution_result_accepts_passing_candidate(tmp_path):
    dictionary_path = tmp_path / 'dictionary.csv'
    history_path = tmp_path / 'dictionary_history.csv'
    dictionary_path.write_text('word,ipa,register,meaning,source_root,domain,notes\n')

    result = EvolutionEngineV2().evolve('ambulare', 'temple')

    saved = save_evolution_result(
        result=result,
        meaning='walk',
        domain='body',
        notes='canonical v2 save',
        path=dictionary_path,
        history_path=history_path,
        reason='test canonical v2 result save',
    )

    assert saved['word'] == 'amvulār'
    dictionary = pd.read_csv(dictionary_path).fillna('')
    assert dictionary.iloc[0]['word'] == 'amvulār'
