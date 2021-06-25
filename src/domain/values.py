from enum import IntEnum, auto
import importlib
from typing import Tuple, List, Type, Optional
import os
import yaml

from .contracts import ConfigObject
from .exceptions import ConfigPathError


class Point:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @property
    def coords(self):
        return (self._x, self._y)

    def __str__(self):
        return "(%s, %s)" % self.coords

    def __eq__(self, obj: object) -> bool:
        return obj.coords == self.coords


class Cardinal(IntEnum):
    N = auto()  # 1
    E = auto()  # 2
    S = auto()  # 3
    W = auto()  # 4

    @classmethod
    def get_members(cls):
        return cls._member_names_


class CardinalMoveMapping:
    """
    This is a mapping that gives the move offset for a given Cardinality.
    """
    __mapping = {
        Cardinal.N: (0, 1),
        Cardinal.E: (1, 0),
        Cardinal.S: (0, -1),
        Cardinal.W: (-1, 0)
    }

    @classmethod
    def get_move_offset(cls, cardinal: Cardinal) -> Point:
        """
        Returns the move offset for a cardinal value as a Point.
        """
        point_values = cls.__mapping[cardinal]
        return Point(*point_values)


class SpinCardinalMapping:
    """
    This is a mapping that gives the new cardinal/orientation offset with
    a given Spin instruction.
    """
    __mapping = {
        "L": -1,
        "R":  1,
    }

    @classmethod
    def get_cardinal_offset(cls, spin_to: str) -> int:
        return cls.__mapping[spin_to]


class MowerScheduleConfig(ConfigObject):
    def __init__(self,
                 initial_position: Point,
                 orientation: Cardinal,
                 commands: List[str]):
        self.initial_position = initial_position
        self.orientation = orientation
        self.commands = commands

    @classmethod
    def create_from_dict(cls, config_data: dict):
        return cls(
            initial_position=Point(
                **config_data['initial_position']
            ),
            orientation=getattr(Cardinal, config_data['orientation']),
            commands=[cmd for cmd in config_data['commands']],
        )

    @property
    def as_dict(self) -> dict:
        return dict(
            initial_position={'x': self.initial_position.coords[0],
                              'y': self.initial_position.coords[1]},
            orientation=self.orientation.name,
            commands=''.join(self.commands), )


class ApplicationConfig(ConfigObject):
    MODES = ('interactive', 'scheduled')

    def __init__(self,
                 controller_class: Type,
                 palete_dimension: Tuple[int, int],
                 mode: str = 'interactive',
                 schedules: Optional[List[MowerScheduleConfig]] = None):
        self.controller_class = controller_class
        self.palete_dimension = palete_dimension
        self.mode = mode
        self.schedules = schedules

    @classmethod
    def create_from_dict(cls, config_data: dict):
        mode = config_data.get('mode', 'interactive')
        if mode == 'interactive':
            schedules = None
        else:
            schedules = [
                MowerScheduleConfig.create_from_dict(sch)
                for sch in config_data.get('schedules')]

        return cls(
            controller_class=cls.get_controller_class_by_name(
                config_data['controller_class']),
            palete_dimension=(
                config_data['palete']['dimension']['rows'],
                config_data['palete']['dimension']['cols']
            ),
            mode=config_data.get('mode', 'interactive'),
            schedules=schedules, )

    @staticmethod
    def read_config_from_yaml(config_path: str = None) -> dict:
        if not config_path:
            config_path = os.getenv(
                'CONFIG_PATH',
                os.path.join(root_dir(), 'config', 'app.yml'))
        try:
            with open(config_path, 'r') as config_file:
                config_data = yaml.safe_load(config_file)
        except FileNotFoundError:
            raise ConfigPathError()

        return config_data

    @staticmethod
    def get_controller_class_by_name(class_name: str) -> Type:
        module = importlib.import_module('src.controllers')
        return getattr(module, class_name)

    @property
    def as_dict(self) -> dict:
        return dict(
            controller_class=self.controller_class.__name__,
            palete={
                'dimension': {
                    'rows': self.palete_dimension[0],
                    'cols': self.palete_dimension[1]
                }
            },
            mode=self.mode,
            schedules=[sch.as_dict for sch in self.schedules] if self.schedules else None, )


def root_dir():
    return os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)))
