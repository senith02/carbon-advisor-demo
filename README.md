# carbon-advisor-demo

This is a demonstration repository for the **carbon-deferral advisor**, a GitHub Action from the BSc
study *An Empirical Decision Model for Selective Carbon-Aware Scheduling in CI/CD Pipelines Using
Commit-Level Software Engineering Characteristics*.

> **Demonstration — not research evidence.** Every result here comes from a small demo app and a
> **synthetic** build workload. The study's evidence is the trace-driven evaluation in
> [`senith02/Artifact`](https://github.com/senith02/Artifact).

## What you are looking at

Every push runs [`ci.yml`](.github/workflows/ci.yml). It has **one advisory job**, with no config
file and no checkout, beside the build:

| job | what it shows |
| :-- | :-- |
| `carbon-advisor` | **The honest answer.** GitHub-hosted runners are not known to be in Great Britain, so the job declares `GITHUB-HOSTED`, and the advisor answers **RUN NOW (fail-safe: region_not_gb)**. **The GB scenario**, in the same Summary and labelled **SCENARIO**, shows what it *would* recommend if this build ran on GB compute. |
| `build` | Unit tests, then a **synthetic ~9-minute CPU workload** ([`scripts/synthetic_workload.py`](scripts/synthetic_workload.py)) standing in for a longer test suite. |

Each run shows a notice at the top of the run page; the advisor job's **Summary** gives the reason.
The full request, response and audit record are uploaded as a workflow artifact.

**The re-dispatch cycle, labelled SCENARIO.** This demo sets `redispatch: scenario-demo`, so the
whole cycle can be shown on a GitHub-hosted runner:
1. When the GB scenario says DEFER, the advisor opens an issue labelled **`carbon-deferral`**, titled
   **[SCENARIO]**, and the build is skipped.
2. At the recommended hour, a small service on the author's server
   ([`carbon_tick.py`](https://github.com/senith02/Artifact/tree/main/Research_Artifact/code/github-action/examples/vps-trigger))
   starts [`carbon-dispatch.yml`](.github/workflows/carbon-dispatch.yml). It re-dispatches `ci.yml` at
   the deferred commit, then comments on and closes the issue. GitHub's own schedule is too unreliable
   to be on time, so it is kept only as a 6-hourly backup.
3. The re-dispatched run is RUN NOW and builds that commit.

Close the issue to cancel a deferral. `scenario-demo` exists for demonstration repositories only; a
real team on GB compute would use `redispatch: true`.

[`pr-target-probe.yml`](.github/workflows/pr-target-probe.yml) shows that a `pull_request_target`
trigger is refused (**RUN NOW, fail-safe: untrusted_event**).

[`whatif.yml`](.github/workflows/whatif.yml) builds a **Repo What-If Report** from the same Action
(`mode: whatif`): it replays this repository's completed `ci.yml` runs through the advisor. Open the
**carbon-whatif** run and read its **Summary**, or download the artifact and open `report.html` in a
browser.

## Try it yourself

Fork this repository, enable workflows in the fork's **Actions** tab, then:

1. **Build history.** Push one commit to `main` and wait about 10 minutes for `ci` to finish
   (`git commit --allow-empty -m "Build history"` then `git push origin main`). The advisor only
   estimates from completed runs.
2. **RUN NOW:** push to `main`, open a pull request, or put `[urgent]` in a commit message.
3. **DEFER RECOMMENDED:** push to a new branch, for example
   `git checkout -b feature/try-defer`, `git commit --allow-empty -m "Try the advisor"`,
   `git push -u origin feature/try-defer`. The GB scenario section of the advisor's Summary shows
   DEFER RECOMMENDED with a start time, unless the current hour is already the cleanest in the next
   24 h. A **[SCENARIO] Carbon deferral** issue appears, and the build is skipped.
4. **Re-dispatch:** in a fork there is no server running `carbon_tick.py`, so after the recommended
   hour run **Actions** → **carbon-dispatch** → **Run workflow** yourself, or set up the trigger from
   the guide above. It re-runs the build and closes the issue.
5. **What-If report:** **Actions** → **carbon-whatif** → **Run workflow**.

The full walkthrough is the
[User Guide](https://github.com/senith02/Artifact/blob/main/Research_Artifact/USER_GUIDE.md).

## How the advisor decides

1. **Pull requests and protected branches** (`main`, release branches, …) always get **RUN NOW**.
2. **Other pushes:** the advisor estimates the run's duration from this workflow's **completed**
   runs. If the estimate is at least 480 s, it recommends the lowest-carbon hour within 24 h on the
   GB hour-of-week profile.
3. **Team vetoes**, set as inputs of the advisor step (or in an optional `.github/carbon-advisor.yml`),
   can only turn a deferral into RUN NOW:
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
