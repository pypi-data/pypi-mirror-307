[![Python Versions](https://img.shields.io/pypi/pyversions/numpy?logo=python&logoColor=white)](https://pypi.org/project/pyqlib/#files)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20windows%20%7C%20macos-lightgrey)](https://pypi.org/project/pyqlib/#files)
[![PypI Versions](https://img.shields.io/pypi/v/frozen)](https://pypi.org/project/pyqlib/#history)
[![Github Commit Status](https://img.shields.io/github/commit-activity/w/Mxyzptlk-Z/frozen?logo=github)](https://github.com/Mxyzptlk-Z/frozen/commits?author=Mxyzptlk-Z)
[![Documentation Status](https://img.shields.io/readthedocs/frozen)](https://qlib.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/pypi/l/frozen)](LICENSE)

## 📰 **What's NEW!** &nbsp;   ✨

Recent released features

| Feature                                   | Status                                                                                                                                                                                                                    |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Data ETL pipeline                         | 🔨[Released](https://github.com/microsoft/qlib/pull/343) on Nov 3, 2024                                                                                                                                                      |
| Parameter tuning by optuna                | 🔨[Released](https://github.com/microsoft/qlib/pull/744) on Oct 23, 2024                                                                                                                                                    |
| Release Frozen v3.0.0                     | 📈[Released](https://github.com/microsoft/qlib/pull/704) on Sep 15, 2024                                                                                                                                                     |
| Integrate Qlib machine learning extension | 📈[Released](https://github.com/microsoft/qlib/pull/689) on Aug 20, 2024                                                                                                                                                     |
| ETF backtest engine                      | 📈[Released](https://github.com/microsoft/qlib/pull/668) on Jul 21, 2024                                                                                                                                                    |
| Factor database                           | 🔨[Released](https://github.com/microsoft/qlib/pull/438) on Jun 29, 2024                                                                                                                                                    |
| Release Frozen v2.6.0                     | 📈[Released](https://github.com/microsoft/qlib/pull/531) on Jun 13, 2024                                                                                                                                                     |
| DuckDB support for data module            | 📈[Released](https://github.com/microsoft/qlib/pull/508) on May 14, 2024                                                                                                                                                    |
| 3D-GPlearn factor mining extension        | :octocat: [Released](https://github.com/microsoft/qlib/releases/tag/v0.7.0) on Apr 7, 2024 |
| Integrate Qlib factor expression engine   | 📈[Released](https://github.com/microsoft/qlib/pull/491) on Feb 25, 2024                                                                                                                                                    |
| Factor expression engine                  | 🔨[Released](https://github.com/microsoft/qlib/pull/290) on Feb 17, 2024                                                                                                                                                    |
| Parallel computation example              | 🔨[Released](https://github.com/microsoft/qlib/pull/227) on Jan 14, 2024                                                                                                                                                    |
| Release Frozen v2.0.0                     | 📈[Released](https://github.com/microsoft/qlib/pull/221) on Dec 18, 2023                                                                                                                                                     |
| Release Frozen v1.0.0                    | 📈[Released](https://github.com/Mxyzptlk-Z/frozen/releases/tag/v1.0.0-alpha) on Apr 24 2023                                                                                                                                |

Frozen is an advanced factor-driven quantitative research platform, powered by a sophisticated event-driven backtesting engine and cutting-edge portfolio optimization engine. The framework aims to seamlessly integrate data processing, research analytics, back-testing, and live-trading into a unified pipeline, while standardizing factor research procedures through a systematic and rigorous approach.

The framework covers the entire chain of quantitative investment: alpha seeking, risk modeling, portfolio optimization, and order execution, enabling researchers and practitioners to efficiently transform their investment hypotheses into implementable strategies. With Frozen's robust architecture and intuitive interface, users can rapidly prototype, validate, and deploy sophisticated quantitative investment strategies with institutional-grade reliability.
For more details, please refer to project website

<table>
  <tbody>
    <tr>
      <th>Frameworks, Tutorial, Data & DevOps</th>
      <th>Solutions in Auto Quant Research</th>
    </tr>
      <td>
        <li><a href="#plans"><strong>Plans</strong></a></li>
        <li><a href="#framework-of-frozen">Framework of Frozen</a></li>
        <li><a href="#quick-start">Quick Start</a></li>
          <ul dir="auto">
            <li type="circle"><a href="#installation">Installation</a> </li>
            <li type="circle"><a href="#data-preparation">Data Preparation</a></li>
            <li type="circle"><a href="#factor-research-workflow"><strong>Factor Research Workflow<strong></a></li>
              <ul dir="auto">
                <li type="circle"><a href="#paper-reproduction">Paper Reproduction</a> </li>
                <li type="circle"><a href="#factor-mining">Factor Mining</a></li></ul>
            <li type="circle"><a href="#investment-strategy">Investment Strategy</a></li>
              <ul dir="auto">
                <li type="circle"><a href="#portfolio-optimization">Portfolio Optimization</a> </li>
                <li type="circle"><a href="#parameter-tuning">Paramemter Tuning</a></li></ul>
          </ul>
        <li><a href="#learning-framework">Learning Framework</a></li>
        <li><a href="#related-reports">Related Reports</a></li>
      </td>
      <td valign="baseline">
        <li><a href="#auto-quant-research-workflow">Auto Quant Research Workflow</a>
          <ul dir="auto">
            <li type="circle"><a href="#data-etl-pipeline">Data ETL Pipeline</a></li>
              <ul dir="auto">
                <li type="circle"><a href="#workflow-orchestration">Workflow Orchestration</a> </li>
                <li type="circle"><a href="#scheduled-run">Scheduled Run</a></li></ul>
            <li type="circle"><a href="#automatic-signal-generation">Automatic Signal Generation</a></li>
            <li type="circle"><a href="#live-trading--order-execution-algorithms">Live Trading & Order Execution Algorithms</a></li>
          </ul>
        </li>
        <li><a href="#interactive-visualization-tools">Interactive Visualization Tools</a>
          <ul dir="auto">
            <li type="circle"><a href="#real-time-monitor-panel">Real-Time Monitor Panel</a></li>
            <li type="circle"><a href="#web-ui-design">Web UI Design</a></li>
            <li type="circle"><a href="#mobile-app">Mobile App</a></li>
          </ul>
        </li>
      </td>
    </tr>
  </tbody>
</table>

# Plans

New features under development (order by estimated release time).

<!-- | Feature                        | Status      | -->

<!-- | --                      | ------    | -->


# Framework of Frozen

# Quick Start

This quick start guide tries to demonstrate

1. It's very easy to build a complete Quant research workflow and try your ideas with _Frozen_.
2. Though with *public data* and *simple models*, traditional factors **work very well** in practical Quant investment.

Here is a quick **[demo](https://terminalizer.com/view/3f24561a4470)** shows how to install ``Frozen``, and run Alpha101 strategy with ``frun``. **But**, please make sure you have already prepared the data following the [instruction](#data-preparation).

## Installation

This table demonstrates the supported Python version of `Frozen`:

|             | install with pip | install from source | Data ETL |
| ----------- | :--------------: | :-----------------: | :------: |
| Python 3.9  |       ✔️       |        ✔️        |    ❌    |
| Python 3.10 |       ✔️       |        ✔️        |   ✔️   |
| Python 3.11 |       ✔️       |        ✔️        |   ✔️   |

**Note**:

1. **Conda** is suggested for managing your Python environment. In some cases, using Python outside of a `conda` environment may result in missing header files, causing the installation failure of certain packages.
2. Python introduced match-case expression in version 3.10, which is incorporated in data ETL pipeline. Thus, for python 3.9, users will have to roll back manually to if-else expression.

### Install with pip

Users can easily install ``Qlib`` by pip according to the following command.

```bash
  pip install frozen
```

**Note**: pip will install the latest stable frozen. However, the main branch of frozen is in active development. If you want to test the latest scripts or functions in the main branch. Please install frozen with the methods below.

### Install from source

Also, users can install the latest dev version ``Frozen`` by the source code according to the following steps:

* It is recommended that users create a seperate environment for better management

  ```shell
  # if you prefer to use virtual environment, uncomment the following
  # python -m venv .venv
  # source .venv/bin/activate

  # if you prefer to use conda environment, run below
  conda create -n frozen python=3.11
  ```
* Before installing ``Frozen`` from source, users need to install some dependencies:

  ```bash
  pip install numpy
  pip install --upgrade  cython
  ```
* Download the repository and install ``Frozen`` as follows.

  ```bash
  pip install .  # `pip install -e .[dev]` is recommended for development.
  ```

  **Note**:  You can install Frozen with `python setup.py install` as well. But it is not the recommended approach. It will skip `pip` and cause obscure problems. For example, **only** the command ``pip install .`` **can** overwrite the stable version installed by ``pip install pyfrozen``, while the command ``python setup.py install`` **can't**.

## Data Preparation

## Factor Research Workflow

### Paper reproduction

### Factor Mining

## Investment Strategy

### Portfolio Optimization

### Parameter Tuning

# Auto Quant Research Workflow

## Data ETL Pipeline

### Workflow Orchestration

Frozen arrange workflow with Prefect

### Scheduled Run

with cron

## Automatic Signal Generation

## Live Trading & Order Execution Algorithms

# Interactive Visualization Tools

## Real-Time Monitor Panel

with Grafana

## Web UI Design

with Streamlit

## Mobile App Design

with Flutter

```bash
# if you want to conduct ETL task flow orchestration
prefect config set PREFECT_API_URL="http://127.0.0.1:4200/api"
prefect server start
```
