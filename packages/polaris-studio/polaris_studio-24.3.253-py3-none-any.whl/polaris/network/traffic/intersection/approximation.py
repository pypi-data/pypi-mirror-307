# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import pandas as pd
import shapely.wkb
from shapely.geometry import LineString

from .find_directions import find_directions

pocket_table_fields = ["link", "dir", "type", "lanes", "length"]


class Approximation:
    """A link connecting to a node

    ::

        from polaris.network.network import Network

        net = Network()
        net.open('D:/Argonne/GTFS/CHICAGO/chicago2018-Supply.sqlite')
        intersection = net.get_intersection(2468)

        # List of all links that "Arrive in the node"
        intersection.incoming

        # List of all links that "depart from the node"
        intersection.outgoing

        # One can manipulate the possibility of approximations to have
        # pockets added when building connections based on link IDs
        # doing the following:

        for approx in intersection.incoming:
            if approx.link == 12345:
                approx.set_allow_pockets()

            if approx.link == 67890:
                approx.set_block_pockets()
    """

    #: Maximum pocket length
    max_pocket = 400
    pocket_insert_sql = "INSERT INTO Pocket(link,dir,type,lanes,length) VALUES(?,?,?,?,?)"
    pocket_table_fields = pocket_table_fields

    def __init__(self, data: list) -> None:
        self.node: int = data[0]
        self.link: int = data[1]
        self.lanes: int = data[2]
        self.geo: LineString = shapely.wkb.loads(data[3])
        self.link_rank: int = data[4]
        self.allows_pockets = data[5] > 0
        self.direction: int = data[6]
        self.function = data[7].lower()
        self.bearing: float = data[8]
        self.pocket_length: float = min(max(round(0.15 * self.geo.length, 0), 10), self.max_pocket)

        # If the field is not filled, then we allow for pockets
        self.cardinal: str = find_directions(self.bearing % 360)

        # These parameters are designed to be changed as a function of the other approximation it is compared to
        self.penalty = 0
        self.r_pckts: int = 0
        self.l_pckts: int = 0
        self._used_l_pckts: int = 0
        self._used_r_pckts: int = 0
        self._used_lanes: int = 0
        self._current_lane_to_use: int = 1
        self.__drive_dir: int = 1

    def set_allow_pockets(self):
        """Allows pockets to be built for this link"""
        self.allows_pockets = True

    def set_block_pockets(self):
        """Prevents pockets to be built for this link"""
        self.allows_pockets = False

    @property
    def pocket_data(self) -> pd.DataFrame:
        pckt = "MERGE" if self.function == "outgoing" else "TURN"
        dt = [[self.l_pckts, "LEFT"], [self.r_pckts, "RIGHT"]]
        dt = [[self.link, self.direction, f"{direc}_{pckt}", e, self.pocket_length] for e, direc in dt if e]
        return pd.DataFrame(dt, columns=pocket_table_fields)

    @property
    def has_pockets(self) -> bool:
        return self.r_pckts > 0 or self.l_pckts > 0

    def where_to_connect(self, num_lanes: int) -> str:
        if self.__drive_dir != 1:
            raise NotImplementedError("Only support for right-side driving for now")
        assert num_lanes > 0

        fulfilled = 0
        res_str = ""
        if self.r_pckts > self._used_r_pckts:
            res_str += ",R1"
            fulfilled += 1
        if fulfilled < num_lanes and self.lanes - self._used_lanes > 0:
            lanes = min(self.lanes - self._used_lanes, num_lanes - fulfilled)
            res_str += "," + ",".join([str(x + self._used_lanes + 1) for x in range(lanes)])
            fulfilled += lanes
        if fulfilled < num_lanes and self.l_pckts > self._used_l_pckts:
            res_str += ",L1"

        return res_str[1:]

    def mark_used(self, tot_lanes):
        """Marks a set of lanes as having been already connected"""
        used_lanes = self._used_r_pckts + self._used_l_pckts + self._used_lanes

        assigned = tot_lanes - used_lanes

        if self._used_r_pckts < self.r_pckts and assigned > 0:
            pockets = min(assigned, self.r_pckts - self._used_r_pckts)
            self._used_r_pckts = pockets
            assigned -= pockets

        if assigned > 0:
            lanes = min(assigned, self.lanes - self._used_lanes)
            self._used_lanes += lanes
            assigned -= lanes

        if assigned > 0:
            self._used_l_pckts = min(assigned, self.l_pckts - self._used_l_pckts)

    def total_lanes(self) -> int:
        """Returns all lanes this link has in the intersection"""
        return self.lanes + self.r_pckts + self.l_pckts

    def is_ramp(self):
        """Returns True if link is a Ramp and False otherwise"""
        return self.link_rank == 100

    def _reset_used_connections(self):
        self._used_l_pckts = 0
        self._used_r_pckts = 0
        self._current_lane_to_use = 1
        self._used_lanes = 0

    def __lt__(self, other):
        return self.bearing < other.bearing

    def __radd__(self, other):
        return other + self.lanes + self.r_pckts + self.l_pckts
