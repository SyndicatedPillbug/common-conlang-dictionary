from difflib import SequenceMatcher


MIN_RULE_APPLICATIONS = 2
MAX_SOURCE_SIMILARITY = 0.78


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def diagnose_evolution(source: str, result: str, trace) -> dict:
    applications = max(0, len(trace) - 1)
    sim = similarity(source, result)

    warnings = []

    if applications == 0:
        warnings.append('No sound-change rules fired.')

    elif applications < MIN_RULE_APPLICATIONS:
        warnings.append('Very few sound-change rules fired.')

    if sim >= MAX_SOURCE_SIMILARITY:
        warnings.append('Result remains too close to source form.')

    return {
        'rule_applications': applications,
        'source_similarity': round(sim, 3),
        'warnings': warnings,
    }
