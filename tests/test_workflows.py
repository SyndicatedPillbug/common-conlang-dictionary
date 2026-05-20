from kharvunic.workflows import evolve_with_overrides
from kharvunic.domains import suggest_domains


def test_override_workflow_structure():
    result = evolve_with_overrides('misericordia', 'temple')

    assert 'result' in result
    assert 'ipa' in result
    assert 'trace' in result


def test_domain_suggestions():
    domains = suggest_domains('contract obligation debt')

    assert 'law' in domains or 'trade' in domains
