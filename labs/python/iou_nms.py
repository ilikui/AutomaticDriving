"""Dependency-free 2D box IoU and greedy NMS.

Boxes use (x1, y1, x2, y2), with x2 >= x1 and y2 >= y1.
Educational offline example only; this is not a production detector component.
Run: python labs/python/iou_nms.py
"""
from __future__ import annotations

import math
from typing import Sequence

Box = tuple[float, float, float, float]
Detection = tuple[Box, float]


def _validate_box(box: Sequence[float]) -> Box:
    if len(box) != 4:
        raise ValueError("box must contain exactly four coordinates")
    values = tuple(float(v) for v in box)
    if not all(math.isfinite(v) for v in values):
        raise ValueError("box coordinates must be finite")
    x1, y1, x2, y2 = values
    if x2 < x1 or y2 < y1:
        raise ValueError("box maximum coordinates must not be smaller than minimum coordinates")
    return values  # type: ignore[return-value]


def box_iou(box_a: Sequence[float], box_b: Sequence[float]) -> float:
    """Calculate intersection-over-union for two axis-aligned boxes."""
    ax1, ay1, ax2, ay2 = _validate_box(box_a)
    bx1, by1, bx2, by2 = _validate_box(box_b)

    intersection_w = max(0.0, min(ax2, bx2) - max(ax1, bx1))
    intersection_h = max(0.0, min(ay2, by2) - max(ay1, by1))
    intersection = intersection_w * intersection_h
    area_a = (ax2 - ax1) * (ay2 - ay1)
    area_b = (bx2 - bx1) * (by2 - by1)
    union = area_a + area_b - intersection
    return intersection / union if union > 0.0 else 0.0


def greedy_nms(
    detections: Sequence[Detection],
    iou_threshold: float = 0.5,
) -> list[int]:
    """Return original detection indices kept by score-descending greedy NMS.

    Equal scores retain their input order. Coordinates are continuous (no +1 pixel
    convention). Class labels are not modeled: all detections suppress one another.
    """
    if not math.isfinite(iou_threshold) or not 0.0 <= iou_threshold <= 1.0:
        raise ValueError("iou_threshold must be finite and in [0, 1]")

    validated: list[tuple[Box, float, int]] = []
    for index, (box, score) in enumerate(detections):
        checked_box = _validate_box(box)
        score = float(score)
        if not math.isfinite(score):
            raise ValueError("detection scores must be finite")
        validated.append((checked_box, score, index))

    order = sorted(validated, key=lambda item: (-item[1], item[2]))
    kept: list[int] = []
    while order:
        best = order.pop(0)
        kept.append(best[2])
        order = [
            candidate
            for candidate in order
            if box_iou(best[0], candidate[0]) <= iou_threshold
        ]
    return kept


def main() -> None:
    boxes: list[Detection] = [
        ((10, 10, 50, 50), 0.95),
        ((12, 12, 48, 48), 0.80),
        ((60, 10, 90, 40), 0.75),
    ]
    print("IoU(box 0, box 1):", f"{box_iou(boxes[0][0], boxes[1][0]):.3f}")
    print("Kept detection indices:", greedy_nms(boxes, iou_threshold=0.5))


if __name__ == "__main__":
    main()
