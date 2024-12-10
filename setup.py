import shlex
import sys
from subprocess import check_call
from pathlib import Path

if __name__ == "__main__":
    suffix = sys.argv[1]
    paths = [
        Path(__file__).parent / f"day_{suffix}.py",
        Path(__file__).parent / "data" / f"input_{suffix}_small.txt",
        Path(__file__).parent / "data" / f"input_{suffix}_large.txt",
    ]
    if len(sys.argv) > 2:
        paths.append(
            Path(__file__).parent / "data" / f"input_{suffix}_small_2.txt",
        )
    byteses = [(Path(__file__).parent / "template.py").read_bytes(), bytes(), bytes()]

    for p, b in zip(paths, byteses):
        if p.exists():
            pass
        else:
            p.write_bytes(b)

    check_call(
        shlex.split(f"code-insiders -r {(' '.join(p.as_posix() for p in paths))}")
    )
