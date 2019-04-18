from aiotext.aiotext import Cleaner


def test_aiotext():
    """
    Test Cleaner. Run with pytest
    """

    text = "Call me Ishmael. Some years ago—never mind how long precisely—having "
    text += "little or no money in my purse, and nothing particular to interest me "
    text += "on shore, I thought I would sail about a little and see the watery part "
    text += "of the world. It is a way I have of driving off the spleen and "
    text += "regulating the circulation. Whenever I find myself growing grim about "
    text += "the mouth; whenever it is a damp, drizzly November in my soul; whenever "
    text += "I find myself involuntarily pausing before coffin warehouses, and "
    text += "bringing up the rear of every funeral I meet; and especially whenever "
    text += "my hypos get such an upper hand of me, that it requires a strong moral "
    text += "principle to prevent me from deliberately stepping into the street, and "
    text += "methodically knocking people’s hats off—then, I account it high time to "
    text += "get to sea as soon as I can. This is my substitute for pistol and ball. "
    text += "With a philosophical flourish Cato throws himself upon his sword; I "
    text += "quietly take to the ship. There is nothing surprising in this. If they "
    text += "but knew it, almost all men in their degree, some time or other, "
    text += "cherish very nearly the same feelings towards the ocean with me."

    # Initialize cleaner
    cleaner = Cleaner(expand_contractions=False)

    print(cleaner.clean(text))
    assert cleaner.clean(text) == [['call', 'me', 'ishmael'], ['some', 'year', 'ago', 'never', 'mind', 'how', 'long', 'precisely', 'have', 'little', 'or', 'no', 'money', 'in', 'my', 'purse', 'and', 'nothing', 'particular', 'to', 'interest', 'me', 'on', 'shore', 'i', 'think', 'i', 'would', 'sail', 'about', 'a', 'little', 'and', 'see', 'the', 'watery', 'part', 'of', 'the', 'world'], ['it', 'be', 'a', 'way', 'i', 'have', 'of', 'drive', 'off', 'the', 'spleen', 'and', 'regulate', 'the', 'circulation'], ['whenever', 'i', 'find', 'myself', 'grow', 'grim', 'about', 'the', 'mouth', 'whenever', 'it', 'be', 'a', 'damp', 'drizzly', 'november', 'in', 'my', 'soul', 'whenever', 'i', 'find', 'myself', 'involuntarily', 'pause', 'before', 'coffin', 'warehouse', 'and', 'bring', 'up', 'the', 'rear', 'of', 'every', 'funeral', 'i', 'meet', 'and', 'especially', 'whenever',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        'my', 'hypo', 'get', 'such', 'an', 'upper', 'hand', 'of', 'me', 'that', 'it', 'require', 'a', 'strong', 'moral', 'principle', 'to', 'prevent', 'me', 'from', 'deliberately', 'step', 'into', 'the', 'street', 'and', 'methodically', 'knock', 'people', 's', 'hat', 'off', 'then', 'i', 'account', 'it', 'high', 'time', 'to', 'get', 'to', 'sea', 'as', 'soon', 'as', 'i', 'can'], ['this', 'be', 'my', 'substitute', 'for', 'pistol', 'and', 'ball'], ['with', 'a', 'philosophical', 'flourish', 'cato', 'throw', 'himself', 'upon', 'his', 'sword', 'i', 'quietly', 'take', 'to', 'the', 'ship'], ['there', 'be', 'nothing', 'surprising', 'in', 'this'], ['if', 'they', 'but', 'know', 'it', 'almost', 'all', 'men', 'in', 'their', 'degree', 'some', 'time', 'or', 'other', 'cherish', 'very', 'nearly', 'the', 'same', 'feeling', 'towards', 'the', 'ocean', 'with', 'me']]

    text = "This is A sentence With wierd caps and no period"

    print(cleaner.clean(text))
    assert cleaner.clean(text) == [['this', 'be', 'a', 'sentence', 'with', 'wierd', 'cap', 'and', 'no', 'period']]

    # Initialize cleaner
    cleaner = Cleaner(expand_contractions=True, strip_text_in_brackets=True, combine_concatenations=True)

    text = "This is a dog's bone. That's a cat. Here are some random people's possesives. This sentence doesn't make much sense. That's okay. Just want to give ya'll an example"

    print(cleaner.clean(text))
    assert cleaner.clean(text) == [['this', 'be', 'a', 'dog', 's', 'bone'], ['that', 'be', 'a', 'cat'], ['here', 'be', 'some', 'random', 'people', 's', 'possesives'], ['this', 'sentence', 'do', 'not', 'make', 'much', 'sense'], ['that', 'be', 'okay'], ['just', 'want', 'to', 'give', 'ya', 'll', 'an', 'example']]

    text = "Now let's do it all (here's something). Oh look more-brackets {yep here's more}. You guessed it. This man's math is right-here [5 + 5 * (2 * 2)]. Doesn't this make everything easier."

    print(cleaner.clean(text))
    assert cleaner.clean(text) == [['now', 'let', 'us', 'do', 'it', 'all'], ['oh', 'look', 'morebrackets'], ['you', 'guess', 'it'], ['this', 'man', 's', 'math', 'be', 'righthere'], ['do', 'not', 'this', 'make', 'everything', 'easy']]


test_aiotext()
