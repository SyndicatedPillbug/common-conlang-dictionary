RULES = {
    'common': [
        ('ct', 'kt'),
        ('ae', 'e'),
        ('oe', 'e'),
        ('ph', 'f'),
        ('qu', 'k'),
        ('ti', 'sh'),
        ('c(?=[eiy])', 'ch'),
        ('ce', 'she'),
        ('ci', 'shi'),
        ('vocalic_ria$', 'ra'),
        ('ia$', 'a'),
        ('us$', ''),
        ('um$', ''),
        ('is$', ''),
        ('ere$', 'er'),
    ],
    'temple': [
        ('esh', 'ezh'),
        ('elest', 'elestār'),
        ('cord', 'zher'),
    ],
    'boardroom': [
        ('ct', 'kt'),
        ('kt', 'kr'),
        ('alis$', 'd'),
    ],
    'trade': [
        ('zh', 'j'),
        ('er$', ''),
        ('a$', ''),
    ]
}
