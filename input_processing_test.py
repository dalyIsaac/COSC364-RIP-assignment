from socket import AF_INET
from unittest import TestCase, main
from unittest.mock import Mock, patch

from input_processing import validate_entry
from packet import ResponseEntry
from routingtable import RoutingTable
from validate_data import MAX_ID, MAX_METRIC, MIN_ID, MIN_METRIC


class TestValidateEntry(TestCase):
    table: RoutingTable

    def setUp(self):
        self.table = RoutingTable(2, 1, 1, 1)

    def assertOutputEqual(self, expected: str, logger: Mock):
        actual = ""
        for item in logger.call_args:
            if isinstance(item, tuple):
                for i in item:
                    actual += i
        self.assertEqual(expected, actual)

    def test_valid_entry(self):
        entry = ResponseEntry(afi=AF_INET, router_id=1, metric=1)
        self.assertEqual(validate_entry(self.table, entry), True)

    @patch("input_processing.logger")
    def test_afi(self, logger):
        entry = ResponseEntry(afi=1, router_id=1, metric=1)
        self.assertEqual(validate_entry(self.table, entry), False)
        self.assertOutputEqual(
            "The value 1 for AFI does not match the expected "
            "value of AF_INET = 2.",
            logger,
        )

    @patch("input_processing.logger")
    def test_router_id(self, logger):
        self.table = RoutingTable(1, 1, 1, 1)
        entry = ResponseEntry(afi=AF_INET, router_id=1, metric=17)
        self.assertEqual(validate_entry(self.table, entry), False)

    @patch("input_processing.logger")
    def test_router_id_low(self, logger):
        entry = ResponseEntry(afi=AF_INET, router_id=0, metric=1)
        self.assertEqual(validate_entry(self.table, entry), False)
        self.assertOutputEqual(
            "The entry's router id of 0 should be an integer between "
            f"{MIN_ID} and {MAX_ID}, inclusive.",
            logger,
        )

    @patch("input_processing.logger")
    def test_router_id_high(self, logger):
        entry = ResponseEntry(afi=AF_INET, router_id=64001, metric=1)
        self.assertEqual(validate_entry(self.table, entry), False)
        self.assertOutputEqual(
            "The entry's router id of 64001 should be an integer between "
            f"{MIN_ID} and {MAX_ID}, inclusive.",
            logger,
        )

    @patch("input_processing.logger")
    def test_metric_low(self, logger):
        entry = ResponseEntry(afi=AF_INET, router_id=1, metric=0)
        self.assertEqual(validate_entry(self.table, entry), False)
        self.assertOutputEqual(
            "The entry's metric of 0 was not between the "
            f"expected range of {MIN_METRIC} and {MAX_METRIC}, inclusive.",
            logger,
        )

    @patch("input_processing.logger")
    def test_metric_high(self, logger):
        entry = ResponseEntry(afi=AF_INET, router_id=1, metric=17)
        self.assertEqual(validate_entry(self.table, entry), False)
        self.assertOutputEqual(
            "The entry's metric of 17 was not between the "
            f"expected range of {MIN_METRIC} and {MAX_METRIC}, inclusive.",
            logger,
        )


if __name__ == "__main__":
    main()
