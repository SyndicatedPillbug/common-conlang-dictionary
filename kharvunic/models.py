from dataclasses import dataclass, field
from typing import List


VALID_REGISTERS = {'temple', 'boardroom', 'trade', 'common'}


@dataclass(frozen=True)
class EvolutionStep:
    """One visible step in a word's diachronic evolution."""

    stage: str
    form: str
    note: str = ''

    def __post_init__(self):
        assert self.stage, 'EvolutionStep.stage must not be empty'
        assert self.form, 'EvolutionStep.form must not be empty'


@dataclass(frozen=True)
class EvolutionResult:
    """Complete output from evolving one source form into one register."""

    source: str
    register: str
    result: str
    ipa: str
    trace: List[EvolutionStep] = field(default_factory=list)

    def __post_init__(self):
        assert self.source, 'EvolutionResult.source must not be empty'
        assert self.register in VALID_REGISTERS, f'Unknown register: {self.register}'
        assert self.result, 'EvolutionResult.result must not be empty'
        assert self.ipa.startswith('/') and self.ipa.endswith('/'), 'IPA must be slash-delimited'


@dataclass(frozen=True)
class DictionaryEntry:
    """One stored dictionary entry."""

    word: str
    ipa: str
    register: str
    meaning: str
    source_root: str
    notes: str = ''

    def __post_init__(self):
        assert self.word, 'DictionaryEntry.word must not be empty'
        assert self.register in VALID_REGISTERS, f'Unknown register: {self.register}'
        assert self.meaning, 'DictionaryEntry.meaning must not be empty'
        assert self.source_root, 'DictionaryEntry.source_root must not be empty'
