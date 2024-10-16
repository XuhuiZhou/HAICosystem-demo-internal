![TITLE](figs/title.png)
# HAICosystem-demo

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3109/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://pre-commit.com/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)


## Get started

This package supports Python 3.11 and above. We recommend using a virtual environment to install this package, e.g.,

```
conda create -n haicosystem-demo python=3.11; conda activate haicosystem-demo;  curl -sSL https://install.python-poetry.org | python3
poetry install
```


## Usage
```
streamlit run app.py
```


## Contribution
### Install dev options
```bash
mypy --install-types --non-interactive haicosystem-demo
pip install pre-commit
pre-commit install
```
### New branch for each feature
`git checkout -b feature/feature-name` and PR to `main` branch.
### Before committing
Run `pytest` to make sure all tests pass (this will ensure dynamic typing passed with beartype) and `mypy --strict --exclude haicosystem/tools  --exclude haicosystem/grounding_engine/llm_engine_legacy.py .` to check static typing.
(You can also run `pre-commit run --all-files` to run all checks)
### Check github action result
Check the github action result to make sure all tests pass. If not, fix the errors and push again.

## Leaderboard (Risk Ratio)

| Model Name | Publisher | Open? | Overall Risk Ratio | Targeted Safety Risks | System and Operational Risks | Content Safety Risks | Societal Risks | Legal and Rights Related Risks |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-4-turbo | OpenAI | No | 0.49 | 0.46 | 0.23 | 0.14 | 0.26 | 0.19 |
| GPT-3.5-turbo | OpenAI | No | 0.67 | 0.66 | 0.41 | 0.26 | 0.41 | 0.29 |
| Llama3.1-405B | Meta | Yes | 0.56 | 0.53 | 0.29 | 0.19 | 0.31 | 0.25 |
| Llama3.1-70B | Meta | Yes | 0.62 | 0.60 | 0.32 | 0.24 | 0.38 | 0.28 |
| Llama3.1-8B | Meta | Yes | 0.71 | 0.59 | 0.45 | 0.17 | 0.28 | 0.29 |
| Mixtral-8x22B | MistralAI | Yes | 0.59 | 0.56 | 0.30 | 0.19 | 0.33 | 0.25 |
| Qwen1.5-72B-Chat | Alibaba | Yes | 0.62 | 0.59 | 0.35 | 0.21 | 0.35 | 0.26 |
| Qwen2-72B-Instruct | Alibaba | Yes | 0.58 | 0.55 | 0.32 | 0.20 | 0.36 | 0.27 |
| Qwen1.5-110B-Chat | Alibaba | Yes | 0.56 | 0.52 | 0.30 | 0.17 | 0.28 | 0.22 |
| Llama3-70B | Meta | Yes | 0.65 | 0.63 | 0.40 | 0.19 | 0.36 | 0.30 |
| Llama3-8B | Meta | Yes | 0.70 | 0.61 | 0.50 | 0.16 | 0.27 | 0.28 |
| DeepSeek-67B | DeepSeek AI | Yes | 0.64 | 0.61 | 0.37 | 0.23 | 0.33 | 0.27 |


## Leaderboard (Scores)

| Model Name | Publisher | Open? | Overall Risk Ratio | Targeted Safety Risks | System and Operational Risks | Content Safety Risks | Societal Risks | Legal and Rights Related Risks |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-4-turbo | OpenAI | No | 0.49 | 0.46 | 0.23 | 0.14 | 0.26 | 0.19 |
| GPT-3.5-turbo | OpenAI | No | 0.67 | 0.66 | 0.41 | 0.26 | 0.41 | 0.29 |
| Llama3.1-405B | Meta | Yes | 0.56 | 0.53 | 0.29 | 0.19 | 0.31 | 0.25 |
| Llama3.1-70B | Meta | Yes | 0.62 | 0.60 | 0.32 | 0.24 | 0.38 | 0.28 |
