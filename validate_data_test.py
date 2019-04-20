import sys
from io import StringIO
from unittest import TestCase, main

from validate_data import validate_data


class ValidateDataTest(TestCase):
    captured_output = StringIO()

    def setUp(self):
        self.captured_output = StringIO()
        sys.stdout = self.captured_output

    def assertOutputEqual(self, expected: str, endline="\n"):
        sys.stdout = sys.__stdout__
        self.assertEqual(expected + endline, self.captured_output.getvalue())

    def test_good_data(self):
        """Succeeds for valid data."""
        self.assertEqual(
            validate_data(
                1,
                [3001, 4001, 5001],
                [(5003, 3, 5), (9003, 3, 9), (1303, 3, 13)],
                [10, 60, 40],
            ),
            True,
        )

    def test_router_id_low(self):
        """Error: router id is too low"""
        self.assertEqual(
            validate_data(
                (0),
                [3001, 4001, 5001],
                [(5003, 3, 5), (9003, 3, 9), (1303, 3, 13)],
                [10, 60, 40],
            ),
            False,
        )
        self.assertOutputEqual("Router ID Configuration Error")

    def test_router_id_high(self):
        """Error: router id is too high"""
        self.assertEqual(
            validate_data(
                (64001),
                [3001, 4001, 5001],
                [(5003, 3, 5), (9003, 3, 9), (1303, 3, 13)],
                [10, 60, 40],
            ),
            False,
        )
        self.assertOutputEqual("Router ID Configuration Error")

    def test_input_ports_low(self):
        """Error: input port number is too low"""
        self.assertEqual(
            validate_data(
                (1),
                [1023, 4001, 5001],
                [(5003, 3, 5), (9003, 3, 9), (1303, 3, 13)],
                [10, 60, 40],
            ),
            False,
        )
        self.assertOutputEqual("Input Ports Configuration Error")

    def test_input_ports_high(self):
        """Error: input ports number is too high"""
        self.assertEqual(
            validate_data(
                (1),
                [3001, 4001, 64001],
                [(5003, 3, 5), (9003, 3, 9), (1303, 3, 13)],
                [10, 60, 40],
            ),
            False,
        )
        self.assertOutputEqual("Input Ports Configuration Error")

    def test_input_ports_reuse(self):
        """Error: input port reused."""
        self.assertEqual(
            validate_data(
                (1),
                [3001, 4001, 3001],
                [(5003, 3, 5), (9003, 3, 9), (1303, 3, 13)],
                [10, 60, 40],
            ),
            False,
        )
        self.assertOutputEqual("Input Ports Configuration Error")

    def test_output_ports_range_low(self):
        """Error: output port too low."""
        self.assertEqual(
            validate_data(
                1,
                [3001, 4001, 5001],
                [(1022, 3, 5), (9003, 3, 9), (1303, 3, 13)],
                [10, 60, 40],
            ),
            False,
        )
        self.assertOutputEqual(
            "Output Ports Configuration Error: Port out of range"
        )

    def test_output_ports_range_high(self):
        """Error: output port too high."""
        self.assertEqual(
            validate_data(
                1,
                [3001, 4001, 5001],
                [(5003, 3, 5), (64001, 3, 9), (1303, 3, 13)],
                [10, 60, 40],
            ),
            False,
        )
        self.assertOutputEqual(
            "Output Ports Configuration Error: Port out of range"
        )

    def test_output_ports_reuse(self):
        """Error: output ports reused"""
        self.assertEqual(
            validate_data(
                1,
                [3001, 4001, 5001],
                [(5003, 3, 5), (1303, 3, 9), (1303, 3, 13)],
                [10, 60, 40],
            ),
            False,
        )
        self.assertOutputEqual(
            "Output Ports Configuration Error: Port number re-use"
        )

    def test_output_ports_reuse_input(self):
        """Error: output port reused in the input ports"""
        self.assertEqual(
            validate_data(
                1,
                [3001, 4001, 5001],
                [(5003, 3, 5), (9003, 3, 9), (3001, 3, 13)],
                [10, 60, 40],
            ),
            False,
        )
        self.assertOutputEqual(
            "Output Ports Configuration Error: Port number re-use"
        )

    def test_output_cost_low(self):
        """Error: cost too low"""
        self.assertEqual(
            validate_data(
                1,
                [3001, 4001, 5001],
                [(5003, 0, 5), (9003, 15, 9), (1303, 3, 13)],
                [10, 60, 40],
            ),
            False,
        )
        self.assertOutputEqual(
            "Output Ports Configuration Error: Cost / Metric"
        )

    def test_output_cost_infinity(self):
        """Valid input: Cost is infinity"""
        self.assertEqual(
            validate_data(
                1,
                [3001, 4001, 5001],
                [(5003, 1, 5), (9003, 16, 9), (1303, 3, 13)],
                [10, 60, 40],
            ),
            True,
        )

    def test_output_cost_high(self):
        """Error: cost too high"""
        self.assertEqual(
            validate_data(
                1,
                [3001, 4001, 5001],
                [(5003, 1, 5), (9003, 17, 9), (1303, 3, 13)],
                [10, 60, 40],
            ),
            False,
        )
        self.assertOutputEqual(
            "Output Ports Configuration Error: Cost / Metric"
        )

    def test_output_cost_valid(self):
        """Valid input: different costs"""
        self.assertEqual(
            validate_data(
                1,
                [3001, 4001, 5001],
                [(5003, 1, 5), (9003, 15, 9), (1303, 3, 13)],
                [10, 60, 40],
            ),
            True,
        )

    def test_output_id_low(self):
        """Error: router id is too low"""
        self.assertEqual(
            validate_data(
                1,
                [3001, 4001, 5001],
                [(5003, 3, 0), (9003, 3, 9), (1303, 3, 13)],
                [10, 60, 40],
            ),
            False,
        )
        self.assertOutputEqual("Output Ports Configuration Error: ID")

    def test_output_id_high(self):
        """Error: router id is too high"""
        self.assertEqual(
            validate_data(
                1,
                [3001, 4001, 5001],
                [(5003, 3, 1), (9003, 3, 64001), (1303, 3, 13)],
                [10, 60, 40],
            ),
            False,
        )
        self.assertOutputEqual("Output Ports Configuration Error: ID")

    def test_output_id_valid(self):
        """Valid input: router ids"""
        self.assertEqual(
            validate_data(
                1,
                [3001, 4001, 5001],
                [(5003, 3, 1), (9003, 3, 64000), (1303, 3, 13)],
                [10, 60, 40],
            ),
            True,
        )

    def test_timers_periodic_1(self):
        """Error: incorrect periodic timer ratio"""
        self.assertEqual(
            validate_data(
                1,
                [3001, 4001, 5001],
                [(5003, 3, 5), (9003, 3, 9), (1303, 3, 13)],
                [10, 50, 40],
            ),
            False,
        )
        self.assertOutputEqual("Timers Configuration Error")

    def test_timers_gc(self):
        """Error: incorrect gc timer ratio"""
        self.assertEqual(
            validate_data(
                1,
                [3001, 4001, 5001],
                [(5003, 3, 5), (9003, 3, 9), (1303, 3, 13)],
                [10, 60, 30],
            ),
            False,
        )
        self.assertOutputEqual("Timers Configuration Error")

    def test_timers_periodic_2(self):
        """Error: incorrect periodic timer ratio"""
        self.assertEqual(
            validate_data(
                1,
                [3001, 4001, 5001],
                [(5003, 3, 5), (9003, 3, 9), (1303, 3, 13)],
                [10, 35, 40],
            ),
            False,
        )
        self.assertOutputEqual("Timers Configuration Error")

    def test_timers_wrong_self(self):
        """Error: generally incorrect timer ratios"""
        self.assertEqual(
            validate_data(
                1,
                [3001, 4001, 5001],
                [(5003, 3, 5), (9003, 3, 9), (1303, 3, 13)],
                [20, 10, 42],
            ),
            False,
        )
        self.assertOutputEqual("Timers Configuration Error")


if __name__ == "__main__":
    main()
