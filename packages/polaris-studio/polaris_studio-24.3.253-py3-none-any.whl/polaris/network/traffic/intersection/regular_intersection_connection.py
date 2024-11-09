# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import sqlite3
from typing import List

from polaris.network.traffic.intersection.approximation import Approximation
from polaris.network.traffic.intersection.approximation_list import pure_list_sorting
from polaris.network.traffic.intersection.connectionrecord import ConnectionRecord
from polaris.network.traffic.intersection.intersecsuperclass import IntersecSuperClass
from polaris.network.traffic.intersection.lane_allocation import lane_allocation
from polaris.network.traffic.intersection.lane_out_direc import adds_pockets_for_approximation
from polaris.network.traffic.intersection.should_allow import should_allow


class GenericIntersection(IntersecSuperClass):
    """Computes the connections for generic intersections

    These intersections are all those not falling within any of the special cases.
    Please check the corresponding documentation for algorithm/logic details

    In the process of processing the intersection, approximations are changed in order
    to consider the pockets necessary.

    This class is not intended to be used independently, but one could do that:

    ::

       from polaris.network.network import Network
       from polaris.network.consistency.network_objects.intersection.regular_intersection_connection import GenericIntersection

       net = Network()
       net.open(connection_test_file)
       i = net.get_intersection(1)
       regular = GenericIntersection(i)

       connections = regular.build()
    """

    def __init__(self, intersection):
        super(GenericIntersection, self).__init__(intersection)

    def build(self, conn: sqlite3.Connection) -> List[ConnectionRecord]:
        self.__assess_pocket_needs(conn)

        for inc in self.inter.incoming:  # type: Approximation
            inc._reset_used_connections()
            departures = self.__allowed_movements(inc)
            deps, _, _ = pure_list_sorting(departures + [inc])
            position = [i for i, approx in enumerate(deps) if approx.function == "incoming"][0]

            departures = []
            if position != len(deps):
                departures = deps[position + 1 :]
            if position > 0:
                departures.extend(deps[:position])

            for approx in departures:
                approx._reset_used_connections()
            self.__one_to_many(inc, departures)

        self._reassess_pocket_needs()
        return self.connects

    def __assess_pocket_needs(self, conn):
        for inc in self.inter.incoming:
            departures = self.__allowed_movements(inc)
            adds_pockets_for_approximation(inc, departures, conn)

    def __one_to_many(self, inc: Approximation, departures: List[Approximation]):
        self._compute_balance()
        allocation = lane_allocation(inc, departures)

        for out, alloc in zip(departures, allocation):
            lanes = inc.where_to_connect(int(max(1, alloc)))
            inc.mark_used(int(alloc))

            lanes_to_string = out.where_to_connect(out.total_lanes())
            out.mark_used(out.total_lanes())

            con = ConnectionRecord(inc, out, lanes=lanes, to_lanes=lanes_to_string)
            self.connects.append(con)

    def __allowed_movements(self, inc: Approximation) -> List[Approximation]:
        return [out for out in self.inter.outgoing if should_allow(self.inter, inc, out)]
