# Handles lemmatization
# Recieves a list of tokens and returns a lemmatized list of tokens
# This is needed because lemmatizer doesn't automatically recognize
# parts of speech on it's own and often fails when something is not
# a verb. For instance, it would make "us" into "u" and "does" into "doe"

import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer


def lemmatize(tokens):
    # map between Penn Bank Tags and Word Net Tags
    tag_map = {
        'CC': None,  # coordin. conjunction (and, but, or)
        'CD': wn.NOUN,  # cardinal number (one, two)
        'DT': None,  # determiner (a, the)
        'EX': wn.ADV,  # existential ‘there’ (there)
        'FW': None,  # foreign word (mea culpa)
        'IN': wn.ADV,  # preposition/sub-conj (of, in, by)
        'JJ': wn.ADJ,  # adjective (yellow)
        'JJR': wn.ADJ,  # adj., comparative (bigger)
        'JJS': wn.ADJ,  # adj., superlative (wildest)
        'LS': None,  # list item marker (1, 2, One)
        'MD': None,  # modal (can, should)
        'NN': wn.NOUN,  # noun, sing. or mass (llama)
        'NNS': wn.NOUN,  # noun, plural (llamas)
        'NNP': wn.NOUN,  # proper noun, sing. (IBM)
        'NNPS': wn.NOUN,  # proper noun, plural (Carolinas)
        'PDT': wn.ADJ,  # predeterminer (all, both)
        'POS': None,  # possessive ending (’s )
        'PRP': None,  # personal pronoun (I, you, he)
        'PRP$': None,  # possessive pronoun (your, one’s)
        'RB': wn.ADV,  # adverb (quickly, never)
        'RBR': wn.ADV,  # adverb, comparative (faster)
        'RBS': wn.ADV,  # adverb, superlative (fastest)
        'RP': wn.ADJ,  # particle (up, off)
        'SYM': None,  # symbol (+,%, &)
        'TO': None,  # “to” (to)
        'UH': None,  # interjection (ah, oops)
        'VB': wn.VERB,  # verb base form (eat)
        'VBD': wn.VERB,  # verb past tense (ate)
        'VBG': wn.VERB,  # verb gerund (eating)
        'VBN': wn.VERB,  # verb past participle (eaten)
        'VBP': wn.VERB,  # verb non-3sg pres (eat)
        'VBZ': wn.VERB,  # verb 3sg pres (eats)
        'WDT': None,  # wh-determiner (which, that)
        'WP': None,  # wh-pronoun (what, who)
        'WP$': None,  # possessive (wh- whose)
        'WRB': None,  # wh-adverb (how, where)
        '$': None,  # dollar sign ($)
        '#': None,  # pound sign (#)
        '“': None,  # left quote (‘ or “)
        '”': None,  # right quote (’ or ”)
        '(': None,  # left parenthesis ([, (, {, <)
        ')': None,  # right parenthesis (], ), }, >)
        ',': None,  # comma (,)
        '.': None,  # sentence-final punc (. ! ?)
        ':': None  # mid-sentence punc (: ; ... – -)
    }

    lemmatizer = WordNetLemmatizer()

    # returns list of tuples (word, tag) - penn bank style
    tagTuples = nltk.pos_tag(tokens)

    # converts penn bank to word net
    wnTags = [(word, tag_map[tag]) for (word, tag) in tagTuples]

    # cycles through all tagged words
    # if there is no wn tag, it does nothing
    # if there is a tag, it lemmatizes
    output = []
    for (word, tag) in wnTags:
        if tag == None:
            output.append(word)
        else:
            output.append(lemmatizer.lemmatize(word, tag))

    return output
