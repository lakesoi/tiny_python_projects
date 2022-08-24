#!/usr/bin/env python
"""tests for crowsnest.py"""

import os
from subprocess import getstatusoutput, getoutput

prg = 'crowsnest.py'
# consonant_words = [
    # 'brigantine', 'clipper', 'dreadnought', 'frigate', 'galleon', 'haddock',
    # 'junk', 'ketch', 'longboat', 'mullet', 'narwhal', 'porpoise', 'quay',
    # 'regatta', 'submarine', 'tanker', 'vessel', 'whale', 'xebec', 'yatch',
    # 'zebrafish'
# ]
consonant_words = [
    'brigantine'
]
# vowel_words = ['aviso', 'eel', 'iceberg', 'octopus', 'upbound']
vowel_words = ['aviso']
not_word = ['!@$FD#@', '123455']
template = 'Ahoy, Captain, {} {} off the larboard bow!'
template_starboard = 'Ahoy, Captain, {} {} off the starboard bow!'


# --------------------------------------------------
def test_exists():
    """exists"""

    assert os.path.isfile(prg)


# --------------------------------------------------
def test_usage():
    """usage"""

    for flag in ['-h', '--help']:
        rv, out = getstatusoutput(f'{prg} {flag}')
        assert rv == 0
        assert out.lower().startswith('usage')


# --------------------------------------------------
def test_consonant():
    """brigantine -> a brigantine"""

    for word in consonant_words:
        out = getoutput(f'{prg} {word}')
        assert out.strip() == template.format('a', word)


# --------------------------------------------------
def test_consonant_upper():
    """brigantine -> a Brigatine"""

    for word in consonant_words:
        out = getoutput(f'{prg} {word.title()}')
        assert out.strip() == template.format('a', word.title())


# --------------------------------------------------
def test_vowel():
    """octopus -> an octopus"""

    for word in vowel_words:
        out = getoutput(f'{prg} {word}')
        assert out.strip() == template.format('an', word)


# --------------------------------------------------
def test_vowel_upper():
    """octopus -> an Octopus"""

    for word in vowel_words:
        out = getoutput(f'{prg} {word.upper()}')
        assert out.strip() == template.format('an', word.upper())


# --------------------------------------------------
def test_align_first_character():
    """align capital"""

    for option in ['-c', '--capital']:
        for word in vowel_words:
            out = getoutput(f'{prg} {word} {option} on')
            assert out.strip() == template.format('an', word)
            out = getoutput(f'{prg} {word.title()} {option} on')
            assert out.strip() == template.format('An', word.title())
            out = getoutput(f'{prg} {word} {option} off')
            assert out.strip() == template.format('an', word)
            out = getoutput(f'{prg} {word.title()} {option} off')
            assert out.strip() == template.format('an', word.title())


# --------------------------------------------------
def test_board_direction():
    """side option"""

    for option in ['--side', '-s']:
        for word in vowel_words:
            out = getoutput(f'{prg} {word} {option} left')
            assert out.strip() == template.format('an', word)

    for option in ['--side', '-s']:
        for word in vowel_words:
            out = getoutput(f'{prg} {word} {option} right')
            assert out.strip() == template_starboard.format('an', word)

# --------------------------------------------------
def test_not_word_filter():
    """filtering not words"""
    for word in not_word:
        out = getoutput(f'{prg} {word}')
        assert out.strip() == 'Invalid word'