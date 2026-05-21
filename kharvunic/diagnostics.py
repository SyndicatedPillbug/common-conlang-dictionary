from difflib import SequenceMatcher
from typing import Optional

MIN_RULE_APPLICATIONS = 2
MAX_SOURCE_SIMILARITY = 0.78

PASSING = 'passing'
WEAK = 'weak'
FAILING = 'failing'


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def _normalized(value: str) -> str:
    return value.lower().strip()


def classify_evolution(source: str, result: str, rule_applications: int, warnings: list[str]) -> str:
    """Classify root health for UI and diagnostic corpus reporting."""
    if _normalized(source) == _normalized(result) or rule_applications == 0:
        return FAILING
    if warnings:
        return WEAK
    return PASSING


def diagnose_evolution(
    source: str,
    result: str,
    trace,
    rule_count: Optional[int] = None,
    override_applied: bool = False,
) -> dict:
    """Return user-facing health diagnostics for an evolved form.

    ``rule_count`` counts mechanical sound-change rules. ``trace`` can include
    non-rule events such as overrides, so callers that know the fired rule list
    should pass its length to avoid treating an override as rule coverage.
    """
    applications = max(0, len(trace) - 1) if rule_count is None else max(0, rule_count)
    sim = similarity(source, result)

    warnings: list[str] = []

    if _normalized(source) == _normalized(result):
        warnings.append('Result is unchanged from source; the current rule set is insufficient for this root.')

    if applications == 0:
        warnings.append('No sound-change rules fired.')
    elif applications < MIN_RULE_APPLICATIONS:
        warnings.append('Very few sound-change rules fired.')

    if override_applied and applications == 0:
        warnings.append('Only an override changed the form; mechanical rule coverage is empty.')

    if sim >= MAX_SOURCE_SIMILARITY and _normalized(source) != _normalized(result):
        warnings.append('Result remains too close to source form.')

    health = classify_evolution(source, result, applications, warnings)

    return {
        'health': health,
        'rule_applications': applications,
        'source_similarity': round(sim, 3),
        'warnings': warnings,
    }
