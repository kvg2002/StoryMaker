import pytest

from pipeline.run_pipeline import run


def test_run_propagates_not_implemented_from_scenario_stage() -> None:
    with pytest.raises(NotImplementedError):
        run("겁쟁이가 용을 잡아야 한다")
