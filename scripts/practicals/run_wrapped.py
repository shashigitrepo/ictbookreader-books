"""
Runs one practical like a terminal session: keyboard input comes from PRACTICAL_INPUTS and is
echoed after the prompt (as it appears on screen); matplotlib figures are saved as
figure-N.png instead of opening a window.
"""
import builtins
import json
import os
import runpy
import sys

inputs = list(json.loads(os.environ.get("PRACTICAL_INPUTS", "[]")))


def fake_input(prompt=""):
    if not inputs:
        raise EOFError("the program asked for more input than was given")
    value = inputs.pop(0)
    sys.stdout.write(f"{prompt}{value}\n")
    return value


builtins.input = fake_input

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    count = [0]

    def save_show(*args, **kwargs):
        for num in plt.get_fignums():
            count[0] += 1
            plt.figure(num).savefig(f"figure-{count[0]}.png", dpi=110, bbox_inches="tight")
        plt.close("all")

    plt.show = save_show
except ImportError:
    pass

sys.argv = [sys.argv[1]]
runpy.run_path(sys.argv[0], run_name="__main__")
if inputs:
    sys.stderr.write(f"[build error: {len(inputs)} input value(s) were not used]\n")
    sys.exit(3)
