import hashlib
import random


def seed_for(*parts) -> int:
    joined = '::'.join(str(p) for p in parts)
    digest = hashlib.sha256(joined.encode('utf-8')).hexdigest()
    return int(digest[:16], 16)


class FractalChoice:
    """Seeded variation helper.

    This is not true mathematical fractal generation yet.
    It is a reproducible organic variation layer that lets the same
    root/register/epoch make consistent non-uniform choices.
    """

    def __init__(self, source: str, meaning: str, register: str, seed: str = 'commonwealth'):
        self.source = source
        self.meaning = meaning
        self.register = register
        self.seed = seed

    def rng(self, epoch: int, channel: str):
        return random.Random(seed_for(self.source, self.meaning, self.register, self.seed, epoch, channel))

    def chance(self, epoch: int, channel: str, probability: float) -> bool:
        probability = max(0.0, min(1.0, probability))
        return self.rng(epoch, channel).random() < probability

    def choose(self, epoch: int, channel: str, options):
        assert options, 'FractalChoice.choose requires at least one option'
        return self.rng(epoch, channel).choice(list(options))
