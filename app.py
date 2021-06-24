import argparse
import logging
from typing import List

from src.domain.contracts import ApplicationController
from src.domain.entities import Mower, Palete
from src.domain.values import ApplicationConfig

LOGGER = logging.getLogger('appLogger')


def _start_scheduled_controllers(app_config: ApplicationConfig):
    scheduled_controllers = []
    for schedule in app_config.schedules:
        # create a new controller for each schedule routine
        scheduled_controllers.append(
            app_config.controller_class(
                Mower(position=schedule.initial_position,
                      orientation=schedule.orientation),
                Palete(app_config.palete_dimension),
                schedule=schedule)
        )
    return scheduled_controllers


def _run_scheduled_controllers(controllers: List[ApplicationController]):
    for ctrl in controllers:
        ctrl.run_schedule()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Seat Code Test - Mower App")
    parser.add_argument('--config',
                        help='The application config file path.',
                        dest='config_path',
                        required=False)
    cli_args = parser.parse_args()

    config_data = ApplicationConfig.read_config_from_yaml(cli_args.config_path)
    app_config = ApplicationConfig.create_from_dict(config_data)

    LOGGER.info("Running in '%s' mode" % app_config.mode)
    LOGGER.info("config_path: '%s'" % (cli_args.config_path or 'default', ))
    LOGGER.info("ApplicationConfig: %s" % app_config.as_dict)
    if app_config.mode == 'interactive':
        pass
    else:
        controllers = _start_scheduled_controllers(app_config)
        _run_scheduled_controllers(controllers)
