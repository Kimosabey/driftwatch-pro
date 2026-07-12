# Architecture — DriftWatch Pro

## High-Level Design (HLD)
DriftWatch Pro compares live feature distributions against the training distribution with statistical tests (KS) and alerts when drift crosses a threshold, so model decay is caught early.

```mermaid
%%{init: {'theme':'base','themeVariables':{'primaryColor':'#ffffff','lineColor':'#2563eb','mainBkg':'#ffffff'}}}%%
graph LR
    A([Live Distribution])
    B([vs. Training Distribution])
    C([KS-Test])
    D([Drift Alert])
    A --> B
    B --> C
    C --> D
    style A fill:#eff6ff,stroke:#2563eb,stroke-width:2px,color:#1e40af
    style B fill:#eff6ff,stroke:#2563eb,stroke-width:2px,color:#1e40af
    style C fill:#eff6ff,stroke:#2563eb,stroke-width:2px,color:#1e40af
    style D fill:#eff6ff,stroke:#2563eb,stroke-width:2px,color:#1e40af
```

**Flow:** Live Distribution → vs. Training Distribution → KS-Test → Drift Alert

## Low-Level Design (LLD)
- **Components:** `Python`, `SciPy`
- **Interfaces / contracts:** to be finalized during implementation.
- **Data model:** to be defined per component.

## Decision Log
- **Why this stack:** **Python** — ai & data-processing services; **SciPy** — statistical computing.
- **Antigravity constraint:** run logic/state/UI locally; offload heavy reasoning to cloud APIs; target modest hardware.

## Concept Deep Dive
Distinguishing real drift from noise — choosing tests and thresholds that alert on signal, not variance.
