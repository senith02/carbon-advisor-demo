# carbon-advisor-demo

This is a demonstration repository for the **carbon-deferral advisor**, a GitHub Action from the BSc
study *An Empirical Decision Model for Selective Carbon-Aware Scheduling in CI/CD Pipelines Using
Commit-Level Software Engineering Characteristics*.

> **Demonstration — not research evidence.** Every result here comes from a small demo app and a
> **synthetic** build workload. The study's evidence is the trace-driven evaluation in
> [`senith02/Artifact`](https://github.com/senith02/Artifact).

## What you are looking at

Every push runs [`ci.yml`](.github/workflows/ci.yml), which has three jobs:

| job | what it shows |
| :-- | :-- |
| `advisor (real location, GitHub-hosted)` | The honest answer for this repository. GitHub-hosted runners are not known to be in Great Britain, so the job declares `GITHUB-HOSTED`, and the advisor answers **RUN NOW (fail-safe: region_not_gb)**. |
| `advisor (GB scenario)` | What the advisor *would* recommend if this build ran on GB compute. Every output is labelled **SCENARIO**. |
| `build` | Unit tests, then a **synthetic ~9-minute CPU workload** ([`scripts/synthetic_workload.py`](scripts/synthetic_workload.py)) standing in for a longer test suite. |

Open any run and look at each advisor job's **Summary** for the recommendation and the reason. The
full request, response and audit record are uploaded as a workflow artifact.

[`pr-target-probe.yml`](.github/workflows/pr-target-probe.yml) shows that a `pull_request_target`
trigger is refused (**RUN NOW, fail-safe: untrusted_event**).

## How the advisor decides

1. **Pull requests and protected branches** (`main`, release branches, …) always get **RUN NOW**.
2. **Other pushes:** the advisor estimates the run's duration from this workflow's **completed**
   runs. If the estimate is at least 480 s, it recommends the lowest-carbon hour within 24 h on the
   GB hour-of-week profile.
3. **Team vetoes**, set in [`.github/carbon-advisor.yml`](.github/carbon-advisor.yml), can only turn a
   deferral into RUN NOW:
   - the very first run, with no history (cold start);
   - an `[urgent]` marker in the commit message;
   - tags, manual and scheduled runs;
   - a maximum delay.

The study evaluated commit-level software-engineering characteristics and found no material decision
value beyond the duration estimate. The advisor therefore uses branch/PR status and a duration
estimate only.

## Statements that apply to every output

- Recommendation only: the advisor never pauses, cancels or fails a build.
- Carbon figures are estimates under a constant-power energy model, not measurements.
- Evaluated regime: Great Britain only. The compute location is declared by the team, not detected.
- Thresholds (480 s, 24 h) were fitted on Travis CI 2011-2016 and are extrapolated to GitHub Actions.
- GitHub Actions run wall-clock time is a different measure from Travis `tr_duration`.
- The urgency gate (pull request / protected branch) is an unvalidated approximation (DL-020).
- Manual and scheduled runs are vetoed by team policy, not detected as urgent.
- What-If output is demonstration only.

The advisor's documentation is in
[`Research_Artifact/code/github-action/README.md`](https://github.com/senith02/Artifact/tree/main/Research_Artifact/code/github-action).
