import pytest
from src.domain.contracts import ApplicationController
from src.domain.exceptions import ConfigPathError
from src.domain.values import ApplicationConfig, MowerScheduleConfig, Point, Cardinal, \
    CardinalMoveMapping, SpinCardinalMapping


class TestPoint:
    def test_creation(self):
        coords = (0, 0)
        p = Point(*coords)
        assert isinstance(p, Point)
        assert p.coords == coords


class TestCardinal:
    def test_types_values(self):
        cardinal_members = Cardinal.get_members()
        for member, value in zip(cardinal_members, range(1, len(cardinal_members))):
            cardinal_value = getattr(Cardinal, member)
            assert type(cardinal_value) == Cardinal
            assert cardinal_value == value


class TestCardinalMoveMapping:
    @pytest.mark.parametrize(
        "cardinal,offset",
        [(Cardinal.N, Point(0, 1)),
         (Cardinal.E, Point(1, 0)),
         (Cardinal.S, Point(0, -1)),
         (Cardinal.W, Point(-1, 0))],
    )
    def test_get_move_offset(self, cardinal, offset):
        assert CardinalMoveMapping.get_move_offset(cardinal) == offset


class TestSpinCardinalMapping:
    @pytest.mark.parametrize(
        "spin,offset",
        [('L', -1),
         ('R',  1)],
    )
    def test_get_cardinal_offset(self, spin, offset):
        assert SpinCardinalMapping.get_cardinal_offset(spin) == offset


class TestMowerScheduleConfig:
    @pytest.fixture(scope='class')
    def config_data(self):
        return {
            'initial_position': {'x': 0, 'y': 0},
            'orientation': 'N',
            'commands': 'LMLMLMLMM',
        }

    @pytest.mark.usefixtures('config_data')
    def test_create_from_dict(self, config_data):
        config = MowerScheduleConfig.create_from_dict(config_data)
        assert isinstance(config, MowerScheduleConfig)
    
    @pytest.mark.usefixtures('config_data')
    def test_as_dict(self, config_data):
        schedule_config = MowerScheduleConfig.create_from_dict(config_data)
        assert schedule_config.as_dict == config_data


class TestApplicationConfig:
    @pytest.fixture(scope='class')
    def config_data(self):
        return {
            'controller_class': 'SimpleGreenGrassController',
            'palete': { 'dimension': {'rows': 2, 'cols': 2} },
            'mode': 'interactive',
            'schedules': None,
        }

    @pytest.mark.usefixtures('config_data')
    def test_create_from_dict(self, config_data):
        app_config = ApplicationConfig.create_from_dict(config_data)
        assert isinstance(app_config, ApplicationConfig)
    
    @pytest.mark.usefixtures('config_data')
    def test_as_dict(self, config_data):
        app_config = ApplicationConfig.create_from_dict(config_data)
        assert app_config.as_dict == config_data

    def test_read_config_from_yaml(self):
        config_data = ApplicationConfig.read_config_from_yaml()
        assert isinstance(config_data, dict)

    def test_read_config_from_yaml_error(self):
        with pytest.raises(ConfigPathError):
            ApplicationConfig.read_config_from_yaml('/app.yml')

        assert ConfigPathError().__str__()

    def test_get_controller_class_by_name(self):
        controller_type = ApplicationConfig.get_controller_class_by_name(
            'SimpleGreenGrassController')
        assert issubclass(controller_type, ApplicationController)
