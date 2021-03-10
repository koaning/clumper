import pytest


def test_oversampling(base_clumper):
    with pytest.raises(ValueError):
        base_clumper.sample_frac(frac=1.1, replace=False, random_state=42)
