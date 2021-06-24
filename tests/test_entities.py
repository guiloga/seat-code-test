from src.domain.entities import Mower, Palete
from src.domain.values import Point, Cardinal

class TestMower:
    def test_creation(self):
        p = Point(0, 0)
        mower = Mower(p, Cardinal.N)
        assert isinstance(mower, Mower)
        assert mower.position == p
        assert mower.orientation == Cardinal.N


class TestPalete:
    def test_creation(self):
        dimension = (2, 2)
        palete = Palete(dimension)
        assert isinstance(palete, Palete)
        assert palete.rows == 2 and palete.cols == 2

    def test_is_outside(self):
        palete = Palete((3, 3))
        assert not palete.is_outside(Point(0, 0))
        assert not palete.is_outside(Point(3, 3))
        assert palete.is_outside(Point(4, 4))
