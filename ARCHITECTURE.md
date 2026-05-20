# Architecture

The Kharvunic engine is intentionally modular.

The project is expected to evolve into:
- Temple Common tooling
- Boardroom Common tooling
- Trade Common tooling
- historical reconstruction
- poetic/meter-aware generation
- diachronic linguistic tracing
- lexical drift simulation
- IPA/stress modeling

The codebase therefore prioritizes:
- readability over cleverness
- explicit transformation stages
- strong assertions
- small isolated modules
- reproducible outputs
- editable rule systems

## Core Modules

### `engine.py`
Primary transformation pipeline.

### `rules.py`
Sound shifts and register evolution rules.

### `registers.py`
Metadata and future register-specific behaviors.

### `ipa.py`
Orthography -> IPA conversion.

### `dictionary.py`
Persistent lexicon storage and lookup.

### `models.py`
Strong typed data models and assertions.

## Design Principles

1. Every generated form should be traceable.
2. No arbitrary root invention.
3. Temple/Common/Boardroom divergence should be configurable.
4. Liturgical restoration should exist separately from natural erosion.
5. Trade Common should eventually support contact-language drift.
6. Outputs should be inspectable stage-by-stage.
7. The dictionary becomes canonical over time.

## Future Features

- probabilistic sound drift
- poetic meter validation
- stress modeling
- historical reconstruction mode
- root ancestry graphs
- semantic clustering
- multi-stage timeline evolution
- automatic liturgical restoration
- Trade Common creolization layer
