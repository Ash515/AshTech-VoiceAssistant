
"""Objects and functions used for parsing and manipulating mbrola phonemes"""
from typing import Tuple, List, Union, Iterable
from collections import MutableSequence


def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)


class Phoneme:

    def __init__(self, name : str, duration : int, pitch_mods : List[Tuple[int, int]] = None):
        self.name = name
        self.duration = duration
        self.pitch_modifiers = pitch_mods if pitch_mods is not None else []

    def __str__(self):
        return self.name + "\t" \
               + str(self.duration) + "\t" \
               + " ".join([str(percent) + " " + str(pitch) for percent, pitch in self.pitch_modifiers])

    @classmethod
    def from_str(cls, pho_str):
        """Instanciates a phoneme from a line of espeak's phoneme output."""
        split_pho = pho_str.split()
        name = split_pho.pop(0)
        duration = int(split_pho.pop(0))
        return cls(name, duration, [(int(percent), int(pitch)) for percent, pitch in pairwise(split_pho)])

    def set_from_pitches_list(self, pitch_list: List[int]):
        """Set pitches variations from a list of frequencies. The pitch variation are set to be
        equidistant from one another."""
        segment_length = 100 / (len(pitch_list) - 1)
        self.pitch_modifiers = [(i * segment_length, pitch) for i, pitch in enumerate(pitch_list)]


class PhonemeList(MutableSequence):
    """A list of phonemes. Can be printed into a .pho string formatted file"""

    def __init__(self, blocks: Union[Phoneme, Iterable[Phoneme]]):
        if isinstance(blocks, Phoneme):
            self._pho_list = [blocks]
        elif isinstance(blocks, Iterable):
            self._pho_list = list(blocks)
        else:
            raise ValueError("Expecting a list of blocks or a phonemes, got %s"
                             % str(type(blocks)))

    @classmethod
    def from_pho_str(cls, pho_str_list: str):
        return cls([Phoneme.from_str(pho_str) for pho_str in pho_str_list.split("\n") if pho_str.strip()])

    def __len__(self) -> int:
        return len(self._pho_list)

    def __delitem__(self, index: int):
        del self._pho_list[index]

    def insert(self, index, value: Phoneme):
        assert isinstance(value, Phoneme)
        self._pho_list.insert(index, value)

    def append(self, value: Phoneme):
        assert isinstance(value, Phoneme)
        self._pho_list.append(value)

    def __setitem__(self, index: int, value: Phoneme):
        assert isinstance(value, Phoneme)
        self._pho_list[index] = value

    def __getitem__(self, index: int) -> Phoneme:
        return self._pho_list[index]

    def __iter__(self) -> Iterable[Phoneme]:
        return iter(self._pho_list)

    def __add__(self, other: 'PhonemeList'):
        """Adds two `BlockList` to one another. Tries to merge
        the last block of the current list to the first of the other one."""
        assert self.__class__ == other.__class__
        return PhonemeList(list(self._pho_list) + list(other._pho_list))

    def __str__(self):
        return "\n".join([str(phoneme) for phoneme in self])

    @property
    def phonemes_str(self):
        return "".join([str(phoneme.name) for phoneme in self])


class AbstractPhonemeGroup:
    _all = set()

    def __contains__(self, item):
        return item in self._all

    def __iter__(self):
        return iter(self._all)

## all these sets are made from information taken here: http://www.phon.ucl.ac.uk/home/sampa/
## It's the SAMPA (based on IPA) standard for writing phonemes in lots of langages


class FrenchPhonemes:
    PLOSIVES = {"p", "b", "t", "d", "k", "g"}
    FRICATIVES = {'S', 'Z', 'f', 's', 'v', 'z', 'j'}
    NASAL_CONSONANTS = {'J', 'm', 'n', 'N'}
    LIQUIDS = {'H', 'R', 'j', 'l', 'w'}
    CONSONANTS = PLOSIVES | FRICATIVES | LIQUIDS | NASAL_CONSONANTS
    ORALS = {'2', '9', '@', 'A', 'E', 'O', 'a', 'e', 'i', 'o', 'u', 'y'}
    NASAL_WOVELS = {'9~', 'a~', 'e~', 'o~'}
    INDETERMINATE_WOVELS = {'&/', 'A/', 'E/', 'O/', 'U~/'}
    VOWELS = ORALS | NASAL_WOVELS | INDETERMINATE_WOVELS
    _all = VOWELS | CONSONANTS


class SpanishPhonemes:
    PLOSIVES = {"p", "b", "t", "d", "k", "g"}
    AFFRICATES = {'tS', 'jj'}
    FRICATIVES = {'f', 'B', 'T', 'D', 's', 'x', 'G'}
    NASAL = {'J', 'm', 'n'}
    LIQUIDS = {'rr', 'L', 'l', 'r'}
    CONSONANTS = PLOSIVES | AFFRICATES | FRICATIVES | LIQUIDS | NASAL
    VOWELS = {'a', 'e', 'i', 'o', 'u'}
    ACCENTS = {'"'}
    _all = VOWELS | CONSONANTS | ACCENTS


class BritishEnglishPhonemes(AbstractPhonemeGroup):
    PLOSIVES = {'b', 'd', 'g', 'k', 'p', 't'}
    AFFRICATES = {'dZ', 'tS'}
    FRICATIVES = {'D', 'S', 'T', 'Z', 'f', 'h', 's', 'v', 'z'}
    LIQUIDS = {'l', 'r'}
    NASALS = {'N', 'm', 'n'}
    GLIDES = {'j', 'w'}
    SONORANTS = LIQUIDS | NASALS | GLIDES
    CONSONANTS = PLOSIVES | FRICATIVES | SONORANTS | AFFRICATES
    CHECKED = {'I', 'Q', 'U', 'V', 'e', '{'}
    FREE = {'A:', 'I@', '@U', 'OI,', 'eI', 'e@', 'aI', '3:', 'U@', 'aU,', 'O:', 'i:', 'u:'}
    INDETERMINATE = {'i', 'u'}
    CENTRAL = {'@'}
    VOWELS = CHECKED | FREE | INDETERMINATE | CENTRAL
    ADDITIONALS = {"?", "x"}
    _all = VOWELS | CONSONANTS | ADDITIONALS


class GermanPhonemes(AbstractPhonemeGroup):
    PLOSIVES = {'b', 'd', 'g', 'k', 'p', 't'}
    GLOTTAL_STOP = "?"
    AFFRICATES = {'dZ', 'pf', 'tS', 'ts'}
    FRICATIVES = {'C', 'S', 'Z', 'f', 'h', 'j', 's', 'v', 'x', 'z'}
    SONORANTS = {'N', 'R', 'l', 'm', 'n'}
    CONSONANTS = PLOSIVES | AFFRICATES | FRICATIVES | SONORANTS
    CHECKED = {'9', 'E', 'I', 'O', 'U', 'Y', 'a'}
    PURE = {'2:', 'E:', 'a:', 'e:', 'i:', 'o:', 'u:', 'y:'}
    DIPHTONGS = {'OY', 'aI', 'aU'}
    VOWELS = CHECKED | PURE | DIPHTONGS
    SCHWA = {"@"}
    CENTRING_DIPHTONGS = {'2:6', '6', '96', 'E6', 'E:6', 'I6', 'O6', 'U6', 'Y6',
                          'a6', 'a:6', 'e:6', 'i:6', 'o:6', 'u:6', 'y:6'}
    _all = VOWELS | SCHWA | CENTRING_DIPHTONGS | CONSONANTS


class ItalianPhonemes:
    SINGLE_PLOSIVES = {'p', 'b', 't', 'd', 'k', 'g'}
    GEMINATE_PLOSIVES = {'pp', 'bb', 'tt', 'dd', 'kk', 'gg'}
    PLOSIVES = SINGLE_PLOSIVES | GEMINATE_PLOSIVES
    SINGLE_AFFRICATES = {'ts', 'dz', 'tS', 'dZ', 'tts', 'ddz', 'ttS', 'ddZ'}
    GEMINATE_AFFRICATES = {'ts', 'dz', 'tS', 'dZ', 'tts', 'ddz', 'ttS', 'ddZ'}
    AFFRICATES = SINGLE_AFFRICATES | GEMINATE_AFFRICATES
    SINGLE_FRICATIVES = {'f', 'v', 's', 'z', 'S'}
    GEMINATE_FRICATIVES = {'ff', 'vv', 'ss', 'SS'}
    FRICATIVES = SINGLE_FRICATIVES | GEMINATE_FRICATIVES
    SINGLE_NASAL = {'J', 'm', 'n'}
    GEMINATE_NASAL = {'JJ', 'mm', 'nn'}
    NASAL = SINGLE_NASAL | GEMINATE_NASAL
    SINGLE_LIQUIDS = {'L', 'l', 'r'}
    GEMINATE_LIQUIDS = {'LL', 'll', 'rr'}
    LIQUIDS = SINGLE_LIQUIDS | GEMINATE_LIQUIDS
    SEMIVOWELS = {'j', 'w'}
    CONSONANTS = PLOSIVES | AFFRICATES | FRICATIVES | LIQUIDS | NASAL
    VOWELS = {'i', 'e', 'E', 'a', 'O', 'o', 'u'}
    ACCENTS = {''}
    _all = VOWELS | CONSONANTS | ACCENTS




