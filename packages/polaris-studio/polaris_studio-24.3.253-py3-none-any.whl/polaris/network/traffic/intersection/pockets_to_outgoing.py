# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from sqlite3 import Connection
from typing import List

from polaris.network.traffic.hand_of_driving import driving_side
from polaris.network.traffic.intersection.approximation import Approximation
from polaris.network.traffic.intersection.turn_type import turn_type


def pockets_to_out_link(inc: Approximation, outgoing: List[Approximation], lane_balance, supply_conn: Connection):
    drive_side = driving_side(conn=supply_conn)

    balance = movements_per_direction(drive_side, inc, outgoing)

    sequence = balance["RIGHT"] + balance["LEFT"] if drive_side == 1 else balance["LEFT"] + balance["RIGHT"]

    for out in sequence:  # type: Approximation
        lane_balance -= 1
        if out in balance["RIGHT"]:
            out.l_pckts = 1
        else:
            out.r_pckts = 1

        if lane_balance == 0:
            return


def movements_per_direction(drive_side, inc, outgoing):
    # Side turns would always come primarily from pockets, but we need to know how many turns to each side
    balance = {"LEFT": [], "RIGHT": [], "THRU": [], "UTURN": []}
    for out in outgoing:
        balance[turn_type(inc, out)].append(out)
    uturn_side = "LEFT" if drive_side == 1 else "RIGHT"
    balance[uturn_side].extend(balance["UTURN"])
    return balance
