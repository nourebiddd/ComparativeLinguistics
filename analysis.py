import time
import dask.bag as db

from config import (
    DASK_SCHEDULER,
    NUM_WORKERS,
    BENCHMARK_FACTORS
)

from text_processing import analyze_file

from statistics import (
    empty_stats,
    merge_stats,
    finalize_stats
)


# =========================
# Laufzeitmessung
# =========================

def measure_time(function):
    """
    Misst die Laufzeit einer Funktion.
    """
    start = time.perf_counter()
    result = function()
    end = time.perf_counter()

    runtime = end - start

    return result, runtime

# =========================
# Dask-Analyse
# =========================

def run_dask_analysis_with_files(files):
    """
    Dask-Analyse mit einer übergebenen Dateiliste.

    Wichtig:
    partition_size=1 bedeutet:

    German/datei1.txt  -> Partition 1
    German/datei2.txt  -> Partition 2
    English/datei1.txt -> Partition 3

    Also:
    eine Datei = eine Dask-Partition.
    """
    if len(files) == 0:
        return {}

    result = (
        db.from_sequence(files, partition_size=1)
        .map(analyze_file)
        .foldby(
            key=lambda item: item[0],
            binop=lambda accumulator, item: merge_stats(accumulator, item[1]),
            initial=empty_stats(),
            combine=merge_stats,
            combine_initial=empty_stats(),
            split_every=8
        )
        .compute(
            scheduler=DASK_SCHEDULER,
            num_workers=NUM_WORKERS
        )
    )

    return {
        language: finalize_stats(stats)
        for language, stats in result
    }


# =========================
# Serielle Analyse
# =========================

def run_serial_analysis_with_files(files):
    """
    Serielle Analyse mit einer übergebenen Dateiliste.

    Die Dateien werden nacheinander verarbeitet.
    """
    all_stats = {}

    for file_path in files:
        language, file_stats = analyze_file(file_path)

        if language not in all_stats:
            all_stats[language] = empty_stats()

        all_stats[language] = merge_stats(
            all_stats[language],
            file_stats
        )

    result = {}

    for language, stats in all_stats.items():
        result[language] = finalize_stats(stats)

    return result


# =========================
# Benchmark
# =========================

def run_scaling_benchmark(base_files, first_benchmark_row):
    """
    Führt Benchmark-Tests mit mehreren Datengrößen aus.

    Die normale Analyse mit 364 Dateien wurde bereits vorher berechnet.
    Deshalb wird sie als erster Benchmark-Wert übernommen.

    Dadurch wird die Datenmenge 364 nicht doppelt berechnet.
    """
    benchmark_rows = []

    print("Benchmark-Faktoren:", BENCHMARK_FACTORS)
    print("Starte Benchmark und Skalierungstest...")
    print("------")

    # 1. Bereits gemessene normale Analyse als erster Benchmark-Wert übernehmen
    benchmark_rows.append(first_benchmark_row)

    print(f"Benchmark mit {first_benchmark_row['file_count']} Dateien")
    print(f"Dask-Partitionen: {first_benchmark_row['file_count']}")
    print("Hinweis: Eine Datei entspricht einer Dask-Partition.")
    print(f"Seriell: {round(first_benchmark_row['serial_time'], 4)} Sekunden")
    print(f"Dask: {round(first_benchmark_row['dask_time'], 4)} Sekunden")
    print(f"Speedup: {round(first_benchmark_row['speedup'], 2)}")
    print("------")

    # 2. Nur noch größere Datenmengen berechnen
    for factor in BENCHMARK_FACTORS:
        if factor == 1:
            continue

        benchmark_files = base_files * factor
        file_count = len(benchmark_files)

        print(f"Benchmark mit {file_count} Dateien")
        print(f"Dask-Partitionen: {file_count}")
        print("Hinweis: Eine Datei entspricht einer Dask-Partition.")

        serial_result, serial_time = measure_time(
            lambda: run_serial_analysis_with_files(benchmark_files)
        )

        dask_result, dask_time = measure_time(
            lambda: run_dask_analysis_with_files(benchmark_files)
        )

        assert serial_result == dask_result

        speedup = serial_time / dask_time

        print(f"Seriell: {round(serial_time, 4)} Sekunden")
        print(f"Dask: {round(dask_time, 4)} Sekunden")
        print(f"Speedup: {round(speedup, 2)}")
        print("------")

        benchmark_rows.append({
            "file_count": file_count,
            "serial_time": serial_time,
            "dask_time": dask_time,
            "speedup": speedup
        })

    return benchmark_rows