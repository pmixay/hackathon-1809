"""Run every experiment in order (EXP-01 .. EXP-06). Deterministic; no random seeds involved."""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for script in ("run_alternatives.py", "run_stress_adaptation.py", "run_demand_sensitivity.py", "run_sensitivity.py", "run_extensibility.py", "run_reaction.py"):
    print(f"\n===== {script} =====")
    subprocess.run([sys.executable, str(HERE / script)], check=True, cwd=str(HERE))
