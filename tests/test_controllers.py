import pytest

from src.controllers import SimpleGreenGrassController
from src.utils import start_scheduled_controllers, run_scheduled_controllers
from src.domain.values import ApplicationConfig, MowerScheduleConfig, Point, Cardinal
from src.domain.entities import Mower, Palete
from src.domain.exceptions import InvalidCommandError, VoidScheduleError


class TestSimpleGreenGrassController:
    @pytest.fixture(scope='class')
    def controller_deps(self):
        schedule_config = MowerScheduleConfig(
            Point(0, 0), Cardinal.N, 'LMRLMRMLMRM')

        mower = Mower(
            schedule_config.initial_position,
            schedule_config.orientation)

        palete = Palete((2, 2))
        
        return mower, palete, schedule_config

    @pytest.fixture(scope='class')
    @pytest.mark.usefixtures('controller_deps')
    def controller(self, controller_deps):
        return SimpleGreenGrassController(*controller_deps)
        
    @pytest.mark.usefixtures('controller_deps')
    def test_creation(self, controller_deps):
        controller = SimpleGreenGrassController(*controller_deps)
        assert controller
        assert controller.uuid

    @pytest.mark.usefixtures('controller')
    def test_move(self, controller):
        controller.move()
        assert controller._mower.position == Point(0, 1)

    @pytest.mark.usefixtures('controller')
    def test_spin(self, controller):
        controller.spin('R')
        assert controller._mower.orientation.name == 'E'

        controller.spin('L')
        assert controller._mower.orientation.name == 'N'

    @pytest.mark.usefixtures('controller')
    def test_cmd_handler(self, controller):
        controller.cmd_manager('L')
        assert controller._mower.orientation.name == 'W'

        controller.cmd_manager('M')
        assert controller._is_outside_of_palete == True
        
        controller.cmd_manager('R')
        assert controller._mower.orientation.name == 'N'
    
    @pytest.mark.usefixtures('controller')
    def test_finish(self, controller):
        controller.finish()
        assert controller.finished

    def test_run_schedule(self):
        config_data = ApplicationConfig.read_config_from_yaml()
        app_config = ApplicationConfig.create_from_dict(
            config_data)

        controllers = start_scheduled_controllers(app_config)
        run_scheduled_controllers(controllers)
        
        c1, c2 = controllers
        assert c1._mower.position == Point(1, 3) and c1._mower.orientation.name == 'N'
        assert c2._mower.position == Point(5, 1) and c2._mower.orientation.name == 'E'
    
    @pytest.mark.usefixtures('controller_deps')
    def test_void_schedule_error(self, controller_deps):
        controller = SimpleGreenGrassController(*controller_deps[:2])
        assert controller._schedule is None

        with pytest.raises(VoidScheduleError):
            controller.run_schedule()
        
        assert VoidScheduleError().__str__()
    
    @pytest.mark.usefixtures('controller')
    def test_invalid_command(self, controller):
        with pytest.raises(InvalidCommandError):
            controller.cmd_manager('T')
        
        assert InvalidCommandError(None, None).__str__()
