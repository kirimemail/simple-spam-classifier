import sys

try:
    from nltk import wordpunct_tokenize
    from nltk.corpus import stopwords
except ImportError:
    print('[!] You need to install nltk (http://nltk.org/index.html)')


class LanguageDetection(object):
    def __init__(self):
        try:
            """
            Make sure stopwords is exist, if not download it first
            """
            stopwords.fileids()
        except NameError:
            import nltk
            nltk.download('stopwords')
            nltk.download('punkt')

    def __calculate_languages_ratios(self, text):
        """
        Calculate probability of given text to be written in several languages and
        return a dictionary that looks like {'french': 2, 'spanish': 4, 'english': 0}

        @param text: Text whose language want to be detected
        @type text: str

        @return: Dictionary with languages and unique stopwords seen in analyzed text
        @rtype: dict
        """

        languages_ratios = {}

        '''
        nltk.wordpunct_tokenize() splits all punctuations into separate tokens
    
        >>> wordpunct_tokenize("That's thirty minutes away. I'll be there in ten.")
        ['That', "'", 's', 'thirty', 'minutes', 'away', '.', 'I', "'", 'll', 'be', 'there', 'in', 'ten', '.']
        '''

        tokens = wordpunct_tokenize(text)
        words = [word.lower() for word in tokens]

        # Compute per language included in nltk number of unique stopwords appearing in analyzed text
        for language in stopwords.fileids():
            stopwords_set = set(stopwords.words(language))
            words_set = set(words)
            common_elements = words_set.intersection(stopwords_set)

            languages_ratios[language] = len(common_elements)  # language "score"

        return languages_ratios

    # ----------------------------------------------------------------------
    def detect_language(self, text):
        """
        Calculate probability of given text to be written in several languages and
        return the highest scored.

        It uses a stopwords based approach, counting how many unique stopwords
        are seen in analyzed text.

        @param text: Text whose language want to be detected
        @type text: str

        @return: Most scored language guessed
        @rtype: str
        """

        ratios = self.__calculate_languages_ratios(text)

        most_rated_language = max(ratios, key=ratios.get)

        return most_rated_language


if __name__ == '__main__':
    text = '''
    Dapatkan lebih banyak pelanggan potensial yang siap membeli produk Anda kapan saja. 
    Buat akun Anda sekarang untuk mulai berkomunikasi secara personal dengan pelanggan Anda
    '''
    language_detection = LanguageDetection()
    language = language_detection.detect_language(text)

    print(language)
