# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from sqlite3 import Connection
from typing import List

from polaris.network.traffic.hand_of_driving import driving_side
from polaris.network.traffic.intersection.approximation import Approximation
from polaris.network.traffic.intersection.turn_type import turn_type


def pockets_to_inc_link(inc: Approximation, outgoing: List[Approximation], lane_balance, supply_conn: Connection):
    balance = lanes_per_direction(inc, outgoing, supply_conn)
    inc.r_pckts = 0
    inc.l_pckts = 0
    if lane_balance <= -2:
        if balance["RIGHT"] > 0:
            inc.r_pckts = 1
        if balance["LEFT"] > 0:
            inc.l_pckts = 1
    else:
        # If we only have one pocket, then we put to the side where there would be conflict: {LEFT: USA, RIGHT: UK}
        if driving_side(conn=supply_conn) == 1:
            has_pocket = "LEFT" if balance["LEFT"] < balance["RIGHT"] else "RIGHT"
        else:
            has_pocket = "RIGHT" if balance["RIGHT"] < balance["LEFT"] else "LEFT"

        if has_pocket == "LEFT":
            inc.l_pckts = 1
        elif has_pocket == "RIGHT":
            inc.r_pckts = 1


def lanes_per_direction(inc, outgoing, supply_conn):
    balance = {"LEFT": 0, "RIGHT": 0, "THRU": 0, "UTURN": 0}
    for out in outgoing:
        balance[turn_type(inc, out)] += out.lanes
    uturn_side = "LEFT" if driving_side(conn=supply_conn) == 1 else "RIGHT"
    # U-turn should never count as more than one lane
    balance[uturn_side] += min(1, balance["UTURN"])
    return balance
