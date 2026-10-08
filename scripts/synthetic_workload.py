"""SYNTHETIC workload — stands in for a longer test suite (research DL-036 §3).

It keeps one CPU core busy finding primes for a fixed number of seconds, so
that this demo workflow's completed runs take long enough (about 9 minutes)
for the advisor's duration estimate to reach the 480 s threshold. Any
DEFER RECOMMENDED this repository shows follows from this chosen length: it
is a demonstration, never evidence about real projects.
"""

from __future__ import annotations

import argparse
import time

from demo_app import is_prime


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=int, default=540)
    args = parser.parse_args()
    deadline = time.monotonic() + args.seconds
    n = found = 0
    while time.monotonic() < deadline:
        for _ in range(10_000):
            n += 1
            found += is_prime(n)
    print(f"synthetic workload: {args.seconds} s, checked {n:,} integers, found {found:,} primes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
