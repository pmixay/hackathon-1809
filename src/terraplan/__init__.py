"""TerraPlan — propellant supply planning circuit for an orbital fuel depot (2035–2040).

Calculation core for CosmoHackathon 2026, case 2 "Fuel Space Circuit 2035".
All formulas follow the organizer control rules (docs/organizer/reference_repo/docs_CALCULATION_RULES.md).
"""

__version__ = "0.1.0"

from .case import Case, CaseError, load_case  # noqa: F401
from .scenario import Scenario, ScenarioError, load_scenario  # noqa: F401
from .plan import Plan, PlanError, load_plan, save_plan  # noqa: F401
from .assumptions import Assumptions, load_assumptions  # noqa: F401
from .engine import Result, simulate  # noqa: F401
from .export import write_results  # noqa: F401
from .compare import compare_results  # noqa: F401
