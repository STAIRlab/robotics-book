# Bayesian Robotics Book - Companion Notebooks

Computational examples for **Bayesian Methods for Autonomous Robotics and Intelligent Infrastructure Systems: Probabilistic Perception, Estimation, and Digital Twins**, by **Khalid M. Mosalam**, Taisei Professor of Civil Engineering, University of California, Berkeley.

The notebooks are organized by topic. Each can be run independently from top to bottom, and some support several chapters. The larger notebooks contain their numerical calculations directly. Short chapter notebooks call the inspectable [chapter_examples.py](robotics_book/chapter_examples.py) implementation and print their computed values. The shared [book.mplstyle](notebooks/book.mplstyle) file controls figure appearance only.

## Contributors and maintainers

- **Fan Hu**, Structural Artificial Intelligence Research Laboratory (STAIRlab), University of California, Berkeley
- **Khalid M. Mosalam**, Taisei Professor of Civil Engineering, University of California, Berkeley
- **Ziad Mosalam**, author of the six additional companion notebooks and the visual design of the numerical figures and restyled book diagrams

The original notebook and diagram credits are retained. Other contributors to the book are acknowledged in the book.

## Setup and use

Use Python 3.12. In your Python environment, install the pinned dependencies from the repository root:

```bash
python -m pip install -r requirements.txt
```

Notebook execution tools are listed separately in `requirements-dev.txt`. To install them for automated execution and validation, use `python -m pip install -r requirements-dev.txt`. They are not imported by the numerical examples.

Open a notebook in JupyterLab, Jupyter Notebook, or a notebook-capable editor, using that Python environment. To install and launch JupyterLab:

```bash
python -m pip install jupyterlab
cd notebooks
python -m jupyterlab
```

Choose **Restart Kernel and Run All Cells**. Run with `notebooks/` as the working directory so the shared style and relative export paths resolve correctly. Plotting notebooks display each figure inline and save matching **PDF and PNG** files in [figures/](figures/). Rerunning a notebook refreshes its exports. The two original print-only notebooks continue to print numerical results.

For Conda, [environment.yml](environment.yml) creates the `bayesian_robotics` environment using the same pinned requirements and adds JupyterLab:

```bash
conda env create -f environment.yml
conda activate bayesian_robotics
cd notebooks
jupyter lab
```

## Original six notebooks

The numerical calculations in these notebooks are preserved. Four have updated plotting cells and figure exports. The two print-only notebooks, `bayesian-inference-basics.ipynb` and `monte-carlo-methods.ipynb`, are unchanged.

| Notebook | Topic | Output |
|---|---|---|
| [bayesian-inference-basics.ipynb](notebooks/bayesian-inference-basics.ipynb) | Bayes' theorem, updating, inference and prediction: localization, stop-sign detection, radar tracking, pedestrian motion and Gaussian processes | Printed numerical results |
| [sensor-models.ipynb](notebooks/sensor-models.ipynb) | Range and bearing geometry, likelihood, Gauss-Newton estimation, observability and camera projection | 4 figures: `sensor-models-geometry`, `sensor-models-likelihood`, `sensor-models-gauss-newton`, `sensor-models-camera` |
| [kalman-filters.ipynb](notebooks/kalman-filters.ipynb) | Scalar Kalman filtering, EKF and UKF examples | Printed results and 2 figures: `kalman-ekf-state-measurement`, `kalman-ukf-state-measurement` |
| [particle-filters.ipynb](notebooks/particle-filters.ipynb) | Particle localization, a fixed small-example walkthrough and comparison with an EKF | Printed tables and `particle-filters-comparison` |
| [monte-carlo-methods.ipynb](notebooks/monte-carlo-methods.ipynb) | Expected path costs and estimation of pi | Printed numerical results |
| [motion-planning-under-uncertainty.ipynb](notebooks/motion-planning-under-uncertainty.ipynb) | Belief geometry, risk-sensitive costs and information-gathering actions | 6 figures with the `motion-planning-` prefix: `belief-geometry`, `risk-tradeoff`, `cost-distributions`, `policy-trajectories`, `uncertainty-history`, `information-tradeoff` |

Every figure name in the tables denotes both a `.pdf` and a `.png` file in `figures/`.

The sensor estimate converges to approximately **(5.245, 3.088)**. The particle-filter walkthrough reproduces all three book tables and the means **7.0631** before resampling and **7.0608** after the fixed draw. Motion-planning goal-distance labels refer to the **belief mean**. Its plotted covariance ellipses have Mahalanobis radius 2; they are not labeled as 95% regions.

## Additional companion notebooks

These six notebooks are authored by **Ziad Mosalam**. They develop selected examples where a complete calculation and an informative figure support the book's discussion.

| Notebook | Topic | Output |
|---|---|---|
| [gaussian-process-prediction.ipynb](notebooks/gaussian-process-prediction.ipynb) | Prediction after observations stop, comparing two covariance models on the same data | `gaussian-process-prediction` |
| [filter-comparison.ipynb](notebooks/filter-comparison.ipynb) | EKF, UKF and particle filtering on shared observations over 64 independent runs | `comparison-trajectory`, `comparison-diagnostics` |
| [condition-monitoring.ipynb](notebooks/condition-monitoring.ipynb) | Hidden Markov filtering and smoothing of a noisy condition indicator | `condition-monitoring` |
| [bayesian-decisions.ipynb](notebooks/bayesian-decisions.ipynb) | Posterior expected losses, action selection and the value of another inspection | `bayesian-decisions` |
| [rare-event-monte-carlo.ipynb](notebooks/rare-event-monte-carlo.ipynb) | Ordinary Monte Carlo and importance sampling against an analytic probability | `rare-event-monte-carlo` |
| [slam.ipynb](notebooks/slam.ipynb) | Weighted pose-graph optimization and the effect of a loop closure | `slam-loop-closure` |

## Chapter calculations used by the book

These 19 notebooks restore the generating code for numerical illustrations already included in the manuscript. They preserve the earlier calculation inputs and outputs while exporting vector PDFs with selectable Computer Modern text at a fixed physical width. Each notebook displays its figure and prints the numerical values. The first 18 use [chapter_examples.py](robotics_book/chapter_examples.py); `monte-carlo-path-costs` contains its calculation directly. JSON records are written to `results/`.

| Notebook | Figure and calculation |
|---|---|
| [bayes-theorem.ipynb](notebooks/bayes-theorem.ipynb) | Three-location posterior |
| [bayesian-updating.ipynb](notebooks/bayesian-updating.ipynb) | Repeated independent detections |
| [bayesian-inference.ipynb](notebooks/bayesian-inference.ipynb) | Scalar Gaussian update |
| [bayesian-prediction.ipynb](notebooks/bayesian-prediction.ipynb) | Velocity and acceleration contributions to variance |
| [real-time-bayesian-systems.ipynb](notebooks/real-time-bayesian-systems.ipynb) | Cumulative latency and deadline |
| [kalman-filter.ipynb](notebooks/kalman-filter.ipynb) | Sequential scalar-update variances |
| [extended-kalman-filter.ipynb](notebooks/extended-kalman-filter.ipynb) | Normalized variances after one range update |
| [unscented-kalman-filter.ipynb](notebooks/unscented-kalman-filter.ipynb) | Squaring and its linearization at zero |
| [bayesian-decision-theory.ipynb](notebooks/bayesian-decision-theory.ipynb) | Renewal-reward inspection interval |
| [probabilistic-robotics.ipynb](notebooks/probabilistic-robotics.ipynb) | Condition-state Bayes filter |
| [hidden-markov-models.ipynb](notebooks/hidden-markov-models.ipynb) | Three-observation forward probabilities |
| [bayesian-learning.ipynb](notebooks/bayesian-learning.ipynb) | Sensor-bias posterior variance |
| [general-state-space-models.ipynb](notebooks/general-state-space-models.ipynb) | Filtering and backward smoothing variances |
| [probabilistic-graphical-models.ipynb](notebooks/probabilistic-graphical-models.ipynb) | Exact enumeration of a chain |
| [computer-vision.ipynb](notebooks/computer-vision.ipynb) | Coordinate-error propagation |
| [slam-foundations.ipynb](notebooks/slam-foundations.ipynb) | Global-shift and relative variances; exports `slam` |
| [digital-twins.ipynb](notebooks/digital-twins.ipynb) | Model-discrepancy calibration |
| [infrastructure-applications.ipynb](notebooks/infrastructure-applications.ipynb) | Recomputation of the printed modal-period table |
| [monte-carlo-path-costs.ipynb](notebooks/monte-carlo-path-costs.ipynb) | Seed-0 path-cost means and standard errors; exports `monte-carlo-results` |

Except for the two explicit export names above, each figure uses its notebook's stem. The infrastructure example recomputes a printed table; it does not validate the model against a newly supplied field dataset. `slam-foundations` is a two-variable gauge illustration, while `slam` remains the separate pose-graph notebook. `monte-carlo-path-costs` uses exactly the same seed-0 samples as the original print-only `monte-carlo-methods` notebook.

The numerical checks in `tests/test_chapter_examples.py` verify selected book values, preservation of the unobserved SLAM gauge, and non-increasing variance under smoothing. Run them from the repository root:

```bash
python -m unittest discover -s tests -p test_chapter_examples.py -v
```

## Data and interpretation

Stochastic examples declare fixed seeds. All observations, routes and costs are synthetic or explicitly illustrative. The small particle-filter walkthrough uses the book's fixed positions and resampling indices. No external dataset or account is required.

Each new notebook states its model assumptions, explains the plotted quantities and includes numerical checks. The filter comparison supports conclusions about its particular nonlinear scenario. The condition states and decision costs are teaching assumptions, not calibrated structural condition or maintenance recommendations. The SLAM example supplies the loop correspondence and demonstrates the pose-graph back end; it does not perform feature association. The rare-event example uses a known Gaussian limit state, while the Gaussian-process intervals are conditional on the stated covariance and noise models.

## Book diagrams and visual style

The figures use the **Berkeley editorial** design: serif mathematical typography, deep blue, restrained gold, consistent line weights and clear distinctions between observations, estimates and uncertainty. Color is supplemented by labels, markers or line patterns where needed.

The [37 standalone TikZ diagrams](figures/tikz/README.md) use the same design. Their editable `.tex` sources and compiled PDFs are in [figures/tikz/](figures/tikz/). The [source index](figures/tikz/figure-sources.json) maps each diagram to its book source and figure label. These diagrams compile with LaTeX independently of the notebooks. Curves identified as schematics illustrate concepts rather than measured or simulated results.

## License

The notebooks and figures are licensed under **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**, as in the book. See [LICENSE](LICENSE) for the legal code and the [CC BY-NC 4.0 license page](https://creativecommons.org/licenses/by-nc/4.0/).
