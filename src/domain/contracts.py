from abc import ABC, abstractmethod
from typing import Tuple
from uuid import UUID
import uuid


class ApplicationController(ABC):
    __uuid: UUID = None
    CLI: Tuple = None  # Command Interface

    @property
    def uuid(self):
        return str(self.__uuid)[:8]

    @uuid.setter
    def uuid(self, uuid_: UUID):
        self.__uuid = uuid_

    @abstractmethod
    def cmd_manager(self, cmd: str, *args, **kwargs):
        pass

    def validate_cmd(self, cmd: str):
        if cmd not in self.CLI:
            # todo: customize that exception
            raise Exception()


class ConfigObject(ABC):
    """
    Config object serialized and deserialized from dict.
    """
    @classmethod
    @abstractmethod
    def create_from_dict(cls, config_data: dict):
        pass

    @property
    @abstractmethod
    def as_dict(self) -> dict:
        pass
