import math
from typing import List

import i2cdriver
from time import sleep

READ_CURRENT = 0
READ_RELAYS = 128
WRITE_RELAYS = 160


class PendingCommitError(Exception):
    pass


class ALxxFIUBoard:
    def __init__(self, relay_count: int, current_count: int):
        self.relay_count = relay_count
        self.current_count = current_count
        self.relay_buffer_size = math.ceil(self.relay_count / 4)
        self.relay_state_buffer = [False] * self.relay_count


class AL1010FIUBoard(ALxxFIUBoard):
    def __init__(self):
        super().__init__(12, 12)


class AL1032FIUBoard(ALxxFIUBoard):
    def __init__(self):
        super().__init__(32, 0)


class ALInstSwitch32ChBoard(ALxxFIUBoard):
    def __init__(self):
        super().__init__(76, 0)


class AL10xxFIUBoardClient:
    def __init__(self, device_info: ALxxFIUBoard, com_port: str, address: int):
        self.device_info = device_info
        self.address = address
        self.i2c = i2cdriver.I2CDriver(com_port)
        self.i2c.setspeed(400)
        self.pending_commit = False

    def _write_relays_raw(self, relay_mask: int):
        self.i2c.regwr(
            self.address,
            WRITE_RELAYS,
            relay_mask.to_bytes(self.device_info.relay_buffer_size, byteorder="little"),
        )
        sleep(0.04)

    def _read_relays_raw(self) -> int:
        return self.i2c.regrd(self.address, READ_RELAYS, "<H")

    def _read_current_raw(self) -> List[int]:
        return self.i2c.regrd(
            self.address, READ_CURRENT, f"{self.device_info.current_count}h"
        )

    def read_relays(self) -> List[bool]:
        if self.pending_commit:
            raise PendingCommitError()
        raw = self._read_relays_raw()
        states = []
        for idx in range(self.device_info.relay_count):
            states.append(bool(raw & 1 << idx))
        return states

    def set_relay(self, index: int, value: bool):
        self.device_info.relay_state_buffer[index] = value
        self.pending_commit = True

    def set_all_relays(self, value: bool):
        self.device_info.relay_state_buffer = [value] * self.device_info.relay_count
        self.pending_commit = True

    def commit_relays(self):
        raw = 0
        for idx, state in enumerate(self.device_info.relay_state_buffer):
            raw = raw | state << idx
        self._write_relays_raw(raw)
        self.pending_commit = False
