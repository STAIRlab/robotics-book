# Figure pass verification

Checked on 2026-11-11 against the revision based on `2b82435`.
This report covers the repository figures and notebooks. Live Overleaf
integration and full-book pagination require a separate manuscript check.

## Inventory and exports

- All 31 notebooks pass notebook-format validation. Their 105 code cells have
  stored execution counts, with no stored error outputs.
- The notebooks contain 39 inline PNG outputs and supply all 39 numerical PDF
  exports in `figures/`.
- All 39 PDFs are single-page files with selectable text. `pdffonts` reports
  only embedded Computer Modern fonts.
- Export widths are exactly 4.6 inches (24 figures) or 6.5 inches (15 figures).
  PDF creation and modification dates are omitted. PNG exports use 200 dpi.
- Figure renders were visually reviewed for clipping, overlaps, label
  legibility and consistency. The latest sensor geometry and belief-geometry
  exports were checked after their annotation corrections.

## Execution and numerical checks

- The 29 plotting notebooks were executed from top to bottom in independent
  Python processes with IPython, using the pinned Python 3.12 environment.
  Repeated execution leaves their notebook files and PDF/PNG exports
  byte-identical.
- The two original print-only notebooks are byte-identical to both the branch
  baseline and the previously executed audit copies. Their successful prior
  execution was retained without rerunning unchanged calculations.
- All original filter-comparison result arrays remain bitwise identical.
  The notebook now distinguishes mean run RMSE from pooled RMSE.
- The recovered chapter calculations reproduce the earlier numerical result
  dictionaries. The path-cost notebook uses the original seed-0 samples.
- Both chapter test cases pass: selected book values, the unobserved SLAM
  gauge, and the variance behavior of smoothing.
- A clean virtual environment successfully installs every pin in
  `requirements-dev.txt`; `pip check` reports no broken requirements.
- Every relative file link in the repository README resolves.

## Important interpretation details

- GP observations use the book's legacy seed-42 draws. The stated zero mean
  and observation variance remain explicit modeling choices.
- EKF and UKF example lengths remain 30 and 20 steps. A 2-sigma ellipse in
  two dimensions encloses approximately 86.5%, not 95%, probability.
- The motion-planning crossover uses the sample moments:
  `lambda = 0.10520367149494089`; the original discrete-grid switch remains
  `0.12`.
- Rare-event ordinary-MC empirical error markers are shown only where the
  expected number of exceedances per run is at least five. Exact error curves
  retain their full plotted range.

## Execution limitation

The host prevents the network-interface operations used by a Jupyter kernel's
ZMQ transport. Native `nbclient` kernel startup was attempted and failed before
executing notebook cells. Fresh-process IPython execution and repeat-file
checks therefore support the results above; a successful native Jupyter
"Restart Kernel and Run All" is not claimed for this host.
