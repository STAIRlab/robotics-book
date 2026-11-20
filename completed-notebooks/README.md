# Completed companion notebooks — Chapters 2–8

This directory is the **working index** of chapter-specific Jupyter notebooks reviewed during the book's chapter-by-chapter scientific and editorial inspection. The files themselves remain in [`../notebooks/`](../notebooks/) as the **single authoritative copies**, so their imports, tests, and figure-export paths continue to work. The canonical working branch is `book-figure-revision`; do **not** treat `main` as the finalized source during this review.

| Chapter | Notebook | Topic |
|---|---|---|
| 2 | [JNB2 — bayes-theorem.ipynb](../notebooks/bayes-theorem.ipynb) | Bayes' theorem |
| 3 | [JNB3 — bayesian-updating.ipynb](../notebooks/bayesian-updating.ipynb) | Bayesian updating |
| 4 | [JNB4 — bayesian-inference.ipynb](../notebooks/bayesian-inference.ipynb) | Bayesian inference |
| 5 | [JNB5 — bayesian-prediction.ipynb](../notebooks/bayesian-prediction.ipynb) | Bayesian prediction |
| 6 | [JNB6 — real-time-bayesian-systems.ipynb](../notebooks/real-time-bayesian-systems.ipynb) | Real-time Bayesian systems |
| 7 | [JNB7 — sensor-models.ipynb](../notebooks/sensor-models.ipynb) | Sensor models |
| 8 | [JNB8 — kalman-filter.ipynb](../notebooks/kalman-filter.ipynb) | Linear Kalman filtering and GPS-dropout tracking |

## Review and release status

**Included in the completed-chapter working collection** means the notebook is the current chapter-review choice; it does *not* assert that the whole book, every figure, or every notebook has passed a final release test.

- Chapters 2–7: current chapter notebook files are linked above. Preserve them while reviewing later chapters.
- Chapter 8: the integrated notebook includes the earlier one-dimensional examples, Gaussian update, two-dimensional tracking, and the branch's original sequential-update example. Its embedded code exports `JNB8-KF.pdf` and `JNB8-KF.png` to `figures/` when run from `notebooks/`. **Final run-all validation and standalone PDF/PNG figure commits are still pending.**
- Chapters 9 onward: add a link here **after** completing each chapter's review. The existing shared notebook `notebooks/kalman-filters.ipynb` still contains EKF and UKF examples and is not the dedicated JNB8.
- Contributor credits and source history should remain in each notebook and the Git commit history.

## How to use

From the repository root, install `requirements.txt`; launch JupyterLab from `notebooks/`, then open the linked notebook. Run all cells from top to bottom and inspect outputs and exported figures.

At the end of the chapter-by-chapter review, reconcile duplicate legacy notebooks, verify figure exports and regression tests, and only then plan a controlled merge to `main`.
