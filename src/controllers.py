from uuid import uuid4
import logging
from typing import Type, Optional

from .domain.contracts import ApplicationController
from .domain.entities import Mower, Palete
from .domain.values import Cardinal, MowerScheduleConfig, Point, CardinalMoveMapping, SpinCardinalMapping

LOGGER = logging.getLogger('appLogger')


class SimpleGreenGrassController(ApplicationController):
    """
    A simple green grass controller with optional scheduled commands config.
    """
    CLI = ('L', 'R', 'M')
    SPIN_COMMANDS = ('L', 'R')
    move_mapper: Type = CardinalMoveMapping
    spin_mapper: Type = SpinCardinalMapping
    
    def __init__(self,
                 mower: Mower,
                 palete: Palete,
                 schedule: Optional[MowerScheduleConfig] = None):
        self._mower = mower
        self._palete = palete
        self._schedule = schedule
        self._finished = False
        LOGGER.info(f"[{self.uuid}] INIT position=%s orientation=%s" %
                    (self._mower.initial_position, self._mower.orientation.name))
    
    def __new__(cls, *args, **kwargs):
        inst = super().__new__(cls)
        inst.uuid = uuid4()
        LOGGER.info(f"[{inst.uuid}] Started a new application controller type '{cls.__name__}'")
        return inst

    def cmd_manager(self, cmd, *args, **kwargs):
        LOGGER.info(f"[{self.uuid}] CMD => '{cmd}'")
        super().validate_cmd(cmd)
        if cmd in self.SPIN_COMMANDS:
            self.spin(cmd, *args, **kwargs)
        else:
            self.move()
        LOGGER.info(f"[{self.uuid}] position=%s orientation=%s" %
                    (self._mower.position, self._mower.orientation.name))

    def move(self):
        offset = self.move_mapper.get_move_offset(self._mower.orientation)
        self._mower.position = Point(
            self._mower.position.coords[0] + offset.coords[0],
            self._mower.position.coords[1] + offset.coords[1])
        
        if self._palete.is_outside(self._mower.position):
            LOGGER.info(f"[{self.uuid}] ¡¡¡ Current position is outside of Palete !!!")
    
    def spin(self, to: str):
        value = self._mower.orientation.value + self.spin_mapper.get_cardinal_offset(to)
        if value == 0:
            cardinal_value = len(Cardinal)
        elif value > len(Cardinal):
            cardinal_value = 1
        else:
            cardinal_value = value
        self._mower.orientation = Cardinal(cardinal_value)

    def run_schedule(self):
        LOGGER.info(f"[{self.uuid}] Running scheduled commands '%s' .." %
                    ''.join(self._schedule.commands))

        if self._schedule:
            for cmd in self._schedule.commands:
                self.cmd_manager(cmd)
        else:
            # todo: customize that exception
            raise Exception()

        self._finished = True
        LOGGER.info(f"[{self.uuid}] Controller schedule finished: position=%s orientation=%s" %
                    (self._mower.position, self._mower.orientation.name))