import os


# =========================
# Projekt-Einstellungen
# =========================

PROJECT_NAME = "ComparativeLinguistics"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEXT_PATH = os.path.join(BASE_DIR, "texts", "*", "*.txt")

OUTPUT_FOLDER = os.path.join(BASE_DIR, "Ergebnisse")


# =========================
# Text-Einstellungen
# =========================

WORD_PATTERN = r"[^\W\d_]+"

STOPWORDS = {
    "the", "and", "a", "an", "of",
    "und", "mit", "der", "die", "das",
    "la", "le", "et"
}


# =========================
# Dask-Einstellungen
# =========================

DASK_SCHEDULER = "processes"

NUM_WORKERS = max(1, (os.cpu_count() or 2) - 1)


# =========================
# Benchmark-Einstellungen
# =========================

BENCHMARK_FACTORS = [1, 2, 4]