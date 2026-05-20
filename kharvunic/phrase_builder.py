from kharvunic.rhythm import scan_line
from kharvunic.ipa import to_ipa


def analyze_phrase(text: str, dictionary_words=None):
    dictionary_words = dictionary_words or set()

    words = [w.strip(',.!?;:').lower() for w in text.split() if w.strip()]

    ipa = ' '.join(to_ipa(word) for word in words)

    unknown = [
        word for word in words
        if dictionary_words and word not in dictionary_words
    ]

    rhythm = scan_line(text)

    return {
        'text': text,
        'ipa': ipa,
        'syllables': rhythm['syllables'],
        'stress': rhythm['stress'],
        'cadence': rhythm['cadence'],
        'unknown_words': unknown,
    }
