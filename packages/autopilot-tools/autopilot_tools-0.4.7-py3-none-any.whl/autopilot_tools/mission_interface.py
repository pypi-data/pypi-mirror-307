#!/usr/bin/env python3
# This program is free software under the GNU General Public License v3.
# See <https://www.gnu.org/licenses/> for details.
# Author: Yuriy <1budsmoker1@gmail.com>

import time
import math
import logging
from functools import partial
from typing import List

from pymavlink import mavutil
from pymavlink.dialects.v20.ardupilotmega import \
    (MAVLink_mission_item_int_message, MAVLink_mission_count_message,
     MAV_MISSION_TYPE_FENCE, MAV_MISSION_TYPE_RALLY,
     MAV_MISSION_TYPE_MISSION,
     MAV_MISSION_ACCEPTED)

from autopilot_tools.mission_file.mission_file import Plan, MissionItem, ParamList
from autopilot_tools.mission_file.mission_result import MissionResult, StatusCode, StatusText
from autopilot_tools.exceptions import MavlinkTimeoutError
from autopilot_tools.utils import retry_command

logger = logging.getLogger(__name__)

class MissionInterface:
    def __init__(self, master) -> None:
        self.master = master

    def download_from_autopilot(self) -> List[MAVLink_mission_item_int_message]:
        def get_count() -> MAVLink_mission_count_message:
            self.master.mav.mission_request_list_send(
                self.master.target_system, self.master.target_component)
            return self.master.recv_match(type='MISSION_COUNT', blocking=True, timeout=1)

        count = retry_command(get_count)
        if count is None:
            raise MavlinkTimeoutError

        data = []
        i = 0
        while i < count.count:

            def get_mission_item() -> MAVLink_mission_item_int_message:
                self.master.mav.mission_request_int_send(
                    self.master.target_system, self.master.target_component, i)
                return self.master.recv_match(type='MISSION_ITEM_INT', blocking=True, timeout=1)

            data_item = retry_command(get_mission_item)
            if data_item is None:
                raise MavlinkTimeoutError

            if data_item.seq == i:
                i += 1
                data.append(data_item)
        self.master.mav.mission_ack_send(
            self.master.target_system, self.master.target_component, MAV_MISSION_ACCEPTED)
        return data

    def load_to_autopilot(self, path: str) -> StatusCode:
        mission_file = Plan(path)

        fence_items = mission_file.geofence.get_mission_item_representation()
        rally_points_length = mission_file.rally_points.get_mission_item_representation()
        mission_length = mission_file.mission.get_mission_item_representation()

        def send_mission_items(
                count: int, item_list: List[MissionItem], mission_type: int) -> StatusCode:
            self.master.mav.mission_count_send(
                self.master.target_system, self.master.target_component,
                count, mission_type
            )
            if not item_list:
                return StatusCode.EMPTY_MISSION_ITEM_LIST
            reached_last_item = False
            next_item = -1
            while not reached_last_item:
                res = self.master.recv_match(
                    type=['MISSION_REQUEST_INT', 'MISSION_REQUEST'], blocking=True, timeout=0.5)
                if res is None:
                    return StatusCode.MAVLINK_ERROR
                next_item = res.seq
                logger.debug(f"Sending {item_list[next_item]} with id {next_item}")

                to_send = item_list[next_item]

                params = ParamList(
                    *[x if x is not None else math.nan for x in to_send.params]
                )
                self.master.mav.mission_item_int_send(
                    self.master.target_system, self.master.target_component,
                    to_send.arguments.seq,
                    to_send.arguments.frame,
                    to_send.arguments.command,
                    to_send.arguments.current,
                    to_send.arguments.auto_continue,
                    params.param1,
                    params.param2,
                    params.param3,
                    params.param4,
                    params.x,
                    params.y,
                    params.z,
                    to_send.mission_type
                )

                if next_item == count - 1:
                    reached_last_item = True

            res = self.master.recv_match(type='MISSION_ACK', blocking=True, timeout=0.5)

            return StatusCode.OK if res is not None else StatusCode.MAVLINK_ERROR

        result = retry_command(
            partial(send_mission_items, *fence_items, MAV_MISSION_TYPE_FENCE),
            test=lambda x: x in [StatusCode.OK, StatusCode.EMPTY_MISSION_ITEM_LIST])
        if result is None:
            raise MavlinkTimeoutError

        result = retry_command(
            partial(send_mission_items, *rally_points_length, MAV_MISSION_TYPE_RALLY),
            test=lambda x: x in [StatusCode.OK, StatusCode.EMPTY_MISSION_ITEM_LIST])
        if result is None:
            raise MavlinkTimeoutError

        result = retry_command(
            partial(send_mission_items, *mission_length, MAV_MISSION_TYPE_MISSION),
            test=lambda x: x in [StatusCode.OK, StatusCode.EMPTY_MISSION_ITEM_LIST])
        if result is None:
            raise MavlinkTimeoutError
        logger.info('Mission upload complete')
        return StatusCode.OK

    def run(self, path: str = None, timeout: int = 100) -> MissionResult:
        if path is not None:
            self.load_to_autopilot(path)

        mission_data = self.download_from_autopilot()
        time.sleep(5)
        seq = 0
        start_time = time.time()
        time_elapsed = 0
        self.master.mav.command_long_send(
            self.master.target_system, self.master.target_component,
            mavutil.mavlink.MAV_CMD_MISSION_START,
            0,
            0, len(mission_data) - 1, 0, 0, 0, 0, 0
        )

        seq_zeroed = False
        logger.info(f"starting mission from {seq} mission_item")

        status_texts = []

        while not seq_zeroed and time_elapsed < timeout:
            msg = self.master.recv_match(type='MISSION_CURRENT', blocking=False)
            status = self.master.recv_match(type='STATUSTEXT', blocking=False)
            if status:
                status_texts.append(StatusText(status.severity, status.text))

            if msg is None:
                time.sleep(0.01)
                continue

            if msg.seq != seq:
                if msg.seq == 0:
                    seq_zeroed = True
                else:
                    seq = msg.seq
                    logger.info(f"mission_item {msg.seq} reached")
            time_elapsed = time.time() - start_time
        return MissionResult(
            StatusCode.OK if time_elapsed < timeout else StatusCode.MISSION_TIMEOUT,
            int(time_elapsed),
            len(mission_data),
            status_texts
        )
