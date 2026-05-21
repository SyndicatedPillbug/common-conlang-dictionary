"""Editable sound-change rule library.

Rules are stored as CSV so the Streamlit app can view, edit, enable,
disable, and reorder them without touching Python source code.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

import pandas as pd

RULE_COLUMNS = [
    "id",
    "stage",
    "register",
    "order",
    "enabled",
    "pattern",
    "replacement",
    "description",
    "attribution",
]


@dataclass(frozen=True)
class Rule:
    id: str
    stage: str
    register: str
    order: int
    enabled: bool
    pattern: str
    replacement: str
    description: str = ""
    attribution: str = ""

    def __post_init__(self) -> None:
        assert self.id, "Rule.id must not be empty"
        assert self.stage, "Rule.stage must not be empty"
        assert self.register, "Rule.register must not be empty"
        assert isinstance(self.order, int), "Rule.order must be an integer"
        assert self.pattern != "", "Rule.pattern must not be empty"
        re.compile(self.pattern)


def _coerce_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def ensure_rule_file(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        pd.DataFrame(columns=RULE_COLUMNS).to_csv(path, index=False)


def load_rules(path: Path) -> List[Rule]:
    ensure_rule_file(path)
    df = pd.read_csv(path).fillna("")
    missing = set(RULE_COLUMNS) - set(df.columns)
    assert not missing, f"Rule file missing columns: {sorted(missing)}"

    rules: List[Rule] = []
    for _, row in df.iterrows():
        rules.append(
            Rule(
                id=str(row["id"]),
                stage=str(row["stage"]),
                register=str(row["register"]),
                order=int(row["order"]),
                enabled=_coerce_bool(row["enabled"]),
                pattern=str(row["pattern"]),
                replacement=str(row["replacement"]),
                description=str(row["description"]),
                attribution=str(row["attribution"]),
            )
        )
    return sorted(rules, key=lambda rule: (rule.order, rule.stage, rule.register, rule.id))


def save_rules(path: Path, rules_df: pd.DataFrame) -> None:
    missing = set(RULE_COLUMNS) - set(rules_df.columns)
    assert not missing, f"Cannot save rules; missing columns: {sorted(missing)}"
    for _, row in rules_df.fillna("").iterrows():
        Rule(
            id=str(row["id"]),
            stage=str(row["stage"]),
            register=str(row["register"]),
            order=int(row["order"]),
            enabled=_coerce_bool(row["enabled"]),
            pattern=str(row["pattern"]),
            replacement=str(row["replacement"]),
            description=str(row["description"]),
            attribution=str(row["attribution"]),
        )
    rules_df[RULE_COLUMNS].sort_values(["order", "stage", "register", "id"]).to_csv(path, index=False)


def select_rules(rules: Iterable[Rule], register: str) -> List[Rule]:
    """Return enabled rules that apply globally or to the requested register."""
    selected = [
        rule for rule in rules
        if rule.enabled and rule.register in {"all", register}
    ]
    return sorted(selected, key=lambda rule: (rule.order, rule.stage, rule.register, rule.id))
