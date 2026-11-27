from collections import Counter

from text_processing import get_language, process
from word_stats import analyze, empty_stats, add_word, merge_stats, finalize_stats


# =========================
# Tests
# =========================
# Funktionieren mit `python main.py` (über run_tests) und mit `pytest tests.py`.

def test_sprache_erkennen():
    # Test 1: Sprache aus dem Ordnernamen erkennen (auch mit Windows-Pfaden)
    assert get_language("texts/german/test.txt") == "german"
    assert get_language("texts\\german\\test.txt") == "german"


def test_woerter_und_stopwords():
    # Test 2: Wörter erkennen, Stopwords, Zahlen und Sonderzeichen entfernen
    result = process(("Das Haus und Auto 123 !!!", "texts/german/test.txt"))
    assert result == [("german", "haus"), ("german", "auto")]


def test_statistik():
    # Test 3: Statistik prüfen
    test_words = [
        ("german", "haus", 4),
        ("german", "auto", 4),
        ("german", "programm", 8)
    ]
    analysis = analyze(test_words)

    assert analysis["word_count"] == 3
    assert analysis["average"] == 16 / 3
    assert analysis["median"] == 4
    assert analysis["longest_word"] == "programm"
    assert analysis["longest_length"] == 8


def test_leere_liste():
    # Test 4: Leere Liste analysieren
    assert analyze([]) is None


def test_umlaute():
    # Test 5: Umlaute erkennen
    result = process(("Äpfel größer schön 123 !!!", "texts/german/test.txt"))
    assert result == [("german", "äpfel"), ("german", "größer"), ("german", "schön")]


def test_median_gerade_anzahl():
    # Test 6: Median bei gerader Anzahl = Mittelwert der beiden mittleren Werte
    analysis = analyze([("x", "ab", 2), ("x", "abc", 3), ("x", "abcd", 4), ("x", "abcde", 5)])
    assert analysis["median"] == 3.5


def test_merge_entspricht_gesamtanalyse():
    # Test 7: Teilstatistiken zusammenführen (wie bei Dask) ergibt dasselbe
    # wie eine Analyse aller Wörter auf einmal
    words_a = ["haus", "baum", "schiff"]
    words_b = ["auto", "programmierung", "zug"]

    part_a, part_b, combined = empty_stats(), empty_stats(), empty_stats()
    for w in words_a:
        add_word(part_a, w)
    for w in words_b:
        add_word(part_b, w)
    for w in words_a + words_b:
        add_word(combined, w)

    merged = merge_stats(part_a, part_b)
    assert finalize_stats(merged) == finalize_stats(combined)
    assert merged["distribution"] == Counter(len(w) for w in words_a + words_b)
    # Zusammenführen in umgekehrter Reihenfolge darf nichts ändern
    assert finalize_stats(merge_stats(part_b, part_a)) == finalize_stats(combined)


ALL_TESTS = [
    test_sprache_erkennen,
    test_woerter_und_stopwords,
    test_statistik,
    test_leere_liste,
    test_umlaute,
    test_median_gerade_anzahl,
    test_merge_entspricht_gesamtanalyse,
]


def run_tests():
    """
    Tests für die Dokumentation.
    """
    print("Starte Tests...")

    for test in ALL_TESTS:
        test()

    print(f"Alle {len(ALL_TESTS)} Tests erfolgreich.")
    print("------")


if __name__ == "__main__":
    run_tests()
