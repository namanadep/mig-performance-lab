"""mig-lab CLI."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml


def main() -> None:
    p = argparse.ArgumentParser(prog="mig-lab")
    sub = p.add_subparsers(dest="cmd", required=True)

    st = sub.add_parser("status", help="Dump nvidia-smi -L as JSON")
    st.add_argument("--json-out", type=Path)

    dp = sub.add_parser("describe-profiles", help="Print mig_profiles.yaml")
    dp.add_argument("--config", type=Path, default=Path("configs/mig_profiles.yaml"))

    args = p.parse_args()

    if args.cmd == "describe-profiles":
        cfg_path = args.config
        if not cfg_path.is_file():
            print(f"Config not found: {cfg_path}", file=sys.stderr)
            sys.exit(1)
        data = yaml.safe_load(cfg_path.read_text()) or {}
        print(yaml.dump(data, default_flow_style=False))
        return

    if args.cmd == "status":
        from mig_lab.nvidia_mig import parse_smi_l_output, run_nvidia_smi_l

        try:
            text = run_nvidia_smi_l()
        except Exception as e:
            print(f"nvidia-smi failed: {e}", file=sys.stderr)
            sys.exit(2)
        gpus = parse_smi_l_output(text)
        out = [{"index": g.index, "name": g.name, "uuid": g.uuid} for g in gpus]
        payload = json.dumps({"gpus": out}, indent=2)
        if args.json_out:
            args.json_out.parent.mkdir(parents=True, exist_ok=True)
            args.json_out.write_text(payload)
            print(f"Wrote {args.json_out}")
        else:
            print(payload)


if __name__ == "__main__":
    main()
