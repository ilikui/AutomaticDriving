"""Timestamp gate and correlated-noise fusion for two scalar measurements.

The timestamp gate rejects stale/misaligned observations; it does not interpolate
or compensate motion. Correlated fusion uses a supplied covariance estimate.
"""
from __future__ import annotations

import math
from typing import List, Tuple

TimedMeasurement = Tuple[float, float, float]  # (value, variance, timestamp_s)


def require_time_alignment(
    measurements: List[TimedMeasurement], max_skew_s: float
) -> List[Tuple[float, float]]:
    """Validate timestamps and return (value, variance) pairs within max skew."""
    if not measurements:
        raise ValueError("at least one measurement is required")
    if not math.isfinite(max_skew_s) or max_skew_s < 0:
        raise ValueError("max_skew_s must be finite and non-negative")
    for value, variance, timestamp in measurements:
        if not all(math.isfinite(v) for v in (value, variance, timestamp)):
            raise ValueError("measurement values, variances and timestamps must be finite")
        if variance <= 0:
            raise ValueError("measurement variances must be positive")
    timestamps = [item[2] for item in measurements]
    if max(timestamps) - min(timestamps) > max_skew_s:
        raise ValueError("measurement timestamps exceed allowed skew")
    return [(value, variance) for value, variance, _ in measurements]


def fuse_correlated_pair(
    value_a: float,
    variance_a: float,
    value_b: float,
    variance_b: float,
    covariance_ab: float,
) -> Tuple[float, float]:
    """Best linear unbiased estimate for two measurements with known covariance."""
    values = (value_a, variance_a, value_b, variance_b, covariance_ab)
    if not all(math.isfinite(v) for v in values):
        raise ValueError("all inputs must be finite")
    if variance_a <= 0 or variance_b <= 0:
        raise ValueError("variances must be positive")
    if abs(covariance_ab) > math.sqrt(variance_a * variance_b):
        raise ValueError("covariance violates positive-semidefinite constraint")
    denominator = variance_a + variance_b - 2.0 * covariance_ab
    if denominator <= 1e-12:
        raise ValueError("measurements provide no independent information")
    weight_a = (variance_b - covariance_ab) / denominator
    weight_b = (variance_a - covariance_ab) / denominator
    estimate = weight_a * value_a + weight_b * value_b
    fused_variance = (variance_a * variance_b - covariance_ab**2) / denominator
    return estimate, fused_variance


def main() -> None:
    samples = [(10.2, 1.0, 100.000), (10.0, 0.64, 100.015)]
    aligned = require_time_alignment(samples, max_skew_s=0.03)
    estimate, variance = fuse_correlated_pair(
        aligned[0][0], aligned[0][1], aligned[1][0], aligned[1][1],
        covariance_ab=0.3,
    )
    print("Time-alignment and correlated-noise demo")
    print(f"timestamp skew: {max(s[2] for s in samples) - min(s[2] for s in samples):.3f} s")
    print(f"fused estimate: {estimate:.3f} m")
    print(f"fused variance: {variance:.4f} m^2")
    print("The example assumes the covariance is known and both observations refer to the same target/state.")


if __name__ == "__main__":
    main()
