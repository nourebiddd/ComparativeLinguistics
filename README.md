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
├── main.py
├── analysis.py
├── stats.py
├── tests.py
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
- ✅ **7 functional tests** including correctness check (serial == parallel)

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install dask matplotlib
```

### Run the analysis

```bash
python main.py
```

This will:
1. Run the serial analysis
2. Run the parallel Dask analysis
3. Compare results and runtimes
4. Generate histograms and benchmark charts

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

All 7 functional tests pass:

| # | Test |
|---|------|
| 1 | Language detection from file path |
| 2 | Word extraction from a line |
| 3 | Stopword, number & special char removal |
| 4 | Correct statistical calculation |
| 5 | Empty input handling |
| 6 | German umlaut recognition (ä, ö, ü) |
| 7 | Serial and parallel results are identical ✅ |

---

## 🛠️ Tech Stack

- **Python 3**
- **Dask** — parallel computing
- **Matplotlib** — charts and histograms
- **re / collections** — text processing

---

## 📄 License

This project was created for academic purposes.
