# Failure Scenarios — DriftWatch Pro

The interesting failures here are statistical, not crashes — a drift detector that cries wolf (or stays
silent) is worse than one that's down.

## Fault Analysis
- **Tiny live batch.** Few samples make PSI wildly overstate divergence. Mitigated by **adaptive binning**
  (`bins` scales with `n//5`), so a 10-sample batch uses ~2 bins instead of 10. Regression-tested against a
  stable small batch that previously false-flagged.
- **Empty baseline or empty batch.** `ks_2samp` / `psi` raise `ValueError`; the API returns `400` instead of
  producing a meaningless score.
- **Check against an unregistered feature.** `DriftMonitor.check` raises `KeyError`; the API returns `404`.
- **One test trips, the other doesn't.** By design drift = KS `p<alpha` **OR** PSI `>threshold`, so a
  shape change KS catches isn't masked by a modest PSI (and vice-versa).
- **Threshold mis-set.** Too-tight `alpha`/`psi_threshold` floods alerts; too-loose hides drift. Both are
  explicit constructor args and covered by tests at known-stable and known-shifted distributions.

## Recovery Strategy
- Stateless per request; baselines live in memory and are re-registerable. A restart loses baselines only —
  re-`POST /baseline` to restore. (Persisting baselines is a listed future enhancement.)

## Verification
- 10 tests: KS on same vs. shifted distributions, PSI near-zero on identical / high on shifted, the
  small-sample regression, and monitor severity grading (`none` / `moderate` / `high`).
