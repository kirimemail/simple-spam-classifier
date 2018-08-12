from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import SnowballStemmer
from Sastrawi.Stemmer import StemmerFactory
import numpy as np


class StemmedCountVectorizer(CountVectorizer):
    def get_stemmer(self, doc):
        from .language_detection import LanguageDetection
        lang_detect = LanguageDetection()
        lang = lang_detect.detect_language(doc)
        try:
            if lang == 'indonesian':
                factory = StemmerFactory()
                return factory.create_stemmer()
            else:
                return SnowballStemmer(lang)
        except Exception as err:
            return SnowballStemmer('english')

    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: ([self.get_stemmer(doc).stem(w) for w in analyzer(doc)])


class SelectStemmedCountVectorizer(CountVectorizer):
    def __init__(self, input='content', encoding='utf-8',
                 decode_error='strict', strip_accents=None,
                 lowercase=True, preprocessor=None, tokenizer=None,
                 stop_words=None, token_pattern=r"(?u)\b\w\w+\b",
                 ngram_range=(1, 1), analyzer='word',
                 max_df=1.0, min_df=1, max_features=None,
                 vocabulary=None, binary=False, dtype=np.int64, stemmer_language='english'):
        super(SelectStemmedCountVectorizer).__init__(input=input, encoding=encoding, decode_error=decode_error,
                                                     strip_accents=strip_accents, lowercase=lowercase,
                                                     preprocessor=preprocessor, tokenizer=tokenizer,
                                                     stop_words=stop_words, token_pattern=token_pattern,
                                                     ngram_range=ngram_range, analyzer=analyzer, max_df=max_df,
                                                     min_df=min_df, max_features=max_features, vocabulary=vocabulary,
                                                     binary=binary, dtype=dtype)
        self.stemmer_language = stemmer_language

    def get_stemmer(self):
        try:
            if self.stemmer_language == 'indonesian':
                factory = StemmerFactory()
                return factory.create_stemmer()
            else:
                return SnowballStemmer(self.stemmer_language)
        except Exception as err:
            return SnowballStemmer('english')

    def build_analyzer(self):
        analyzer = super(SelectStemmedCountVectorizer, self).build_analyzer()
        return lambda doc: ([self.get_stemmer().stem(w) for w in analyzer(doc)])
