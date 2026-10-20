"""Dependency-free 1D constant-velocity Kalman filter demonstration.

Educational simulation only; not intended for vehicle deployment.
Run: python labs/python/kalman_1d.py
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Estimate:
    time_s: float
    truth_m: float
    measurement_m: float
    position_m: float
    velocity_mps: float
    position_error_m: float


class ConstantVelocityKalman:
    """State x=[position, velocity], covariance P is a 2x2 matrix."""

    def __init__(
        self,
        initial_position_m: float = 0.0,
        initial_velocity_mps: float = 0.0,
        position_variance: float = 10.0,
        velocity_variance: float = 10.0,
        measurement_variance: float = 1.0,
        acceleration_noise_variance: float = 0.2,
    ) -> None:
        if position_variance <= 0 or velocity_variance <= 0:
            raise ValueError("initial variances must be positive")
        if measurement_variance <= 0 or acceleration_noise_variance < 0:
            raise ValueError("measurement variance must be positive and process noise non-negative")
        self.x = [float(initial_position_m), float(initial_velocity_mps)]
        self.p = [[float(position_variance), 0.0], [0.0, float(velocity_variance)]]
        self.r = float(measurement_variance)
        self.q = float(acceleration_noise_variance)

    def predict(self, dt_s: float) -> Tuple[float, float]:
        if not math.isfinite(dt_s) or dt_s <= 0:
            raise ValueError("dt_s must be finite and greater than zero")

        dt = dt_s
        position, velocity = self.x
        self.x = [position + dt * velocity, velocity]

        p00, p01 = self.p[0]
        p10, p11 = self.p[1]
        # F P F^T, where F=[[1, dt], [0, 1]].
        fpf = [
            [p00 + dt * (p01 + p10) + dt * dt * p11, p01 + dt * p11],
            [p10 + dt * p11, p11],
        ]
        # White-acceleration process noise: q * [[dt^4/4, dt^3/2],
        # [dt^3/2, dt^2]].
        q = self.q
        self.p = [
            [fpf[0][0] + q * dt**4 / 4.0, fpf[0][1] + q * dt**3 / 2.0],
            [fpf[1][0] + q * dt**3 / 2.0, fpf[1][1] + q * dt**2],
        ]
        return self.x[0], self.x[1]

    def update(self, measured_position_m: float) -> Tuple[float, float]:
        if not math.isfinite(measured_position_m):
            raise ValueError("measurement must be finite")
        # Measurement model z=H x + noise, H=[1, 0].
        innovation = measured_position_m - self.x[0]
        innovation_variance = self.p[0][0] + self.r
        k0 = self.p[0][0] / innovation_variance
        k1 = self.p[1][0] / innovation_variance

        self.x[0] += k0 * innovation
        self.x[1] += k1 * innovation

        # Joseph covariance update is more numerically robust than (I-KH)P.
        p00, p01 = self.p[0]
        p10, p11 = self.p[1]
        a00, a01 = 1.0 - k0, 0.0
        a10, a11 = -k1, 1.0
        ap00 = a00 * p00 + a01 * p10
        ap01 = a00 * p01 + a01 * p11
        ap10 = a10 * p00 + a11 * p10
        ap11 = a10 * p01 + a11 * p11
        self.p = [
            [ap00 * a00 + ap01 * a01 + self.r * k0 * k0,
             ap00 * a10 + ap01 * a11 + self.r * k0 * k1],
            [ap10 * a00 + ap11 * a01 + self.r * k1 * k0,
             ap10 * a10 + ap11 * a11 + self.r * k1 * k1],
        ]
        # Remove tiny asymmetry from floating-point roundoff.
        off_diagonal = (self.p[0][1] + self.p[1][0]) / 2.0
        self.p[0][1] = off_diagonal
        self.p[1][0] = off_diagonal
        return self.x[0], self.x[1]


def run_demo(seed: int = 7, steps: int = 20, dt_s: float = 0.5) -> List[Estimate]:
    if steps < 1:
        raise ValueError("steps must be at least one")
    rng = random.Random(seed)
    true_velocity_mps = 3.0
    filter_ = ConstantVelocityKalman(
        initial_position_m=0.0,
        initial_velocity_mps=0.0,
        measurement_variance=1.0,
        acceleration_noise_variance=0.15,
    )
    results: List[Estimate] = []
    for step in range(1, steps + 1):
        time_s = step * dt_s
        truth = true_velocity_mps * time_s
        measurement = truth + rng.gauss(0.0, 1.0)
        filter_.predict(dt_s)
        position, velocity = filter_.update(measurement)
        results.append(
            Estimate(time_s, truth, measurement, position, velocity, position - truth)
        )
    return results


def main() -> None:
    rows = run_demo()
    print("t(s)  truth(m)  measured(m)  estimated(m)  velocity(m/s)  error(m)")
    for row in rows:
        print(
            f"{row.time_s:4.1f}  {row.truth_m:8.3f}  {row.measurement_m:11.3f}"
            f"  {row.position_m:12.3f}  {row.velocity_mps:13.3f}"
            f"  {row.position_error_m:8.3f}"
        )
    mean_abs_error = sum(abs(row.position_error_m) for row in rows) / len(rows)
    print(f"Mean absolute position error: {mean_abs_error:.3f} m")


if __name__ == "__main__":
    main()
