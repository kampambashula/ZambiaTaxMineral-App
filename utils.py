import numpy as np
from scipy.ndimage import gaussian_filter1d

# PAYE Functions
def effective_rate_paye(income):
    # Example piecewise PAYE
    if income <= 61_200:
        return 0
    elif income <= 85_200:
        return 0.1
    elif income <= 110_400:
        return 0.15
    elif income <= 248_000:
        return 0.25
    else:
        return 0.3

def calculate_marginal_point(income, effective_rate, threshold_income=110_400):
    mask = income > threshold_income
    income_filtered = income[mask]
    rate_filtered = effective_rate[mask]
    derivative = np.gradient(rate_filtered, income_filtered)

    max_slope_idx = np.argmax(derivative)
    for i in range(max_slope_idx, len(derivative)-1):
        if derivative[i+1] < derivative[i]:
            marginal_idx = i
            break

    return income_filtered[marginal_idx], rate_filtered[marginal_idx]

# Mineral Royalty Functions
def smooth_revenue(revenue_noisy, sigma=5):
    return gaussian_filter1d(revenue_noisy, sigma=sigma)
