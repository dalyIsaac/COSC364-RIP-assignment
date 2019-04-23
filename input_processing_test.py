import sys
from io import StringIO
from socket import AF_INET
from unittest import TestCase, main

from input_processing import validate_entry
from packet import ResponseEntry
from routingtable import RoutingTable
from validate_data import MAX_ID, MAX_METRIC, MIN_ID, MIN_METRIC


class TestValidateEntry(TestCase):
    captured_output = StringIO()
    table: RoutingTable

    def setUp(self):
        self.captured_output = StringIO()
        sys.stdout = self.captured_output
        self.table = RoutingTable(2, 1, 1, 1)

    def assertOutputEqual(self, expected: str, endline="\n"):
        sys.stdout = sys.__stdout__
        self.assertEqual(expected + endline, self.captured_output.getvalue())

    def test_valid_entry(self):
        entry = ResponseEntry(afi=AF_INET, router_id=1, metric=1)
        self.assertEqual(validate_entry(self.table, entry), True)

    def test_afi(self):
        entry = ResponseEntry(afi=1, router_id=1, metric=1)
        self.assertEqual(validate_entry(self.table, entry), False)
        self.assertOutputEqual(
            "The value 1 for AFI does not match the expected "
            "value of AF_INET = 2."
        )

    def test_router_id(self):
        self.table = RoutingTable(1, 1, 1, 1)
        entry = ResponseEntry(afi=AF_INET, router_id=1, metric=17)
        self.assertEqual(validate_entry(self.table, entry), False)

    def test_router_id_low(self):
        entry = ResponseEntry(afi=AF_INET, router_id=0, metric=1)
        self.assertEqual(validate_entry(self.table, entry), False)
        self.assertOutputEqual(
            "The entry's router id of 0 should be an integer between "
            f"{MIN_ID} and {MAX_ID}, inclusive."
        )

    def test_router_id_high(self):
        entry = ResponseEntry(afi=AF_INET, router_id=64001, metric=1)
        self.assertEqual(validate_entry(self.table, entry), False)
        self.assertOutputEqual(
            "The entry's router id of 64001 should be an integer between "
            f"{MIN_ID} and {MAX_ID}, inclusive."
        )

    def test_metric_low(self):
        entry = ResponseEntry(afi=AF_INET, router_id=1, metric=0)
        self.assertEqual(validate_entry(self.table, entry), False)
        self.assertOutputEqual(
            "The entry's metric of 0 was not between the "
            f"expected range of {MIN_METRIC} and {MAX_METRIC}, inclusive."
        )

    def test_metric_high(self):
        entry = ResponseEntry(afi=AF_INET, router_id=1, metric=17)
        self.assertEqual(validate_entry(self.table, entry), False)
        self.assertOutputEqual(
            "The entry's metric of 17 was not between the "
            f"expected range of {MIN_METRIC} and {MAX_METRIC}, inclusive."
        )


if __name__ == "__main__":
    main()
