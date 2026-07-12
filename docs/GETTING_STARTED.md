# Getting Started — DriftWatch Pro

## Prerequisites
- **Python 3.11+**
- **numpy** (the only dependency) — `pip install -r requirements.txt`
- **Docker** (optional) to run the HTTP service.

## Run it
```bash
git clone https://github.com/Kimosabey/driftwatch-pro.git
cd driftwatch-pro
pip install -r requirements.txt

python -m unittest discover -s tests   # 10 tests
python -m driftwatch.demo              # baseline vs. stable / shifted / variance batches
docker compose up                      # HTTP API on :8000
```

## Environment variables
| Key | Default | Description |
| :--- | :--- | :--- |
| `PORT` | `8000` | HTTP port for the API |

Detection thresholds are constructor arguments on `DriftMonitor(alpha=0.05, psi_threshold=0.2)` rather
than env vars.

## Running tests
```bash
python -m unittest discover -s tests   # stdlib test runner, no pytest needed
```
