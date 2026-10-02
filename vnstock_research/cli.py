from __future__ import annotations

import argparse
import json
from .data import make_synthetic_bars
from .experiment import run_exp_001


def main():
    parser = argparse.ArgumentParser(description="VN stock research platform")
    sub = parser.add_subparsers(dest="command", required=True)
    exp = sub.add_parser("run-exp-001")
    exp.add_argument("--output", default="artifacts/exp-001")
    exp.add_argument("--method", choices=["kmeans", "hdbscan"], default="kmeans")
    exp.add_argument("--clusters", type=int, default=3)
    exp.add_argument("--window", type=int, default=20)
    args = parser.parse_args()
    if args.command == "run-exp-001":
        report = run_exp_001(make_synthetic_bars(), args.output, n_clusters=args.clusters, method=args.method, window=args.window)
        print(json.dumps(report, indent=2, default=str))


if __name__ == "__main__":
    main()

