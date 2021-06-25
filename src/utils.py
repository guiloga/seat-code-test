from typing import List

from src.domain.contracts import ApplicationController
from src.domain.entities import Mower, Palete
from src.domain.values import ApplicationConfig, Point, Cardinal


def start_scheduled_controllers(app_config: ApplicationConfig):
    scheduled_controllers = []
    for schedule in app_config.schedules:
        scheduled_controllers.append(
            app_config.controller_class(
                Mower(position=schedule.initial_position,
                      orientation=schedule.orientation),
                Palete(app_config.palete_dimension),
                schedule=schedule)
        )
    return scheduled_controllers


def run_scheduled_controllers(controllers: List[ApplicationController]):
    for ctrl in controllers:
        ctrl.run_schedule()


def run_interactive_mode(app_config: ApplicationConfig):  # pragma: no cover
    # todo: exception handling
    pos_ = input(
        ">> Enter initial position coordinates in format <x,y> i.e 0,0: ") or '0,0'
    initial_position = Point(*[int(x) for x in pos_.split(',')])

    cd_name = input(
        ">> Enter initial orientation [N, E, S, W] i.e N: ") or 'N'
    orientation = getattr(Cardinal, cd_name)

    mower = Mower(initial_position, orientation)

    rows_cols = input(
        ">> Enter Palete dimension in format <num_rows,num_cols> i.e 5,5: ") or '5,5'
    palete = Palete(tuple(int(x) for x in rows_cols.split(',')))

    controller = app_config.controller_class(mower, palete)

    while not controller.finished:
        next_cmd = input(
            ">> Enter a new command %s ('X' to finish): " % [cmd for cmd in controller.CLI])
        if next_cmd == 'X':
            controller.finish()
        else:
            controller.cmd_manager(next_cmd)
