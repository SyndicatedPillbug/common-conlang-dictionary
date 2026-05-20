DIGRAPH_IPA = {
    'kh': 'x',
    'gh': 'ɣ',
    'sh': 'ʃ',
    'zh': 'ʒ',
    'th': 'θ',
    'dh': 'ð',
    'rh': 'r̥',
}

VOWEL_IPA = {
    'ā': 'aː',
    'ē': 'eː',
    'ī': 'iː',
    'ō': 'oː',
    'ū': 'uː',
    'ã': 'ã',
    'õ': 'õ',
    'ĩ': 'ĩ',
    'a': 'a',
    'e': 'e',
    'i': 'i',
    'o': 'o',
    'u': 'u',
}

CONSONANT_IPA = {
    'p': 'p', 'b': 'b', 't': 't', 'd': 'd', 'k': 'k', 'g': 'g',
    'm': 'm', 'n': 'n', 'l': 'l', 'r': 'r', 's': 's', 'z': 'z',
    'f': 'f', 'v': 'v', 'h': 'h', 'j': 'j', 'y': 'j',
}


def to_ipa(word: str) -> str:
    """Return a rough IPA rendering for Kharvunic orthography.

    This is intentionally simple and editable. It does not yet model stress,
    register-specific pronunciation, or sandhi.
    """
    text = word.lower().strip()
    out = []
    i = 0
    while i < len(text):
        two = text[i:i + 2]
        one = text[i]
        if two in DIGRAPH_IPA:
            out.append(DIGRAPH_IPA[two])
            i += 2
        elif one in VOWEL_IPA:
            out.append(VOWEL_IPA[one])
            i += 1
        elif one in CONSONANT_IPA:
            out.append(CONSONANT_IPA[one])
            i += 1
        else:
            out.append(one)
            i += 1
    return '/' + ''.join(out) + '/'
