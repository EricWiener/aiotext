import os
import argparse
import json
from pycontractions import Contractions  # expand contractions
from aiotext.lemmatize import lemmatize
import re  # regex
import string  # string helper Library
from nltk import sent_tokenize, word_tokenize
import regex


class Cleaner:
    def __init__(self,
                 expand_contractions=True,
                 strip_text_in_brackets=False,
                 combine_concatenations=False,
                 w2v_path=None,
                 api_key="word2vec-google-news-300",
                 ):

        self.opt_expand_contractions = expand_contractions
        self.opt_strip_text_in_brackets = strip_text_in_brackets
        self.opt_combine_concatenations = combine_concatenations

        if expand_contractions:
            print("Loading contractions dataset (this will take a while the first time)")

            # Load your favorite word2vec model
            self.cont = Contractions(w2v_path=w2v_path, api_key=api_key)
            print("Contractions dataset downloaded")

            print("Training contractions model (this will take a while)")
            # prevents loading on first expand_texts call
            self.cont.load_models()
            print("Contraction model successfully trained")

    def expand_contractions(self, text):
        text = text.replace("’", "'")  # need to put in the correct apostrophe
        expanded_text = list(self.cont.expand_texts([text], precise=True))
        return expanded_text[0]

    def strip_brackets(self, text):
        # Remove strings in brackets
        # Eg. "This is a sentence (extra info) description."
        # Becomes "This is a sentence description."
        """ Remove brackets from text
            Matches (), [], {}

            Converts:
            'hello (there) you (my[best] friend) lets {dine } }' -> 'hello  you  lets  }'
        """

        brace_open_type = ""
        brace_pair = {
            '(': ')',
            '[': ']',
            '{': '}'
        }
        open_brace_list = list(brace_pair.keys())

        res = ""
        for c in text:
            if len(brace_open_type) == 0:
                # not opened
                if c in open_brace_list:
                    brace_open_type = c
                else:
                    res += c
            else:
                # opened
                if brace_pair[brace_open_type] == c:
                    brace_open_type = ""

        return res

    def combine_concatenations(self, sentence):
        """
        Recieves string sentence
        "This is a sentence"
        """
        # convert concatenated words into seperate words
        # georgetown-louisville becomes georgetown louisville

        # Pd matches all types of dashes
        # https://www.compart.com/en/unicode/category/Pd

        if self.opt_combine_concatenations:
            def _refu(sent): return regex.sub(r'\p{Pd}+', '', sent)
        else:
            def _refu(sent): return regex.sub(r'\p{Pd}+', ' ', sent)

        return _refu(sentence)

    def remove_non_english(self, tokens):
        """
        Removes non-english words and all punctuation and numbers
        Removes extra white space

        Recieves list of tokens comprising a single sentence:
        ['this', 'is', 'a', 'sentence']
        """
        # remove all punctuation (removes non-english words too)
        # stripped = re.sub('[^a-zA-Z\s]*', '', stripped)

        # removes extra white spaces
        # stripped = re.sub('[ ]{2,}',' ', stripped)

        cleaned_tokens = []
        for token in tokens:
            cleaned = re.sub('[ ]{2,}', ' ', re.sub('[^a-zA-Z\s]*', '', token)).strip()
            if len(cleaned) != 0:
                cleaned_tokens.append(cleaned)

        return cleaned_tokens

    def lemmatize_sentences(self, tokenized_sentences):
        """
        Recieves
            Args: tokenized_sentences is of form
                [['this', 'is', 'sentence'],
                ['this', 'is', 'another']
                ['this', 'is', 'another']]

            Returns: lemmatized 2d list of same form
                [['this', 'is', 'sentenc'],
                ['this', 'is', 'anoth']
                ['this', 'is', 'anoth']]
        """
        lemmatized_sentences = []
        for sentence in tokenized_sentences:
            lemmatized_sentences.append(lemmatize(sentence))
        # lemmatized_sentences = [lemmatize(sentence) for sentence in tokenized_sentences]
        return lemmatized_sentences

    def clean(self, text):
        if self.opt_expand_contractions:
            # Expands it's -> it is
            text = self.expand_contractions(text)
    
        # text is lowercased after contractions are expanded
        # the contractions will be capitalized after they are expanded
        # eg. (i'm -> [I, am]). Therefore, the lowercasing is done afterwards
        text = text.lower()

        if self.opt_strip_text_in_brackets:
            text = self.strip_brackets(text)

        sentences = sent_tokenize(text)
        sentences = [self.combine_concatenations(sentence) for sentence in sentences]
        tokens_per_sentence = [word_tokenize(sent) for sent in sentences]
        lemmatized_tokens_per_sent = self.lemmatize_sentences(tokens_per_sentence)
        cleaned_tokens_per_sent = [self.remove_non_english(sent) for sent in lemmatized_tokens_per_sent]

        return cleaned_tokens_per_sent
