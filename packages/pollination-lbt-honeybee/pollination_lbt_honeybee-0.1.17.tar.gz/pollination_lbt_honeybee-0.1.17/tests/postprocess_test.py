from pollination.lbt_honeybee.postprocess import Breeam4b
from queenbee.plugin.function import Function


def test_breeam_4b():
    function = Breeam4b().queenbee
    assert function.name == 'breeam4b'
    assert isinstance(function, Function)
