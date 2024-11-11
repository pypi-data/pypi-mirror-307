import spacy_helper as sh

l = [
    {
        'start': 2,
        'end': 2
    },
    {
        'start': -1,
        'end': 1
    },
    {
        'start': -1,
        'end': 0
    },
    {
        'start': 1,
        'end': 3
    }
]

l = [
    {
        'start': 0,
        'end': 0
    },

    {
        'start': 1,
        'end': 3
    }
]
print('Before', l)
l.sort(key=lambda x: (x['start'], x['end']))
print('After', l)
sh.check_overlap(l)