# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import os
import sqlite3
from typing import Optional

from polaris.utils.database.db_utils import read_about_model_value, read_and_close


def driving_side(database_path: Optional[os.PathLike] = None, conn: Optional[sqlite3.Connection] = None) -> int:
    if database_path is None and conn is None:
        raise Exception("To retrieve an hand of driving you must provide a database connection OR a database path")
    with conn or read_and_close(database_path) as conn:
        side = read_about_model_value(conn, "hand_of_driving", cast=str, default="RIGHT")
        return -1 if side.upper() == "LEFT" else 1
