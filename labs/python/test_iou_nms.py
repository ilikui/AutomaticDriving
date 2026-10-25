"""Unit tests for the dependency-free IoU/NMS teaching example."""
import math
import unittest

from iou_nms import box_iou, greedy_nms


class BoxIoUTests(unittest.TestCase):
    def test_identical_boxes_have_iou_one(self):
        self.assertAlmostEqual(box_iou((0, 0, 2, 2), (0, 0, 2, 2)), 1.0)

    def test_disjoint_boxes_have_iou_zero(self):
        self.assertEqual(box_iou((0, 0, 1, 1), (2, 2, 3, 3)), 0.0)

    def test_partial_overlap(self):
        self.assertAlmostEqual(box_iou((0, 0, 2, 2), (1, 1, 3, 3)), 1 / 7)

    def test_zero_area_boxes(self):
        self.assertEqual(box_iou((1, 1, 1, 1), (1, 1, 1, 1)), 0.0)

    def test_invalid_box_raises(self):
        with self.assertRaises(ValueError):
            box_iou((0, 0, 2, 1), (0, 0, 1, 1))
        with self.assertRaises(ValueError):
            box_iou((0, 0, math.inf, 1), (0, 0, 1, 1))


class GreedyNMSTests(unittest.TestCase):
    def test_suppresses_overlapping_lower_score_box(self):
        detections = [
            ((0, 0, 10, 10), 0.9),
            ((1, 1, 9, 9), 0.8),
            ((20, 20, 30, 30), 0.7),
        ]
        self.assertEqual(greedy_nms(detections, 0.5), [0, 2])

    def test_equal_scores_keep_input_order(self):
        detections = [((0, 0, 10, 10), 0.5), ((0, 0, 10, 10), 0.5)]
        self.assertEqual(greedy_nms(detections, 0.5), [0])

    def test_threshold_boundary_is_not_suppressed(self):
        detections = [((0, 0, 2, 2), 0.9), ((1, 0, 3, 2), 0.8)]
        self.assertEqual(greedy_nms(detections, 1 / 3), [0, 1])

    def test_invalid_threshold_and_score_raise(self):
        with self.assertRaises(ValueError):
            greedy_nms([], float("nan"))
        with self.assertRaises(ValueError):
            greedy_nms([((0, 0, 1, 1), float("inf"))])

    def test_empty_input(self):
        self.assertEqual(greedy_nms([]), [])


if __name__ == "__main__":
    unittest.main()
