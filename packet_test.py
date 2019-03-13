from unittest import main, TestCase
from routingtable import RoutingTable
from routeentry import RouteEntry
from packet import construct_packets
from socket import AF_INET


class TestPacketConstruction(TestCase):

    def _test_single_packet(self, packet, expected_packet, iteration=0):
        for i, val in enumerate(expected_packet):
            self.assertEqual(packet[i], val, f"Iteration {iteration}. Failed on byte {i}. Expected: {val}. Received: {packet[i]}")
            
    def test_single_entry(self):
        """Tests a routing table, where the single entry does not match the given router_id"""
        table = RoutingTable(0)
        table.add_route(1, RouteEntry(3000, 1, 2)) # port: 3000, metric: 1, next_address: 2

        packets = construct_packets(table, 3)

        expected_packet = bytearray(24)
        expected_packet[0] = 2
        expected_packet[1] = 2
        expected_packet[2:4] = (0).to_bytes(2, "big")
        expected_packet[4:6] = AF_INET.to_bytes(2, "big")
        expected_packet[8:12] = (1).to_bytes(4, "big")
        expected_packet[20:24] = (1).to_bytes(4, "big")

        self.assertEqual(len(packets), 1)
        packet = packets[0]
        self.assertEqual(len(packet), len(expected_packet))
        self._test_single_packet(packet, expected_packet)

    
    def test_two_entries_router_id_clash(self):
        """
        Tests that a routing table with two entries, where one entry was learnt from the given router_id, only returns 
        one route.
        """
        table_router_id = 1
        table = RoutingTable(table_router_id)
        table.add_route(1, RouteEntry(3000, 1, 2))
        table.add_route(2, RouteEntry(3000, 2, 2, 3))

        packets = construct_packets(table, 3)

        expected_packet = bytearray(24)
        expected_packet[0] = 2
        expected_packet[1] = 2
        expected_packet[2:4] = (1).to_bytes(2, "big")
        expected_packet[4:6] = AF_INET.to_bytes(2, "big")
        expected_packet[8:12] = (1).to_bytes(4, "big")
        expected_packet[20:24] = (1).to_bytes(4, "big")

        self.assertEqual(len(packets), 1)
        packet = packets[0]
        self.assertEqual(len(packet), len(expected_packet))
        self._test_single_packet(packet, expected_packet)


    def test_two_entries_infinity(self):
        """
        Tests that a routing table with two entries, where one entry has a metric of infinity, but is flagged, is 
        returned.
        """
        table = RoutingTable(0)
        table.add_route(1, RouteEntry(3000, 1, 2))
        table.add_route(2, RouteEntry(3000, 16, 3))
        table[2].flag = True

        packets = construct_packets(table, 1)

        expected_packet = bytearray(44)
        expected_packet[0] = 2
        expected_packet[1] = 2
        expected_packet[2:4] = (0).to_bytes(2, "big")
        expected_packet[4:6] = AF_INET.to_bytes(2, "big")
        expected_packet[8:12] = (1).to_bytes(4, "big") #!
        expected_packet[20:24] = (1).to_bytes(4, "big")
        expected_packet[20+4:20+6] = AF_INET.to_bytes(2, "big")
        expected_packet[20+8:20+12] = (2).to_bytes(4, "big")
        expected_packet[20+20:20+24] = (16).to_bytes(4, "big")

        self.assertEqual(len(packets), 1)
        packet = packets[0]
        self.assertEqual(len(packet), len(expected_packet))
        self._test_single_packet(packet, expected_packet)

    def test_two_entries_flag(self):
        """
        Tests that a routing table with two entries, where one entry has a metric of infinity, and is not flagged, is not 
        returned.
        """
        table = RoutingTable(0)
        table.add_route(1, RouteEntry(3000, 1, 2))
        table.add_route(2, RouteEntry(3000, 16, 3))
        table[2].flag = False

        packets = construct_packets(table, 3)

        expected_packet = bytearray(24)
        expected_packet[0] = 2
        expected_packet[1] = 2
        expected_packet[2:4] = (0).to_bytes(2, "big")
        expected_packet[4:6] = AF_INET.to_bytes(2, "big")
        expected_packet[8:12] = (1).to_bytes(4, "big")
        expected_packet[20:24] = (1).to_bytes(4, "big")

        self.assertEqual(len(packets), 1)
        packet = packets[0]
        self.assertEqual(len(packet), len(expected_packet))
        self._test_single_packet(packet, expected_packet)
    
    def test_multiple_packets(self):
        """
        Tests that multiple packets are returned, when the number of routes is greater than 25.
        """
        # Number of entries inside the table: 32
        # Number of entries being sent out: 31
        table = RoutingTable(0)
        table.add_route(1, RouteEntry(3000, 1, 2))
        table.add_route(2, RouteEntry(3000, 16, 3))
        table[2].flag = False
        for i in range(30):
            table.add_route(i + 3, RouteEntry(3000, 1, 2))
        
        packets = construct_packets(table, 3)

        expected_packet1  = bytearray(504)
        expected_packet1[0] = 2
        expected_packet1[1] = 2
        expected_packet1[2:4] = (0).to_bytes(2, "big")
        diff = 1
        for i in range(25):
            if i + diff == 2:
                diff += 1
            expected_packet1[i*20+4:i*20+6] = AF_INET.to_bytes(2, "big")
            expected_packet1[i*20+8:i*20+12] = (i + diff).to_bytes(4, "big")
            expected_packet1[i*20+20:i*20+24] = (1).to_bytes(4, "big")

        expected_packet2 = bytearray(124)
        expected_packet2[0] = 2
        expected_packet2[1] = 2
        expected_packet2[2:4] = (0).to_bytes(2, "big")
        for i in range(6):
            expected_packet2[i*20+4:i*20+6] = AF_INET.to_bytes(2, "big")
            expected_packet2[i*20+8:i*20+12] = (i + 27).to_bytes(4, "big")
            expected_packet2[i*20+20:i*20+24] = (1).to_bytes(4, "big")

        expected_packets = [expected_packet1, expected_packet2]

        self.assertEqual(len(packets), 2)
        for i, packet in enumerate(packets):
            expected_packet = expected_packets[i]
            self.assertEqual(len(packet), len(expected_packet))
            self._test_single_packet(packet, expected_packet, i)

if __name__ == '__main__':
    main()
