import argparse
import logging

from src.domain.values import ApplicationConfig
from src.utils import start_scheduled_controllers, run_scheduled_controllers, \
    run_interactive_mode

LOGGER = logging.getLogger('appLogger')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Seat Code Test - Mower App")
    parser.add_argument('--config',
                        help='The application config file path.',
                        dest='config_path',
                        required=False)
    parser.add_argument('--interactive',
                        help='Flag to force run in interactive mode.',
                        dest='interactive',
                        action=argparse.BooleanOptionalAction,
                        default=False)
    cli_args = parser.parse_args()

    config_data = ApplicationConfig.read_config_from_yaml(cli_args.config_path)
    app_config = ApplicationConfig.create_from_dict(config_data)
    
    if cli_args.interactive:
        run_mode = 'interactive'
    else:
        run_mode = app_config.mode

    LOGGER.info("Running in '%s' mode" % run_mode)
    LOGGER.info("config_path: '%s'" % (cli_args.config_path or 'default', ))
    LOGGER.info("ApplicationConfig: %s" % app_config.as_dict)
    if run_mode == 'interactive':
        run_interactive_mode(app_config)
    else:
        controllers = start_scheduled_controllers(app_config)
        run_scheduled_controllers(controllers)
