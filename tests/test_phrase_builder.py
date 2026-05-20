from kharvunic.phrase_builder import analyze_phrase


def test_phrase_analysis():
    result = analyze_phrase('Rhesht plorēsh lakrem vel lath')

    assert result['syllables'] > 0
    assert result['ipa']
    assert result['cadence'] in {'heavy', 'open'}
