"""
Semantic Text Similarity Module
================================
Upgrades the basic TF-IDF cosine similarity with:

  1. Token Normalization   -- lowercase, strip punctuation, collapse whitespace
  2. Compound-Word Joining -- "mobile phone" -> "mobilephone" before tokenising
  3. Synonym Expansion     -- maps synonyms to a canonical form
                             e.g. flask/bottle -> __vessel__
                                  smartphone/mobilephone -> __smartphone__
                                  iphone15/Iphone15 -> __iphone__
  4. Porter Stemmer        -- pure-Python suffix stripping (no NLTK required)
  5. TF-IDF Cosine Sim     -- smooth IDF over the 2-doc corpus, cosine distance

Zero external dependencies beyond the Python stdlib.
"""

import re
import math
from collections import Counter

# ---------------------------------------------------------------------------
# 1.  Stop-words
# ---------------------------------------------------------------------------
STOP_WORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an',
    'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'before',
    'being', 'below', 'between', 'both', 'but', 'by', 'can', 'did', 'do',
    'does', 'doing', 'down', 'during', 'each', 'few', 'for', 'from',
    'further', 'had', 'has', 'have', 'having', 'he', 'her', 'here', 'hers',
    'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in', 'into',
    'is', 'it', 'its', 'itself', 'just', 'me', 'more', 'most', 'my',
    'myself', 'no', 'nor', 'not', 'now', 'of', 'off', 'on', 'once', 'only',
    'or', 'other', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 's',
    'same', 'she', 'should', 'so', 'some', 'such', 't', 'than', 'that',
    'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there',
    'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under',
    'until', 'up', 'very', 'was', 'we', 'were', 'what', 'when', 'where',
    'which', 'while', 'who', 'whom', 'why', 'with', 'you', 'your', 'yours',
    'yourself', 'yourselves',
    # domain noise
    'lost', 'found', 'item', 'please', 'left', 'near', 'room',
}


# ---------------------------------------------------------------------------
# 2.  Synonym dictionary
#     Keys   = surface forms (already lowercased, punctuation removed)
#     Values = canonical __tokens__ (double-underscore avoids stop-word collision)
#
#     Add new synonym groups freely.
# ---------------------------------------------------------------------------
SYNONYM_MAP = {
    # -- Containers / drinkware --------------------------------------------
    "bottle":           "__vessel__",
    "flask":            "__vessel__",
    "thermos":          "__vessel__",
    "tumbler":          "__vessel__",
    "waterbottle":      "__vessel__",
    "sipper":           "__vessel__",
    "canteen":          "__vessel__",
    "jug":              "__vessel__",

    # -- Smartphones --------------------------------------------------------
    "smartphone":       "__smartphone__",
    "mobilephone":      "__smartphone__",
    "mobile":           "__smartphone__",
    "cellphone":        "__smartphone__",
    "phone":            "__smartphone__",
    "handset":          "__smartphone__",
    "android":          "__smartphone__",

    # -- Apple product line --------------------------------------------------
    "iphone":           "__iphone__",
    "iphone15":         "__iphone__",
    "iphone14":         "__iphone__",
    "iphone13":         "__iphone__",
    "iphone12":         "__iphone__",
    "iphone11":         "__iphone__",
    "iphonex":          "__iphone__",
    "ipad":             "__ipad__",
    "macbook":          "__macbook__",
    "airpods":          "__airpods__",
    "airpod":           "__airpods__",

    # -- Laptops / computers ------------------------------------------------
    "laptop":           "__laptop__",
    "notebook":         "__laptop__",
    "netbook":          "__laptop__",
    "chromebook":       "__laptop__",
    "computer":         "__computer__",
    "desktop":          "__computer__",
    "pc":               "__computer__",

    # -- Headphones / audio -------------------------------------------------
    "headphone":        "__headphones__",
    "headphones":       "__headphones__",
    "earphone":         "__headphones__",
    "earphones":        "__headphones__",
    "earbuds":          "__headphones__",
    "earbud":           "__headphones__",
    "headset":          "__headphones__",

    # -- Bags / backpacks ---------------------------------------------------
    "bag":              "__bag__",
    "backpack":         "__bag__",
    "rucksack":         "__bag__",
    "satchel":          "__bag__",
    "handbag":          "__bag__",
    "tote":             "__bag__",

    # -- Writing instruments ------------------------------------------------
    "pen":              "__pen__",
    "pencil":           "__pen__",
    "marker":           "__pen__",
    "highlighter":      "__pen__",
    "ballpen":          "__pen__",
    "ballpoint":        "__pen__",

    # -- Books / notebooks --------------------------------------------------
    # NOTE: "notebook" intentionally NOT listed here — it maps to __laptop__ above.
    "book":             "__book__",
    "textbook":         "__book__",
    "notes":            "__book__",
    "journal":          "__book__",
    "diary":            "__book__",


    # -- Wallets / cards ----------------------------------------------------
    "wallet":           "__wallet__",
    "purse":            "__wallet__",
    "cardholder":       "__wallet__",
    "cardcase":         "__wallet__",

    # -- Keys ---------------------------------------------------------------
    "key":              "__key__",
    "keys":             "__key__",
    "keychain":         "__key__",
    "keyring":          "__key__",

    # -- Glasses / eyewear --------------------------------------------------
    "glasses":          "__glasses__",
    "spectacles":       "__glasses__",
    "specs":            "__glasses__",
    "eyeglasses":       "__glasses__",
    "sunglasses":       "__glasses__",
    "goggles":          "__glasses__",

    # -- Chargers / cables --------------------------------------------------
    "charger":          "__charger__",
    "cable":            "__charger__",
    "adapter":          "__charger__",
    "powerbank":        "__powerbank__",

    # -- Umbrella -----------------------------------------------------------
    "umbrella":         "__umbrella__",
    "brolly":           "__umbrella__",
    "parasol":          "__umbrella__",

    # -- ID / cards ---------------------------------------------------------
    "idcard":           "__idcard__",
    "studentid":        "__idcard__",
    "identitycard":     "__idcard__",
    "aadhar":           "__idcard__",
    "aadharcard":       "__idcard__",

    # -- Watches ------------------------------------------------------------
    "watch":            "__watch__",
    "smartwatch":       "__watch__",
    "wristwatch":       "__watch__",

    # -- Clothing -----------------------------------------------------------
    "jacket":           "__jacket__",
    "hoodie":           "__jacket__",
    "sweatshirt":       "__jacket__",
    "coat":             "__jacket__",

    # -- Colour spellings ---------------------------------------------------
    "grey":             "gray",
    "colour":           "color",

    # -- Campus locations ---------------------------------------------------
    "cafeteria":        "__canteen__",
    "mess":             "__canteen__",
    "library":          "__library__",
    "lib":              "__library__",
    "hostel":           "__hostel__",
    "dorm":             "__hostel__",
    "dormitory":        "__hostel__",
    "classroom":        "__classroom__",
    "lab":              "__lab__",
    "laboratory":       "__lab__",
}


# ---------------------------------------------------------------------------
# 3.  Compound-word patterns to join BEFORE tokenising
#     Processed on the lowercased text; applied in order.
# ---------------------------------------------------------------------------
COMPOUND_PATTERNS = [
    (r'\bmobile\s+phone\b',     'mobilephone'),
    (r'\bcell\s+phone\b',       'cellphone'),
    (r'\bsmart\s+phone\b',      'smartphone'),
    (r'\biphone\s*(\d+)\b',     r'iphone\1'),   # "iphone 15" -> "iphone15"
    (r'\bipod\s+touch\b',       'ipodtouch'),
    (r'\bback\s+pack\b',        'backpack'),
    (r'\bwater\s+bottle\b',     'waterbottle'),
    (r'\bpower\s+bank\b',       'powerbank'),
    (r'\bid\s+card\b',          'idcard'),
    (r'\bstudent\s+id\b',       'studentid'),
    (r'\baadhar\s+card\b',      'aadharcard'),
    (r'\bear\s+buds?\b',        'earbuds'),
    (r'\bear\s+phones?\b',      'earphones'),
    (r'\bsmart\s+watch\b',      'smartwatch'),
    (r'\bwrist\s+watch\b',      'wristwatch'),
    (r'\bball\s*point\b',       'ballpoint'),
    (r'\bball\s+pen\b',         'ballpen'),
    (r'\btext\s+book\b',        'textbook'),
    (r'\bhand\s+bag\b',         'handbag'),
    (r'\bcard\s+holder\b',      'cardholder'),
    (r'\bkey\s+chain\b',        'keychain'),
    (r'\bkey\s+ring\b',         'keyring'),
    (r'\bsun\s+glasses?\b',     'sunglasses'),
    (r'\beye\s+glasses?\b',     'eyeglasses'),
]


# ---------------------------------------------------------------------------
# 4.  Minimal Porter Stemmer (pure Python, no dependencies)
# ---------------------------------------------------------------------------

def _has_vowel(word):
    return bool(re.search(r'[aeiou]', word))


def _ends_double_consonant(word):
    return (len(word) >= 2 and
            word[-1] == word[-2] and
            word[-1] not in 'aeiou')


def _cvc(word):
    """True if word ends consonant-vowel-consonant and last consonant not in w,x,y."""
    if len(word) < 3:
        return False
    c, v, c2 = word[-3], word[-2], word[-1]
    return (c not in 'aeiou') and (v in 'aeiou') and (c2 not in 'aeiou') and (c2 not in 'wxy')


def _measure(stem):
    """Count VC sequences (m) in stem."""
    seq = re.sub(r'^[^aeiou]+', '', stem)
    seq = re.sub(r'[aeiou]+', 'v', seq)
    seq = re.sub(r'[^v]+', 'c', seq)
    return seq.count('vc')


def _porter_stem(word):
    """Return the stemmed form of a lowercase English word."""
    if len(word) <= 2:
        return word

    # Step 1a
    if word.endswith('sses'):
        word = word[:-2]
    elif word.endswith('ies'):
        word = word[:-2]
    elif word.endswith('ss'):
        pass
    elif word.endswith('s'):
        word = word[:-1]

    # Step 1b helper
    def step1b_cleanup(w):
        if w.endswith('at') or w.endswith('bl') or w.endswith('iz'):
            return w + 'e'
        if _ends_double_consonant(w) and w[-1] not in 'lsz':
            return w[:-1]
        if _measure(w) == 1 and _cvc(w):
            return w + 'e'
        return w

    if word.endswith('eed'):
        stem = word[:-3]
        if _measure(stem) > 0:
            word = stem + 'ee'
    elif word.endswith('ed'):
        stem = word[:-2]
        if _has_vowel(stem):
            word = step1b_cleanup(stem)
    elif word.endswith('ing'):
        stem = word[:-3]
        if _has_vowel(stem):
            word = step1b_cleanup(stem)

    # Step 1c
    if word.endswith('y') and _has_vowel(word[:-1]):
        word = word[:-1] + 'i'

    # Step 2
    step2_map = [
        ('ational', 'ate'), ('tional', 'tion'), ('enci', 'ence'),
        ('anci', 'ance'), ('izer', 'ize'), ('iser', 'ise'),
        ('abli', 'able'), ('alli', 'al'), ('entli', 'ent'),
        ('eli', 'e'), ('ousli', 'ous'), ('ization', 'ize'),
        ('isation', 'ise'), ('ation', 'ate'), ('ator', 'ate'),
        ('alism', 'al'), ('iveness', 'ive'), ('fulness', 'ful'),
        ('ousness', 'ous'), ('aliti', 'al'), ('iviti', 'ive'),
        ('biliti', 'ble'),
    ]
    for suffix, replacement in step2_map:
        if word.endswith(suffix):
            stem = word[:-len(suffix)]
            if _measure(stem) > 0:
                word = stem + replacement
            break

    # Step 3
    step3_map = [
        ('icate', 'ic'), ('ative', ''), ('alize', 'al'),
        ('iciti', 'ic'), ('ical', 'ic'), ('ful', ''), ('ness', ''),
    ]
    for suffix, replacement in step3_map:
        if word.endswith(suffix):
            stem = word[:-len(suffix)]
            if _measure(stem) > 0:
                word = stem + replacement
            break

    # Step 4
    step4_suffixes = [
        'ement', 'ment', 'ance', 'ence', 'er', 'ic', 'able', 'ible',
        'ant', 'ent', 'ion', 'ou', 'ism', 'ate', 'iti', 'ous', 'ive', 'ize',
    ]
    for suffix in step4_suffixes:
        if word.endswith(suffix):
            stem = word[:-len(suffix)]
            m = _measure(stem)
            if suffix == 'ion':
                if m > 1 and stem and stem[-1] in 'st':
                    word = stem
            elif m > 1:
                word = stem
            break

    # Step 5a
    if word.endswith('e'):
        stem = word[:-1]
        if _measure(stem) > 1:
            word = stem
        elif _measure(stem) == 1 and not _cvc(stem):
            word = stem

    # Step 5b
    if _measure(word) > 1 and _ends_double_consonant(word) and word.endswith('l'):
        word = word[:-1]

    return word


# ---------------------------------------------------------------------------
# 5.  Tokeniser pipeline
# ---------------------------------------------------------------------------

def _normalise_text(text):
    """Lowercase, join compound words, strip punctuation, collapse spaces."""
    text = text.lower()
    for pattern, repl in COMPOUND_PATTERNS:
        text = re.sub(pattern, repl, text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _tokenise(text):
    """
    Full pipeline:
      raw text -> normalise -> split -> synonym expand -> stem -> drop stop-words
    """
    normed = _normalise_text(text)
    raw_tokens = normed.split()

    tokens = []
    for tok in raw_tokens:
        canonical = SYNONYM_MAP.get(tok, tok)

        # Canonical __markers__ are kept verbatim (skip stemming & stop-word filter)
        if canonical.startswith('__'):
            tokens.append(canonical)
            continue

        if canonical in STOP_WORDS:
            continue

        stemmed = _porter_stem(canonical)
        if stemmed:
            tokens.append(stemmed)

    return tokens


# ---------------------------------------------------------------------------
# 6.  TF-IDF Cosine Similarity  (public API)
# ---------------------------------------------------------------------------

def compute_text_similarity(str1, str2):
    """
    Compute semantic TF-IDF cosine similarity between two strings.

    Pipeline applied to each string:
      compound joining -> synonym expansion -> Porter stemming -> stop-word removal

    Similarity computed via:
      smooth TF-IDF vectors -> cosine distance

    Returns:
        float: similarity score in [0.0, 1.0]

    Examples that now work correctly:
        "bottle" vs "flask"             -> high score  (both -> __vessel__)
        "smartphone" vs "mobile phone"  -> high score  (both -> __smartphone__)
        "iPhone15" vs "Iphone15"        -> high score  (both -> __iphone__)
        "headphones" vs "earbuds"       -> high score  (both -> __headphones__)
    """
    if not str1 or not str2:
        return 0.0

    tokens1 = _tokenise(str1)
    tokens2 = _tokenise(str2)

    # Fallback: if pipeline wiped all tokens, use raw normalised split
    if not tokens1 or not tokens2:
        tokens1 = _normalise_text(str1).split() or ['']
        tokens2 = _normalise_text(str2).split() or ['']
        if not tokens1 or not tokens2:
            return 0.0

    tf1 = Counter(tokens1)
    tf2 = Counter(tokens2)
    len1 = len(tokens1)
    len2 = len(tokens2)

    vocab = set(tf1.keys()) | set(tf2.keys())
    N = 2  # corpus of 2 documents

    vec1, vec2 = {}, {}
    for word in vocab:
        df = (1 if word in tf1 else 0) + (1 if word in tf2 else 0)
        idf = math.log((1 + N) / (1 + df)) + 1.0
        vec1[word] = (tf1.get(word, 0) / len1) * idf
        vec2[word] = (tf2.get(word, 0) / len2) * idf

    dot  = sum(vec1[w] * vec2[w] for w in vocab)
    mag1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
    mag2 = math.sqrt(sum(v ** 2 for v in vec2.values()))

    if mag1 == 0 or mag2 == 0:
        return 0.0

    return float(dot / (mag1 * mag2))
