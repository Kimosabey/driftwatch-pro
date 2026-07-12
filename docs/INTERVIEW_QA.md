# Interview Q&A — DriftWatch Pro

### "Tell me about this project."
DriftWatch Pro detects **data drift** — when production data drifts away from the training distribution and
a model starts to silently decay. It registers a per-feature baseline, then scores each live batch with two
statistical tests (KS and PSI) and grades severity, so drift becomes an explicit alert instead of a mystery
drop in accuracy.

### "What was the hardest / most interesting part?"
Telling **real drift from sampling noise**. I implemented the two-sample KS test on numpy (ECDF gap + an
asymptotic p-value) and PSI on quantile bins. The subtle bug I found in testing: PSI with 10 quantile bins
on a tiny batch reports huge fake divergence — so I made the **bin count adaptive** to sample size, which
fixed a stable batch that was false-flagging.

### "Why implement the stats yourself instead of scipy?"
To keep the dependency footprint to one library (numpy) and, honestly, because implementing KS and PSI by
hand shows I understand them rather than just calling `ks_2samp`. scipy is a drop-in alternative.

### "Why two detectors?"
KS catches a change in distribution *shape*; PSI is the drift metric MLOps teams already use and quantifies
*magnitude*. Drift trips if either fires, which reduces missed drift.

### "How is it tested?"
10 stdlib `unittest` tests with fixed seeds: KS on identical vs. shifted distributions, PSI near-zero on
identical / >0.25 on shifted, the small-sample regression, and severity grading. No pytest needed.

### "How does it fit your portfolio?"
It's my MLOps / data-science piece (real Python), under the "Antigravity" model — cheap, local, explainable
statistics (`#48`).
