#!/usr/bin/env python3

# Copyright 2024 (author: lamnt45)


# technical
import typing as tp
import subprocess


### FUNCTIONS
def mini_bash(
    cmd: str,
    executable: str = "/bin/bash",
    shell: bool = True,
    capture_output: bool = True,
    text: bool = True,
) -> tp.Tuple[str]:
    cmd = "set -Eeuo pipefail\n" + cmd
    Result = subprocess.run(
        cmd,
        executable=executable,
        shell=shell,
        capture_output=capture_output,
        text=text,
    )
    if Result.returncode != 0:
        raise RuntimeError(
            "> cant execute:\n" + cmd[:1000] + "\n" + "> stderr:\n" + Result.stderr
        )
    return Result.stdout, Result.stderr
