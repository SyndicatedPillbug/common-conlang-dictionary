"""Temple/Common rhythm analysis.

Not a full phonology engine yet.
This module provides:
- syllable estimation
- stress approximation
- cadence/rhythm hints
- line scanning support
"""

from __future__ import annotations

import re

VOWELS = 'aeiouāēīōūãõĩ'


def count_syllables(word: str) -> int:
    groups = re.findall(rf'[{VOWELS}]+', word.lower())
    return max(1, len(groups))


def estimate_stress(word: str) -> str:
    """Very rough penultimate stress model.

    Later:
    - long-vowel weighting
    - sacred exceptions
    - Trade Common stress erosion
    """
    syllables = re.findall(rf'[{VOWELS}]+|[^{VOWELS}]+', word.lower())

    vowel_positions = [
        i for i, chunk in enumerate(syllables)
        if any(ch in VOWELS for ch in chunk)
    ]

    if not vowel_positions:
        return word

    target = vowel_positions[-2] if len(vowel_positions) > 1 else vowel_positions[0]

    out = []
    for i, chunk in enumerate(syllables):
        if i == target:
            out.append(chunk.upper())
        else:
            out.append(chunk)

    return ''.join(out)


def scan_line(line: str) -> dict:
    words = [w for w in re.split(r'\s+', line.strip()) if w]

    syllables = sum(count_syllables(word) for word in words)

    stressed = [estimate_stress(word) for word in words]

    cadence = 'heavy'
    if line.endswith(('a', 'e', 'i', 'o', 'u', 'ā', 'ē', 'ī', 'ō', 'ū')):
        cadence = 'open'

    return {
        'words': words,
        'syllables': syllables,
        'stress': stressed,
        'cadence': cadence,
    }
