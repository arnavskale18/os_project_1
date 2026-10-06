# Adaptive Banker's Algorithm for Efficient and Fair Deadlock Avoidance

An interactive academic simulation system comparing the **Classical Banker's Algorithm** with an **Adaptive Banker's Algorithm** featuring **EWMA Runtime Demand Estimation** and **Starvation-Aware Candidate Ranking**.

---

## 📌 Project Overview

Deadlock avoidance in operating systems traditionally relies on Dijkstra's **Banker's Algorithm**. While Classical Banker strictly prevents deadlocks by granting only resource requests that guarantee a safe state, it suffers from key operational limitations:
1. **Arbitrary Safe Selection**: When multiple processes issue safe requests simultaneously, Classical Banker selects arbitrarily (or FCFS), ignoring process wait times and aging.
2. **Process Starvation**: Low-priority processes or processes requesting larger resource chunks can be deferred indefinitely while smaller safe requests are repeatedly granted.
3. **Static Max Claims**: Conventional Banker assumes static maximum claim vectors without observing actual runtime demand patterns.

### 🌟 The Adaptive Banker Solution

Our **Adaptive Banker's Algorithm** enhances Classical Banker with two dynamic layers:
1. **Runtime Demand Estimation (EWMA)**: Observes actual process resource requests over time to compute exponentially weighted moving averages and estimate likely future demand.
2. **Starvation-Aware Candidate Ranking**: Evaluates all pending requests against the Banker Safety Test, and then ranks **only SAFE candidates** using a multi-factor composite score (Waiting Time, Process Priority, Resource Efficiency, and Aging Score).

> ⚠️ **HARD SAFETY GUARANTEE**: Banker Safety Verification remains mandatory. Runtime demand estimation and starvation ranking **NEVER** allow an unsafe request to be granted. Safety violations remain strictly **0**.

---

## 🧮 Mathematical Foundations

### 1. EWMA Runtime Demand Estimation

For process $P_i$ requesting resource vector $\mathbf{R}(t)$ at time step $t$:

$$\mathbf{Prediction}(t) = \alpha \cdot \mathbf{Observation}(t) + (1-\alpha) \cdot \mathbf{Prediction}(t-1)$$

Where $\alpha = 0.6$ by default.

Estimated demand with safety margin $S = 1.0$:

$$\mathbf{EstimatedDemand} = \lceil \mathbf{Prediction}(t) + S \rceil$$

### 2. Starvation-Aware Ranking Formula

For every candidate request passing the Banker Safety test:

$$\text{Score} = 0.40 \cdot \text{WaitingScore} + 0.20 \cdot \text{PriorityScore} + 0.20 \cdot \text{EfficiencyScore} + 0.20 \cdot \text{AgingScore}$$

Where:
- **WaitingScore**: $\frac{\text{waiting\_time}}{\max(1, \text{max\_wait\_in\_system})}$
- **PriorityScore**: $\frac{\text{priority}}{10.0}$
- **EfficiencyScore**: $\frac{1}{2} \left( \frac{\sum \text{Request}}{\max(1, \sum \text{Need})} + \frac{\sum \text{Request}}{\max(1, \sum \text{EstimatedDemand})} \right)$
- **AgingScore**: $\min\left(1.0, \frac{\text{waiting\_time}}{\text{starvation\_threshold}}\right)$ (Default threshold = 10 ticks)

---

## 🏗 System Architecture

```
adaptive-banker/
├── backend/
│   ├── main.py                  # FastAPI REST API endpoints
│   ├── requirements.txt         # Dependencies (FastAPI, uvicorn, pydantic, pytest)
│   ├── algorithms/
│   │   ├── banker.py            # Classical Banker Safety Algorithm
│   │   ├── demand_estimator.py  # EWMA Demand Estimator
│   │   └── ranking.py           # Starvation-Aware Scoring & Ranking
│   ├── simulation/
│   │   ├── engine.py            # Discrete-event simulation engine
│   │   ├── process.py           # Process lifecycle model & state transitions
│   │   └── scenarios.py         # Built-in reproducible workload scenarios
│   ├── models/
│   │   └── state.py             # Pydantic data schemas & state models
│   ├── metrics/
│   │   └── metrics.py           # Metrics calculation & benchmarking
│   └── tests/
│       ├── test_banker.py       # Safety, validation & rejection tests
│       ├── test_estimator.py    # EWMA & safety margin tests
│       └── test_ranking.py      # Aging & candidate ranking tests
├── frontend/
│   ├── package.json
│   ├── src/
│   │   ├── components/          # React Dashboard components
│   │   ├── services/api.js      # REST API client
│   │   └── App.jsx
└── README.md
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- Node.js 18+ & npm

### 1. Launch Backend Server

```bash
cd backend
python -m uvicorn main:app --reload
```
The FastAPI backend will start at `http://localhost:8000`.

### 2. Launch Frontend Dashboard

In a separate terminal:
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` in your browser.

---

## 🧪 Running Unit Tests

Run the complete backend test suite using `pytest`:

```bash
cd backend
python -m pytest
```

---

## 📊 Scenarios & Demonstrations

1. **Starvation Demonstration (`STARVATION`)**: Shows a low-priority process requesting resources while higher-priority processes repeatedly submit requests. Under Classical Banker, the low-priority process starves. Under Adaptive Banker, aging elevates its score until it is safely granted.
2. **Normal Workload (`NORMAL`)**: Balanced resource requests across 5 processes.
3. **High Contention (`HIGH_CONTENTION`)**: Scarce resources forcing multiple safe/unsafe evaluations.
4. **Dynamic Demand (`DYNAMIC_DEMAND`)**: Shifting resource request sizes demonstrating real-time EWMA adaptation.

---

## 📝 Academic Verification & Key Findings

- **Zero Deadlocks / Zero Safety Violations**: Both algorithms maintain 0 safety violations under all workloads.
- **Fairness & Reduced Waiting Time**: Adaptive Banker prevents process starvation and significantly reduces maximum and average waiting times.
