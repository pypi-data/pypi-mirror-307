# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from sqlite3 import Connection
from typing import List

from polaris.network.traffic.intersection.approximation import Approximation
from polaris.network.traffic.intersection.pockets_to_incoming import pockets_to_inc_link
from polaris.network.traffic.intersection.pockets_to_outgoing import pockets_to_out_link


def adds_pockets_for_approximation(inc: Approximation, outgoing: List[Approximation], supply_conn: Connection):
    if not inc.allows_pockets:
        return
    lane_balance = inc.lanes + inc.r_pckts + inc.l_pckts - sum([out.lanes for out in outgoing])

    if lane_balance == 0:
        return
    elif lane_balance < 0:  # We need pockets in the incoming link
        pockets_to_inc_link(inc, outgoing, lane_balance, supply_conn)
    else:
        pockets_to_out_link(inc, outgoing, lane_balance, supply_conn)
