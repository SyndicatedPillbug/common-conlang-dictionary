"""Serious v2 evolution engine.

This engine is stricter than the original prototype:
- it uses the richer v2 rule library by default
- it reports every rule that fired
- it attaches diagnostics directly to output
- it supports override-aware final forms

The goal is to make obvious when a word has NOT meaningfully evolved.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List

from kharvunic.ipa import to_ipa
from kharvunic.models import EvolutionStep
from kharvunic.rule_library import load_rules, select_rules
from kharvunic.overrides import find_override
from kharvunic.diagnostics import diagnose_evolution

RULE_PATH_V2 = Path('data/rules_v2.csv')


class EvolutionEngineV2:
    """Apply richer staged rules and expose diagnostics."""

    def __init__(self, rule_path: Path | None = None):
        self.rule_path = rule_path or RULE_PATH_V2
        self.rules = load_rules(self.rule_path)

    def evolve(self, source: str, register: str):
        assert source.strip(), 'Source root must not be empty'
        assert register in {'temple', 'boardroom', 'trade'}, f'Unsupported register: {register}'

        current = source.lower().strip()
        trace: List[EvolutionStep] = [
            EvolutionStep('source', current, 'Initial source root')
        ]

        fired = []

        for rule in select_rules(self.rules, register):
            updated = re.sub(rule.pattern, rule.replacement, current)
            if updated != current:
                current = updated
                fired.append(rule.id)
                trace.append(
                    EvolutionStep(
                        stage=rule.stage,
                        form=current,
                        note=f'{rule.id}: {rule.description}',
                    )
                )

        mechanical = current
        override = find_override(source, register)

        if override:
            final = override['override']
            trace.append(
                EvolutionStep(
                    stage='override',
                    form=final,
                    note=override['reason'],
                )
            )
            override_applied = True
            override_reason = override['reason']
        else:
            final = mechanical
            override_applied = False
            override_reason = ''

        diagnostics = diagnose_evolution(source, final, trace)

        return {
            'source': source,
            'register': register,
            'mechanical_result': mechanical,
            'result': final,
            'ipa': to_ipa(final),
            'trace': trace,
            'rules_fired': fired,
            'override_applied': override_applied,
            'override_reason': override_reason,
            'diagnostics': diagnostics,
        }

    def compare(self, source: str):
        return {
            register: self.evolve(source, register)
            for register in ['temple', 'boardroom', 'trade']
        }
