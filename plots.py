import os
import matplotlib.pyplot as plt

from config import OUTPUT_FOLDER


# =========================
# Diagramme
# =========================

def plot_histogram(language, distribution):
    """
    Erstellt ein Histogramm für eine Sprache.
    """
    x = sorted(distribution.keys())
    y = [distribution[length] for length in x]

    plt.figure()
    plt.bar(x, y)
    plt.xlabel("Wortlänge")
    plt.ylabel("Anzahl")
    plt.title(f"Histogramm - {language}")
    plt.tight_layout()

    path = os.path.join(OUTPUT_FOLDER, f"{language}_histogramm.png")
    plt.savefig(path)
    plt.close()


def plot_runtime_comparison(serial_time, dask_time):
    """
    Erstellt ein Diagramm für den normalen Laufzeitvergleich.
    """
    methods = ["Seriell", "Dask"]
    times = [serial_time, dask_time]

    plt.figure()
    plt.bar(methods, times)
    plt.xlabel("Methode")
    plt.ylabel("Zeit in Sekunden")
    plt.title("Laufzeitvergleich")
    plt.tight_layout()

    path = os.path.join(OUTPUT_FOLDER, "laufzeitvergleich.png")
    plt.savefig(path)
    plt.close()


def plot_scaling_benchmark(benchmark_rows):
    """
    Erstellt ein Diagramm für den Skalierungstest.
    """
    file_counts = [row["file_count"] for row in benchmark_rows]
    serial_times = [row["serial_time"] for row in benchmark_rows]
    dask_times = [row["dask_time"] for row in benchmark_rows]

    plt.figure()
    plt.plot(file_counts, serial_times, marker="o", label="Seriell")
    plt.plot(file_counts, dask_times, marker="o", label="Dask")
    plt.xlabel("Anzahl der verarbeiteten Dateien")
    plt.ylabel("Zeit in Sekunden")
    plt.title("Benchmark und Skalierungstest")
    plt.legend()
    plt.tight_layout()

    path = os.path.join(OUTPUT_FOLDER, "skalierung_laufzeit.png")
    plt.savefig(path)
    plt.close()


def save_summary_image(results):
    """
    Speichert die Ergebnisse der Textanalyse als reine Tabelle.

    Es werden keine Laufzeitwerte, kein Speedup und kein zusätzlicher Titel angezeigt.
    Laufzeiten und Speedup werden separat im Laufzeitvergleich und in der Benchmark-Tabelle dargestellt.
    """
    rows = []

    for language in sorted(results.keys()):
        data = results[language]

        rows.append([
            language,
            f"{data['word_count']:,}".replace(",", "."),
            f"{data['average']:.2f}",
            data["median"],
            data["longest_word"],
            data["longest_length"]
        ])

    columns = [
        "Sprache",
        "Wortanzahl",
        "Durchschnitt",
        "Median",
        "Längstes Wort",
        "Länge"
    ]

    # Größeres Bild für bessere Lesbarkeit
    fig, ax = plt.subplots(figsize=(28, 7))
    ax.axis("off")

    col_widths = [
        0.10,  # Sprache
        0.13,  # Wortanzahl
        0.13,  # Durchschnitt
        0.09,  # Median
        0.45,  # Längstes Wort
        0.10   # Länge
    ]

    table = ax.table(
        cellText=rows,
        colLabels=columns,
        cellLoc="center",
        loc="center",
        colWidths=col_widths
    )

    # Größere Schrift
    table.auto_set_font_size(False)
    table.set_fontsize(13)

    # Tabelle größer skalieren: Breite, Höhe
    table.scale(1.15, 2.2)

    # Kopfzeile hervorheben und längstes Wort linksbündig ausrichten
    for (row, col), cell in table.get_celld().items():
        cell.set_linewidth(0.8)

        if row == 0:
            cell.set_text_props(weight="bold")
            cell.set_height(0.09)

        if col == 4 and row != 0:
            cell.get_text().set_ha("left")

    path = os.path.join(OUTPUT_FOLDER, "zusammenfassung_ergebnisse.png")

    # Hohe dpi für bessere Qualität
    plt.savefig(
        path,
        dpi=400,
        bbox_inches="tight",
        pad_inches=0.08
    )

    plt.close()

def save_benchmark_table_image(benchmark_rows):
    """
    Speichert die Benchmark-Ergebnisse als Tabelle.
    """
    rows = []

    for row in benchmark_rows:
        rows.append([
            row["file_count"],
            round(row["serial_time"], 4),
            round(row["dask_time"], 4),
            round(row["speedup"], 2)
        ])

    columns = [
        "Dateien",
        "Seriell in s",
        "Dask in s",
        "Speedup"
    ]

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.axis("off")

    ax.set_title("Benchmark und Skalierungstest", fontsize=14, pad=20)

    table = ax.table(
        cellText=rows,
        colLabels=columns,
        cellLoc="center",
        loc="center"
    )

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.6)

    path = os.path.join(OUTPUT_FOLDER, "benchmark_tabelle.png")
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()