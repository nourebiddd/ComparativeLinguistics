# 📊 ComparativeLinguistics
**Parallele Textanalyse mit Dask** | *Parallel Text Analysis with Dask*

> A Python application that analyzes text files across multiple languages, computes word-length statistics, and compares serial vs. parallel processing performance using **Dask**.

---

- **Noureldin Ebid**

**Module:** Programmierkonzepte und Algorithmen  
**Date:** June 2026

---

## 📌 Overview

ComparativeLinguistics processes hundreds of text files organized by language, automatically detects the language from the folder name, cleans the text, and computes statistical metrics on word lengths. The core question it answers:

> *How well can Dask parallelize the processing of many text files, and what runtime advantage does it offer over serial processing?*

---

## 🗂️ Project Structure

```
ComparativeLinguistics/
│
├── texts/
│   ├── Dutch/
│   ├── English/
│   ├── French/
│   ├── German/
│   ├── Italian/
│   ├── Russian/
│   ├── Spanish/
│   └── Ukrainian/
│
├── Ergebnisse/          # generated charts and tables
├── main.py              # entry point
├── config.py            # paths, stopwords, Dask settings
├── text_processing.py   # language detection, word extraction
├── word_stats.py        # statistics (mergeable, used by Dask)
├── analysis.py          # serial + Dask analysis, benchmark
├── plots.py             # histograms and benchmark charts
├── tests.py             # functional tests
├── requirements.txt
└── README.md
```

---

## ⚙️ Features

- 🔍 **Automatic language detection** from folder/file path
- 🧹 **Text cleaning** — removes stopwords, numbers, and special characters
- 📐 **Statistical metrics** per language:
  - Word count
  - Average word length
  - Median word length
  - Longest word
  - Word-length frequency distribution
- ⚡ **Parallel processing** with `dask.bag`
- 📊 **Runtime comparison** — serial vs. Dask
- 📈 **Scaling benchmark** with 364, 728, and 1456 files
- ✅ **7 functional tests**, plus a correctness check (serial == parallel) on every run

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install -r requirements.txt
```

### Run the analysis

```bash
python main.py
```

This will:
1. Run the functional tests
2. Run the serial analysis
3. Run the parallel Dask analysis
4. Compare results and runtimes
5. Generate histograms and benchmark charts

---

## 📊 Results Summary

| Language  | Word Count | Avg Length | Median |
|-----------|-----------|------------|--------|
| Dutch     | 115,793   | 4.64       | 4      |
| English   | 4,629,131 | 4.46       | 4      |
| French    | 5,325,444 | 4.54       | 4      |
| **German**| 4,598,668 | **5.41**   | 5      |
| Italian   | 3,119,246 | 4.92       | 5      |
| Russian   | 362,614   | 4.98       | 5      |
| Spanish   | 1,406,426 | 4.74       | 4      |
| Ukrainian | 809,177   | 4.54       | 4      |

> German has the highest average word length (5.41) — characteristic of compound word formation (*Komposita*).

---

## ⚡ Performance

| Method | Files | Runtime  | Speedup |
|--------|-------|----------|---------|
| Serial | 364   | 14.69 s  | 1.00×   |
| Dask   | 364   |  3.45 s  | **4.26×**|
| Dask   | 728   |  5.37 s  | **5.49×**|
| Dask   | 1456  |  9.93 s  | **5.70×**|

The larger the dataset, the greater the advantage of parallel processing.

---

## 🧪 Tests

Run them on their own with `python tests.py` or `pytest tests.py`:

| # | Test |
|---|------|
| 1 | Language detection from file path (Unix and Windows paths) |
| 2 | Word extraction with stopword, number & special-character removal |
| 3 | Correct statistical calculation |
| 4 | Empty input handling |
| 5 | German umlaut recognition (ä, ö, ü) |
| 6 | Median with an even number of words |
| 7 | Merging partial statistics (as Dask does) equals analysing everything at once |

In addition, `main.py` asserts that the serial and the Dask results are identical ✅

---

## 🛠️ Tech Stack

- **Python 3**
- **Dask** — parallel computing
- **Matplotlib** — charts and histograms
- **re / collections** — text processing

---

## 📄 License

This project was created for academic purposes.
