from collections import Counter


# =========================
# Statistik-Funktionen
# =========================

def empty_stats():
    """
    Erstellt eine leere Statistik.
    """
    return {
        "word_count": 0,
        "total_length": 0,
        "longest_word": "",
        "longest_length": 0,
        "distribution": Counter()
    }


def add_word_with_length(stats, word, length):
    """
    Fügt ein Wort zur Statistik hinzu.
    """
    stats["word_count"] += 1
    stats["total_length"] += length
    stats["distribution"][length] += 1

    if (
        length > stats["longest_length"]
        or (
            length == stats["longest_length"]
            and (stats["longest_word"] == "" or word < stats["longest_word"])
        )
    ):
        stats["longest_word"] = word
        stats["longest_length"] = length


def add_word(stats, word):
    """
    Fügt ein Wort zur Statistik hinzu.
    """
    add_word_with_length(stats, word, len(word))


def merge_stats(a, b):
    """
    Führt zwei Statistiken zusammen.

    Das ist wichtig für Dask.
    Dask berechnet zuerst Teilstatistiken.
    Danach werden diese Teilstatistiken zusammengeführt.
    """
    result = empty_stats()

    result["word_count"] = a["word_count"] + b["word_count"]
    result["total_length"] = a["total_length"] + b["total_length"]
    result["distribution"] = a["distribution"] + b["distribution"]

    if (
        a["longest_length"] > b["longest_length"]
        or (
            a["longest_length"] == b["longest_length"]
            and (
                b["longest_word"] == ""
                or (
                    a["longest_word"] != ""
                    and a["longest_word"] < b["longest_word"]
                )
            )
        )
    ):
        result["longest_word"] = a["longest_word"]
        result["longest_length"] = a["longest_length"]
    else:
        result["longest_word"] = b["longest_word"]
        result["longest_length"] = b["longest_length"]

    return result


def median_from_distribution(distribution, word_count):
    """
    Berechnet den Median aus der Wortlängen-Verteilung.
    """
    if word_count == 0:
        return 0

    middle_1 = (word_count + 1) // 2
    middle_2 = (word_count + 2) // 2

    value_1 = None
    value_2 = None

    count_sum = 0

    for length in sorted(distribution.keys()):
        count_sum += distribution[length]

        if value_1 is None and count_sum >= middle_1:
            value_1 = length

        if value_2 is None and count_sum >= middle_2:
            value_2 = length
            break

    median = (value_1 + value_2) / 2

    if median.is_integer():
        return int(median)

    return median


def finalize_stats(stats):
    """
    Macht aus der internen Statistik das endgültige Ergebnis.
    """
    if stats["word_count"] == 0:
        return None

    return {
        "word_count": stats["word_count"],
        "average": stats["total_length"] / stats["word_count"],
        "median": median_from_distribution(
            stats["distribution"],
            stats["word_count"]
        ),
        "longest_word": stats["longest_word"],
        "longest_length": stats["longest_length"],
        "distribution": stats["distribution"]
    }


def analyze(words):
    """
    Analyse für kleine Testdaten.
    """
    words = list(words)

    if len(words) == 0:
        return None

    stats = empty_stats()

    for _, word, length in words:
        add_word_with_length(stats, word, length)

    return finalize_stats(stats)