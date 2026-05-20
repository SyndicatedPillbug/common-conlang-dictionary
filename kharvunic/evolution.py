"""Lineage-aware evolution engine.

This module is intentionally explicit and inspectable.
Every transformation step is recorded.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List

from kharvunic.ipa import to_ipa
from kharvunic.models import EvolutionResult, EvolutionStep
from kharvunic.rule_library import load_rules, select_rules

RULE_PATH = Path('data/rules.csv')


class EvolutionEngine:
    """Apply ordered sound-change rules while preserving lineage trace."""

    def __init__(self, rule_path: Path | None = None):
        self.rule_path = rule_path or RULE_PATH
        self.rules = load_rules(self.rule_path)

    def evolve(self, source: str, register: str) -> EvolutionResult:
        assert source.strip(), 'Source root must not be empty'

        current = source.lower().strip()
        trace: List[EvolutionStep] = [
            EvolutionStep(
                stage='source',
                form=current,
                note='Initial source root',
            )
        ]

        applicable = select_rules(self.rules, register)

        for rule in applicable:
            updated = re.sub(rule.pattern, rule.replacement, current)

            if updated != current:
                trace.append(
                    EvolutionStep(
                        stage=rule.stage,
                        form=updated,
                        note=f'{rule.id}: {rule.description}',
                    )
                )
                current = updated

        ipa = to_ipa(current)

        return EvolutionResult(
            source=source,
            register=register,
            result=current,
            ipa=ipa,
            trace=trace,
        )

    def compare_registers(self, source: str) -> dict:
        """Return all register descendants side-by-side."""
        return {
            register: self.evolve(source, register)
            for register in ['temple', 'boardroom', 'trade']
        }
