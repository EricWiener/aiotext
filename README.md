# All-in-one Text Cleaner
This package was created to speed up the process of cleaning text for natural language processing and machine learning. The package does the following:
- Converts all text to lowercase
- Expands contractions using [pycontractions](https://pypi.org/project/pycontractions/) trained on the glove-twitter-100 word2vec training set (optional)
- Removes text in brackets. Matches "()","[]", or "{}" (optional)
- Combines concatenations (turns "georgetown-louisville" into "georgetown louisville" or "georgetownlousivelle"). Matches all types of hyphens.
- Splits sentences on punctuation using algorithm defined in [this stackoverflow post](https://stackoverflow.com/a/31505798/6942666).
- Tokenizes sentences.
- Lemmatizes tokens using NLTK WordNetLemmatizer and a lookup table between Penn Bank tags and Word Net.

## Installation
```
$ pip3 install aiotext
$ pip3 install git+https://github.com/EricWiener/pycontractions
```
Please note that pycontractions is specified as a dependency and will download from PyPi and work, but the branch I linked to above has multiple improvements.


## Usage:
### Options:
| Option                 | Default                    | Description                                                                                                                                                                                    |
|------------------------|----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| expand_contractions    | True                      | If true, contractions will be expanded (it's -> it is). This takes a long time. Especially the first time you run it.                                                                          |
| strip_text_in_brackets | False                      | If true removes text in brackets. If false the brackets will be removed, but text inside will remain.                                                                                          |
| combine_concatenations | False                      | If false replaces hyphen with space (george-louis -> george louis). If true just removes hyphen (george-louis -> georgelouis).                                                                 |
| w2v_path               | None                       | Path to word2vec binary.                                                                                                                                                                       |
| api_key                | "word2vec-google-news-300" | w2v_path will be given preference over api_key. If no valid binary is found at the path, the api will download the key specified. If no key is specified, the Google News vector will be used. |


```python
from aiotext import Cleaner

text = "Call me Ishmael. Some years ago—never mind how long precisely—having "
text += "little or no money in my purse, and nothing particular to interest me "
text += "on shore, I thought I would sail about a little and see the watery part "
text += "of the world. It is a way I have of driving off the spleen and "
text += "regulating the circulation."

# Initialize cleaner
cleaner = Cleaner(expand_contractions=True)

assert cleaner.clean(text) == [
['call', 'me', 'ishmael'],
['some', 'year', 'ago', 'never', 'mind', 'how', 'long', 'precisely', 'have', 'little', 'or', 'no', 'money', 'in', 'my', 'purse', 'and', 'nothing', 'particular',
    'to', 'interest', 'me', 'on', 'shore', 'i', 'think', 'i', 'would', 'sail', 'about', 'a', 'little', 'and', 'see', 'the', 'watery', 'part', 'of', 'the', 'world'],
['it', 'be', 'a', 'way', 'i', 'have', 'of', 'drive', 'off',
    'the', 'spleen', 'and', 'regulate', 'the', 'circulation'],
]
```

# Notes
- Please note you might have to manually quit and reattempt to run the program the first time you run it if it gets stuck after downloading the contractions dataset.
- Wordnet is used to lemmatize based on the parts of speech given by Penn Bank. Since Wordnet is limited in the number of options (eg. no pronouns), some words will not be processed. This is done to preserve the root word. For instance, "us" Wordnet will convert "us" to "u". In order to avoid this, "us" will not be passed into the lemmatizer.
- You may need to run the following if `wordnet` or `punkt` is not found
```python
python3
>> import nltk
>> nltk.download('wordnet')
>> nltk.download('punkt')
```

## Change log
- 1.0.0: Initial release
- 1.0.1: Corrected handling of sentences without punctuation and brackets
- 1.0.2: Added modified contraction expander download. Also made changes to solve [issue](https://github.com/nltk/nltk/issues/2269) with NLTK lemmatizer.
- 1.0.3: Added options for specifying word2vec model to use for contraction expansion
- 1.0.4: Minor syntax error
- 1.0.5: Changed passing of arguments, updated README, improved tokenization, and changed order of parsing to tag POS before cleaning text.
