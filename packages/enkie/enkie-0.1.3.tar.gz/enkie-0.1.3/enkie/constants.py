import math
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

from .commons import Q

# Physical and mathematical constants.
R = Q(8.31446261815324e-3, "kJ / mol / K")
"""The gas constant."""
F = Q(96.48533212, "kC / mol")
"""The Faraday constant."""
LOG10 = math.log(10)
"""The natural logarithm of 10."""

# Default parameters.
DEFAULT_I = Q(0.2, "M")
"""Default ionic strength of a compartment."""
DEFAULT_PH = Q(7.0)
"""Default pH of a compartment."""
DEFAULT_PMG = Q(3.0)
"""Default pMg of a compartment."""
DEFAULT_PHI = Q(0, "V")
"""Default electrostatic potential of a compartment."""
DEFAULT_T = Q(298.15, "K")
"""Default temperature of the system."""

# Default numerical settings.
DEFAULT_RMSE = Q(3000, "kJ/mol")
"""Default uncertainty to use for unknown compounds and chemical groups."""

DEFAULT_SPONTANEOUS_GENES = {"s0001", "SPONTANEOUS"}
"""Default list of genes that denote spontaneous reactions."""
