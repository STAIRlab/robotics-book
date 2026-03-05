# Bayesian Robotics Book - Companion Notebooks

This repository contains companion Jupyter notebooks for the book:

**Bayesian Methods for Autonomous Robotics and Intelligent Infrastructure Systems: Probabilistic Perception, Estimation, and Digital Twins**

Book author:  
**Khalid M. Mosalam**  
Taisei Professor of Civil Engineering  
University of California, Berkeley

The notebooks provide computational examples and reproducible implementations of key concepts discussed in the book.

Repository maintained by:

**Dr. Fan Hu**  
Structural Artificial Intelligence Research Laboratory (STAIRlab)  
University of California, Berkeley

---

## Repository Structure

notebooks/ – Jupyter notebooks organized by chapter  
data/ – sample datasets used in examples  
figures/ – images used in notebooks  

---

## Notebooks

| Chapter | Notebook |
|-------|------|
| Sensor Models | notebooks/ch06_sensor_models.ipynb |
| Kalman Filter | notebooks/ch07_kalman_filter.ipynb |
| EKF | notebooks/ch08_ekf.ipynb |
| UKF | notebooks/ch09_ukf.ipynb |

---

## Installation

### Clone the repository:

```bash
git clone https://github.com/stairlab/robotics-book.git
cd robotics-book
```

### Install dependencies:

#### Option 1: Install using pip
```bash
pip install -r requirements.txt
```

#### Option 2: Install using Conda (recommended)
```bash
conda env create -f environment.yml
conda activate bayesian_robotics
```

### Launch Jupyter:
```bash
jupyter notebook
```

---

## Reproducibility

The notebooks are designed to reproduce the computational examples presented in the book.

Each notebook can be run independently and corresponds to a specific chapter.

---

## License

Educational and research use.
