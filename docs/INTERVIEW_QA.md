# Interview Q&A — DriftWatch Pro

### "Tell me about this project."
DriftWatch Pro is statistical data-drift detection using KS-tests against a training baseline. DriftWatch Pro compares live feature distributions against the training distribution with statistical tests (KS) and alerts when drift crosses a threshold, so model decay is caught early.

### "What was the hardest part?"
Distinguishing real drift from noise — choosing tests and thresholds that alert on signal, not variance.

### "Why did you choose this stack?"
- **Python** — ai & data-processing services.
- **SciPy** — statistical computing.

### "How does it fit the rest of your portfolio?"
It follows my "Antigravity" model — local logic/state/UI, cloud reasoning where it earns its cost — and shares the documentation and deployment conventions used across all my projects (#48).
