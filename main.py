import numpy as np
from scipy.stats import triang, truncnorm

# ---------------------------------
# Input parameters
# ---------------------------------
TYRE_WEIGHT = 10  # kg
POLY_PERCENT = 0.282
BASE_POLY_KG = TYRE_WEIGHT * POLY_PERCENT

SIMULATIONS = 1_000_000

# ---------------------------------
# Wastage: Truncated Normal
# ---------------------------------
MEAN_WASTE = 0.28
STD_WASTE = 0.05

a, b = (0 - MEAN_WASTE) / STD_WASTE, (1 - MEAN_WASTE) / STD_WASTE
wastage = truncnorm.rvs(a, b, loc=MEAN_WASTE, scale=STD_WASTE, size=SIMULATIONS)

# ---------------------------------
# Price: Triangular Distribution
# ---------------------------------
PRICE_MIN = 14500
PRICE_MODE = 17250
PRICE_MAX = 19112

c = (PRICE_MODE - PRICE_MIN) / (PRICE_MAX - PRICE_MIN)
price_per_100kg = triang.rvs(
    c, loc=PRICE_MIN, scale=PRICE_MAX - PRICE_MIN, size=SIMULATIONS
)

# ---------------------------------
# Cost calculation
# ---------------------------------
required_poly = BASE_POLY_KG * (1 + wastage)
price_per_kg = price_per_100kg / 100

cost_per_tyre = required_poly * price_per_kg

# ---------------------------------
# Budget provisioning
# ---------------------------------
budget_95 = np.percentile(cost_per_tyre, 95)
mean_cost = np.mean(cost_per_tyre)

print(f"Mean Cost per Tyre   : ₹{mean_cost:,.2f}")
print(f"95% Budget Provision : ₹{budget_95:,.2f}")
