import re

from config import WORD_PATTERN, STOPWORDS
from word_stats import empty_stats, add_word


WORD_REGEX = re.compile(WORD_PATTERN)


# =========================
# Grundfunktionen
# =========================

def get_language(path):
    """
    Erkennt die Sprache aus dem Ordnernamen.

    Beispiel:
    texts/german/text1.txt -> german
    """
    return path.replace("\\", "/").split("/")[-2]

def get_valid_words(line):
    """
        Extrahiert gültige Wörter aus einer Textzeile.
        Stopwords werden entfernt.
        """
    for word in WORD_REGEX.findall(line):
        word = word.lower()

        if word not in STOPWORDS:
            yield word

def process(item):
    """
    Verarbeitet eine Textzeile.

    Diese Funktion wird auch für Tests benutzt.
    """
    line, path = item
    language = get_language(path)

    return [
        (language, word)
        for word in get_valid_words(line)
    ]


def analyze_file(file_path):
    """
    Analysiert eine einzelne Datei.

    Diese Funktion wird von der seriellen Version
    und von der Dask-Version benutzt.

    Bei Dask gilt:
    eine Datei = eine Partition.
    """
    language = get_language(file_path)
    stats = empty_stats()

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            for word in get_valid_words(line):
                add_word(stats, word)

    return language, stats