"""Parse `nvidia-smi -L` / `nvidia-smi mig` style output (simplified)."""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass


@dataclass
class GpuLine:
    index: int
    name: str
    uuid: str


def parse_smi_l_output(text: str) -> list[GpuLine]:
    """Parse `nvidia-smi -L` output."""
    lines: list[GpuLine] = []
    for line in text.splitlines():
        # GPU 0: NVIDIA H200 (UUID: GPU-xxx)
        m = re.match(r"GPU (\d+): ([^(]+) \(UUID: ([^)]+)\)", line.strip())
        if m:
            lines.append(GpuLine(int(m.group(1)), m.group(2).strip(), m.group(3).strip()))
    return lines


def run_nvidia_smi_l() -> str:
    return subprocess.check_output(["nvidia-smi", "-L"], text=True, timeout=30)
