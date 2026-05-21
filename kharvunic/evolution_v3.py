"""Epochal v3 evolution engine.

This engine is intentionally more aggressive than v2.
It models four 5,000-year passes and uses seeded variation so forms
are reproducible but not perfectly uniform.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List

from kharvunic.fractal import FractalChoice
from kharvunic.ipa import to_ipa
from kharvunic.diagnostics import diagnose_evolution


def _visible_rule_notes(trace: List[V3Step]) -> list[str]:
    """Return notes from epochs that actually changed the surface form."""
    return [step.note for step in trace[1:] if step.note and step.note != 'no visible change']


@dataclass(frozen=True)
class V3Step:
    epoch: str
    form: str
    note: str


def normalize_source(text: str) -> str:
    out = text.lower().strip()
    out = out.replace('ñ', 'ny')
    out = out.replace('á', 'a').replace('é', 'e').replace('í', 'i')
    out = out.replace('ó', 'o').replace('ú', 'u')
    out = out.replace('qu', 'k')
    out = out.replace('ç', 's')
    return out


def collapse_repeats(text: str) -> str:
    return re.sub(r'([aeiou])\1+', r'\1', text)


def epoch_1_inherited(form: str, fc: FractalChoice) -> tuple[str, List[str]]:
    notes = []
    changes = [
        (r'ae', 'e', 'collapse ae'),
        (r'oe', 'e', 'collapse oe'),
        (r'c(?=[eiy])', 'sh', 'palatalize soft c'),
        (r'g(?=[eiy])', 'zh', 'palatalize soft g'),
        (r'ti', 'sh', 'ti > sh'),
        (r'ct', 'kt', 'ct > kt'),
        (r'mb', 'mv', 'mb > mv'),
        (r'nd', 'dh', 'nd > dh'),
        (r'ar(e)?$', 'ar', 'reduce -are'),
        (r'er(e)?$', 'er', 'reduce -ere'),
        (r'ir(e)?$', 'ir', 'reduce -ire'),
    ]
    for pattern, repl, note in changes:
        new = re.sub(pattern, repl, form)
        if new != form:
            form = new
            notes.append(note)

    if fc.chance(1, 'unstressed_initial_a', 0.22):
        new = re.sub(r'^a(?=.)', 'e', form)
        if new != form:
            form = new
            notes.append('initial a weakens to e')

    return form, notes


def epoch_2_contact(form: str, fc: FractalChoice) -> tuple[str, List[str]]:
    notes = []

    if fc.chance(2, 'ny_shift', 0.72):
        repl = fc.choose(2, 'ny_reflex', ['nh', 'ny', 'n'])
        new = form.replace('ny', repl)
        if new != form:
            form = new
            notes.append(f'ny contact reflex > {repl}')

    if fc.chance(2, 'intervocalic_lenition', 0.55):
        new = re.sub(r'([aeiou])b([aeiou])', r'\1v\2', form)
        new = re.sub(r'([aeiou])d([aeiou])', r'\1dh\2', new)
        new = re.sub(r'([aeiou])g([aeiou])', r'\1gh\2', new)
        if new != form:
            form = new
            notes.append('intervocalic lenition')

    if fc.chance(2, 'liquid_metathesis', 0.25):
        new = re.sub(r'([aeiou])r([aeiou])', r'\1rh\2', form)
        if new != form:
            form = new
            notes.append('rhotic sacralization')

    return form, notes


def epoch_3_imperial(form: str, fc: FractalChoice, register: str) -> tuple[str, List[str]]:
    notes = []

    # Institutional compression removes weak final vowels.
    new = re.sub(r'[aeo]$', '', form)
    if new != form:
        form = new
        notes.append('final weak vowel loss')

    # Open repeated a/a patterns collapse under imperial standard speech.
    if fc.chance(3, 'a_reduction', 0.70):
        new = re.sub(r'a([^aeiou]{0,2})a', r'a\1e', form)
        if new != form:
            form = new
            notes.append('repeated a-pattern partially fronts')

    if register == 'boardroom':
        new = form.replace('kt', 'kr').replace('dh', 'd')
        if new != form:
            form = new
            notes.append('Boardroom hardening and cleanup')

    return form, notes


def epoch_4_register(form: str, fc: FractalChoice, register: str) -> tuple[str, List[str]]:
    notes = []

    if register == 'temple':
        if form.endswith('ar'):
            form = form[:-2] + 'ār'
            notes.append('Temple final ar lengthening')
        elif form.endswith('er'):
            form = form[:-2] + 'ēr'
            notes.append('Temple final er lengthening')
        elif fc.chance(4, 'temple_vowel_restoration', 0.35):
            form = form + fc.choose(4, 'temple_appendix', ['a', 'e'])
            notes.append('Temple restores final chant vowel')

    elif register == 'trade':
        new = form.replace('sh', 's').replace('zh', 'j').replace('kh', 'k')
        new = re.sub(r'[āēīōū]', lambda m: {'ā':'a','ē':'e','ī':'i','ō':'o','ū':'u'}[m.group(0)], new)
        new = re.sub(r'(ar|er|ir)$', '', new)
        if new != form:
            form = new
            notes.append('Trade simplification and clipping')

    elif register == 'boardroom':
        new = re.sub(r'(ar|er|ir)$', lambda m: m.group(0)[0], form)
        if new != form:
            form = new
            notes.append('Boardroom clipped verbal ending')

    form = collapse_repeats(form)
    return form, notes


class EvolutionEngineV3:
    def evolve(self, source: str, meaning: str = '', register: str = 'temple', seed: str = 'commonwealth'):
        assert source.strip(), 'source must not be empty'
        assert register in {'temple', 'boardroom', 'trade'}, f'unsupported register: {register}'

        fc = FractalChoice(source, meaning, register, seed)
        current = normalize_source(source)
        trace: List[V3Step] = [V3Step('source', current, 'normalized source')]
        mechanical_result = current

        for label, func in [
            ('epoch 1: early divergence', epoch_1_inherited),
            ('epoch 2: expansion contact', epoch_2_contact),
        ]:
            before = current
            current, notes = func(current, fc)
            note = '; '.join(notes) if notes else 'no visible change'
            trace.append(V3Step(label, current, note))
            if current != before:
                mechanical_result = current

        before = current
        current, notes = epoch_3_imperial(current, fc, register)
        note = '; '.join(notes) if notes else 'no visible change'
        trace.append(V3Step('epoch 3: imperial standardization', current, note))
        if current != before:
            mechanical_result = current

        before = current
        current, notes = epoch_4_register(current, fc, register)
        note = '; '.join(notes) if notes else 'no visible change'
        trace.append(V3Step('epoch 4: register split', current, note))
        if current != before:
            mechanical_result = current

        rules_fired = _visible_rule_notes(trace)

        diagnostics = diagnose_evolution(
            source,
            current,
            trace,
            rule_count=len(rules_fired),
            override_applied=False,
        )

        return {
            'source': source,
            'meaning': meaning,
            'register': register,
            'mechanical_result': mechanical_result,
            'result': current,
            'ipa': to_ipa(current),
            'trace': trace,
            'rules_fired': rules_fired,
            'override_applied': False,
            'override_reason': '',
            'diagnostics': diagnostics,
        }

    def compare(self, source: str, meaning: str = '', seed: str = 'commonwealth'):
        return {
            register: self.evolve(source, meaning, register, seed)
            for register in ['temple', 'boardroom', 'trade']
        }
