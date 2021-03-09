import pytest


def test_oversampling(base_clumper):
    with pytest.raises(ValueError):
        base_clumper.sample(n=len(base_clumper) + 1, replace=False)


@pytest.mark.parametrize("n,expected", [(0, 0), (5, 5), (10, 10), (26, 26)])
def test_sample_size(base_clumper, n, expected):
    """
    Check for sampling n items's size
    """
    assert len(base_clumper.sample(n, replace=False)) == expected


@pytest.mark.parametrize("n,expected", [(0, 0), (5, 5), (10, 10), (26, 26)])
def test_sample_without_replacement(base_clumper, n, expected):
    """
    Check that there are no duplicate values
    """
    sampled_without_replacement = base_clumper.sample(n, replace=False)
    assert len(sampled_without_replacement) == expected

    sampled_without_replacement_blob = sampled_without_replacement.collect()

    for i in range(len(sampled_without_replacement)):
        source_clump = sampled_without_replacement_blob[i]
        for j in range(len(sampled_without_replacement)):
            if i != j:
                assert (
                    sampled_without_replacement_blob[j] != source_clump
                ), "Found duplicates"


@pytest.mark.parametrize("n,expected", [(10, 10), (15, 15), (26, 26)])
def test_sample_with_replacement(base_clumper, n, expected):
    """
    Check that there is at least one duplicate value
    """
    sampled_without_replacement = base_clumper.sample(n, replace=True)
    assert len(sampled_without_replacement) == expected

    sampled_without_replacement_blob = sampled_without_replacement.collect()

    has_duplicate = False
    for i in range(len(sampled_without_replacement)):
        source_clump = sampled_without_replacement_blob[i]
        for j in range(len(sampled_without_replacement)):
            if i != j:
                if sampled_without_replacement_blob[j] == source_clump:
                    has_duplicate = True
                    break

    assert has_duplicate, "Didn't find any duplicates"
