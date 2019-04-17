import os
import argparse
import json
from pycontractions import Contractions  # expand contractions
from aiotext.lemmatize import lemmatize
import re  # regex
import string  # string helper Library
from aiotext.splitToSentences import split_into_sentences
import regex


class Cleaner:
    def __init__(self, options={'expand_contractions': True, 'strip_text_in_brackets': False, "combine_concatenations": False, }):
        self.options = options

        if options['expand_contractions']:
            print("Loading contractions dataset (this will take a while the first time)")

            # Load your favorite word2vec model
            self.cont = Contractions(api_key="glove-twitter-100")
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
        text = re.sub('(\()(.*)(\))|(\[)(.*)(\])|(\{)(.*)(\})', '', text)
        return text

    def combine_concatenations(self, text):
        # convert concatenated words into seperate words
        # georgetown-louisville becomes georgetown louisville
        if self.options['combine_concatenations']:
            # matches all types of dashes
            # https://www.compart.com/en/unicode/category/Pd
            text = regex.sub(r'\p{Pd}+', '', text)
        else:
            # matches all types of dashes
            # https://www.compart.com/en/unicode/category/Pd
            text = regex.sub(r'\p{Pd}+', ' ', text)

        return text

    def split_sentences(self, text):
        """
        Returns: list of sentences
        """
        # split into list of sentences
        return split_into_sentences(text)

    def remove_non_english(self, sentences):
        """
        Removes non-english words and all punctuation and numbers
        Removes extra white space
        """
        # remove all punctuation (removes non-english words too)
        # stripped = re.sub('[^a-zA-Z\s]*', '', stripped)

        # removes extra white spaces
        # stripped = re.sub('[ ]{2,}',' ', stripped)

        strippedSentences = [re.sub('[ ]{2,}', ' ', re.sub('[^a-zA-Z\s]*', '', sentence)) for sentence in sentences]
        return strippedSentences

    def tokenize_sentences(self, sentences):
        # tokenize:
        # this will be a 2 dimensional list
        # [['this', 'is', 'sentence'],
        # ['this', 'is', 'another']
        # ['this', 'is', 'another']]
        tokenized_sentences = []
        for sentence in sentences:
            tokenized_sentences.append(sentence.split())
        return tokenized_sentences

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
        text = text.lower()

        if self.options["expand_contractions"]:
            # Expands it's -> it is
            text = self.expand_contractions(text)

        if self.options["strip_text_in_brackets"]:
            text = self.strip_brackets(text)

        text = self.combine_concatenations(text)
        sentences = self.split_sentences(text)
        cleaned_sentences = self.remove_non_english(sentences)
        tokenized_cleaned_sentences = self.tokenize_sentences(cleaned_sentences)
        lemmatized_tokenized_sentences = self.lemmatize_sentences(tokenized_cleaned_sentences)

        return lemmatized_tokenized_sentences
