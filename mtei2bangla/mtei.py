"""
This module will transliterate the text from Meetei Mayek to Bengali Script.
"""
import re
O = '\uABD1'
OO = 'ꯑꯣ'
U = '\uABCE'
EE = 'ꯑꯤ'
YA = 'ꯌ'
Y_ = 'য'
WA = 'ꯋ'
BA = 'ꯕ'
NA_ = "ꯟ"
NA = "ꯅ"
DIACRITIC_AA = "\uABE5"
PERIOD = "\uABEB"
HALANTA = "\uABED"
"""
All the diacritics are used to extend the sound of "a" to other vowels.
"""
DIACRITICS_WITH_O = {
    "\uABE3" : "ো",
    "\uABE4" : "ী",
    "\uABE5" : "া",
    "\uAbE6" : "ে",
    "\uABE7" : "ৌ",
    "\uABE9" : "ৈ",
    "\uABEA" : "ং",
}
CONJUGATE_WITH_O = {'ꯑꯣ': 'ও', 'ꯑꯤ': 'ঈ', 'ꯑꯥ': 'আ', 'ꯑꯦ': 'এ', 'ꯑꯧ':'ঔ' , 'ꯑꯩ': 'ঐ', 'ꯑꯪ': 'অং'}
NOT_WEIRD_AFTER_NA_ = {'ꯇ', 'ꯊ', 'ꯗ', 'ꯙ', NA, 'ꯕ', YA, 'ꯁ' }
VOWELS = {
    O: 'অ',
    'ꯏ': 'ই',
    'ꯎ': 'উ',
    'ꯢ' : 'ই',
    "\uABE8" : "ু",
} | DIACRITICS_WITH_O | CONJUGATE_WITH_O
NUMERALS = {
    "꯰": "০",
    "꯱": "১",
    "꯲": "২",
    "꯳": "৩",
    "꯴": "৪",
    "꯵": "৫",
    "꯶": "৬",
    "꯷": "৭",
    "꯸": "৮",
    "꯹": "৯"
}
HALANTA_CONSONANTS = {
    NA_ : "ন্",
    "ꯛ" : "ক্",
    "ꯝ" : "ম্",
    "ꯡ" : "ং",
    "ꯜ" : "ল্",
    "ꯠ" : "ৎ",
    "ꯞ" : "প্"
}
CONSONANTS = {
    "\uABC0": "ক",
    "\uABC8": "খ",
    "\uABD2": "গ",
    "\uABD8": "ঘ",
    "\uABC9": "ঙ",
    "\uABC6": "চ",
    "\uABD6": "জ",
    "\uABD3": "ঝ",
    # "ꫣ": "ঞ",
    # "ꫤ": "ট",
    # "ꫥ": "ঠ",
    # "ꫦ": "ড",
    # "ꫧ": "ঢ",
    # "ꫨ": "ণ",
    "ꯇ": "ত",
    "ꯊ": "থ",
    "ꯗ": "দ",
    "ꯙ": "ধ",
    NA: "ন",
    "ꯄ": "প",
    "ꯐ": "ফ",
    "ꯕ": "ব",
    "ꯚ": "ভ",
    "ꯃ": "ম",
    YA: "য়",
    "ꯔ": "র",
    "ꯂ": "ল",
    "ꯋ": "ৱ",
    "ꫩ": "শ",
    "ꫪ": "ষ",
    "ꯁ": "স",
    "ꯍ": "হ",
} | HALANTA_CONSONANTS
MTEI_TO_BENG_MAP = {
    PERIOD : "।",
    HALANTA : "্",
} | VOWELS | NUMERALS | CONSONANTS

JUNK_CHARACTERS = re.compile(f'[\s,\n{PERIOD}]')
def _is_beginning(position, text):
    return position == 0 or JUNK_CHARACTERS.match(text[position - 1])
def is_end_of_word(char):
    return JUNK_CHARACTERS.match(char) or char in {PERIOD}

class MeiteiToBengali:
    _preprocess = staticmethod(lambda x: x)
    _postprocess = staticmethod(lambda x: x)
    def __init__(self, text):
        self.text = text
    @staticmethod
    def set_preprocess(func):
        MeiteiToBengali._preprocess = func
    @staticmethod
    def set_postprocess(func):
        MeiteiToBengali._postprocess = func
    @staticmethod
    def _mtei_to_bengali(text):
        """
        Convert the given Meetei Mayek text to Bengali Script.
        """
        l = len(text)
        i = 0
        while i < l:
            char = text[i]
            if char == O and i + 1 < l and text[i + 1] in DIACRITICS_WITH_O:
                """
                We have only 3 true vowels, 
                ꯑ(a), ꯏ(i), ꯎ (u) 
                Others are just extension from "a" by mixing with diacritics
                """
                yield CONJUGATE_WITH_O.get(char + text[i + 1], char + text[i + 1])
                i += 1
            elif char == YA and i > 0 and text[i - 1] == HALANTA:
                """
                য + ্ = য়
                """
                yield Y_
            elif char == WA and i - 2 >= 0 and text[i - 1] == HALANTA and text[i - 2] in CONSONANTS:
                """
                ব + ্ + র = ব্র
                """
                yield CONSONANTS[BA]
            elif char == NA_ and i + 1 < l and text[i + 1] not in NOT_WEIRD_AFTER_NA_ and text[i + 1] in CONSONANTS:
                """
                ন্ / ণ্ + any consonant (except, ট, ঠ, ড, ঢ, , ত, থ, দ, ধ, ন, ব, য, য়) = wierd
                Any consonant + ্ + ন =  maybe ok
                """
                yield MTEI_TO_BENG_MAP[NA]
                i += 1
                continue
            elif char == U and not _is_beginning(i, text):
                """
                উ/ঊ in the middle of words are often replaced by ও
                """
                # Replace with O
                yield MTEI_TO_BENG_MAP[OO]
            elif char == O and i + 1 < l and text[i:i + 2] == EE:
                """
                Instead of হাঈবা, people love to use হায়বা.
                But this is only in the case when ee or ya is in the middle of the words,
                never to do it if it's in the beginning.
                """
                # Replace with Ya
                yield MTEI_TO_BENG_MAP[YA]
            elif char not in HALANTA_CONSONANTS and char in CONSONANTS and (i == l - 1 or (i + 1 < l and is_end_of_word(text[i + 1]))):
                """
                Consonants without halantas should end with diacritics of aa sound everytime.
                """
                yield MTEI_TO_BENG_MAP[char] + MTEI_TO_BENG_MAP[DIACRITIC_AA]
            else:
                yield MTEI_TO_BENG_MAP.get(char, char)
            i += 1
    @staticmethod
    def transliterate(text):
        text = MeiteiToBengali._preprocess(text)
        transliterated = ''.join(MeiteiToBengali._mtei_to_bengali(text))
        return MeiteiToBengali._postprocess(transliterated)
if __name__ == "__main__":
    text =  input("Enter the Meetei Mayek Text: ")
    print(MeiteiToBengali.transliterate(text))
