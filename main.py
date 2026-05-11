import os
import glob
from multiprocessing import freeze_support

from config import (
    PROJECT_NAME,
    TEXT_PATH,
    OUTPUT_FOLDER,
    DASK_SCHEDULER,
    NUM_WORKERS
)

from analysis import (
    measure_time,
    run_serial_analysis_with_files,
    run_dask_analysis_with_files,
    run_scaling_benchmark
)

from plots import (
    plot_histogram,
    plot_runtime_comparison,
    plot_scaling_benchmark,
    save_summary_image,
    save_benchmark_table_image
)

from tests import run_tests


# =========================
# Hauptprogramm
# =========================

def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    files = sorted(glob.glob(TEXT_PATH))

    if len(files) == 0:
        print("Keine Textdateien gefunden.")
        print("Prüfe diesen Pfad:")
        print(TEXT_PATH)
        return

    print(f"Projekt: {PROJECT_NAME}")
    print("------")

    # 1. Einstellungen anzeigen
    print(f"Gefundene Textdateien: {len(files)}")
    print(f"Dask Scheduler: {DASK_SCHEDULER}")
    print(f"Dask Worker: {NUM_WORKERS}")
    print(f"Dask Partitionen: {len(files)}")
    print("Hinweis: Eine Datei entspricht einer Dask-Partition.")
    print("------")

    # 2. Tests starten
    run_tests()

    # 3. Normale Analyse
    print("Starte serielle Analyse...")
    serial_result, serial_time = measure_time(
        lambda: run_serial_analysis_with_files(files)
    )

    print("Starte Dask-Analyse...")
    dask_result, dask_time = measure_time(
        lambda: run_dask_analysis_with_files(files)
    )

    assert serial_result == dask_result
    print("Serielle Analyse und Dask-Analyse liefern gleiche Ergebnisse.")

    speedup = serial_time / dask_time

    # 4. Ergebnisse anzeigen
    print("------")
    print("Ergebnisse:")

    for language, data in dask_result.items():
        print(f"Sprache: {language}")
        print(f"Wortanzahl: {data['word_count']}")
        print(f"Durchschnitt: {round(data['average'], 2)}")
        print(f"Median: {data['median']}")
        print(
            f"Längstes Wort: {data['longest_word']} "
            f"({data['longest_length']})"
        )
        print("Histogramm wurde gespeichert.")
        print("------")

        plot_histogram(language, data["distribution"])

    # 5. Diagramme für normale Analyse speichern
    plot_runtime_comparison(serial_time, dask_time)
    save_summary_image(dask_result)

    # 6. Benchmark starten
    first_benchmark_row = {
        "file_count": len(files),
        "serial_time": serial_time,
        "dask_time": dask_time,
        "speedup": speedup
    }

    benchmark_rows = run_scaling_benchmark(files, first_benchmark_row)

    # 7. Benchmark-Diagramme speichern
    plot_scaling_benchmark(benchmark_rows)
    save_benchmark_table_image(benchmark_rows)

    print("Diagramme gespeichert in:")
    print(OUTPUT_FOLDER)


if __name__ == "__main__":
    freeze_support()
    main()