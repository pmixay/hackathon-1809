"""Запуск всех экспериментов по порядку (EXP-01 … EXP-13). EXP-10 использует фиксированный seed."""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for script in ("run_alternatives.py", "run_stress_adaptation.py", "run_demand_sensitivity.py", "run_sensitivity.py", "run_extensibility.py", "run_reaction.py", "run_reverse_stress.py", "run_protection_measures.py", "run_earth_new_delay.py", "run_monte_carlo.py", "run_geopolitical_price_shock.py", "run_p2z_resilience.py", "run_earth_new_delay_measures.py"):
    print(f"\n===== {script} =====")
    subprocess.run([sys.executable, str(HERE / script)], check=True, cwd=str(HERE))
