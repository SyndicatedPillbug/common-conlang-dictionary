from difflib import SequenceMatcher

MIN_SIMILARITY = 0.82


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def find_collisions(entries, word: str):
    matches = []

    for entry in entries:
        existing = str(entry.get('word', ''))
        score = similarity(existing, word)

        if score >= MIN_SIMILARITY:
            matches.append({
                'existing_word': existing,
                'meaning': entry.get('meaning', ''),
                'register': entry.get('register', ''),
                'similarity': round(score, 3),
            })

    return sorted(matches, key=lambda x: x['similarity'], reverse=True)
