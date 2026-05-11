from text_processing import get_language, process
from statistics import analyze


# =========================
# Tests
# =========================

def run_tests():
    """
    Tests für die Dokumentation.
    """
    print("Starte Tests...")

    # Test 1: Sprache erkennen
    assert get_language("texts/german/test.txt") == "german"

    # Test 2: Wörter erkennen und Stopwords entfernen
    test_line = "Das Haus und Auto 123 !!!"
    result = process((test_line, "texts/german/test.txt"))

    assert result == [
        ("german", "haus"),
        ("german", "auto")
    ]

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

    # Test 4: Leere Liste analysieren
    empty_analysis = analyze([])
    assert empty_analysis is None

    # Test 5: Umlaute erkennen
    umlaut_result = process(("Äpfel größer schön 123 !!!", "texts/german/test.txt"))

    assert umlaut_result == [
        ("german", "äpfel"),
        ("german", "größer"),
        ("german", "schön")
    ]

    print("Alle Tests erfolgreich.")
    print("------")