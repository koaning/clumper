from clumper.clump import Clumper
import pytest
import itertools


def test_oversampling_no_replace(base_clumper):
    """
    Make sure that over sampling is not allowed when sampling without replacement
    """
    with pytest.raises(ValueError):
        base_clumper.sample(n=len(base_clumper) + 1, replace=False)


def test_non_existent_weight(base_clumper):
    """
    Make sure that providing non existent weight key throws error
    """
    with pytest.raises(KeyError):
        base_clumper.sample(n=len(base_clumper) - 1, replace=False, weights="my-key")


@pytest.mark.parametrize("n", [0, 1, 19, 26])
def test_sample_size(base_clumper, n):
    """
    Make sure that sampling n element does indeed give n elements
    """
    assert len(base_clumper.sample(n, replace=False)) == n


def has_duplicate(sampled_clumper):
    for i in range(len(sampled_clumper)):
        source_clump = sampled_clumper[i]
        for j in range(len(sampled_clumper)):
            if i != j:
                if sampled_clumper[j] == source_clump:
                    return True
    return False


@pytest.mark.parametrize("n", [0, 1, 10, 19, 26])
def test_basic_sample_without_replacement(n):
    """
    Make sure that there are no duplicate values when sampling without replacement
    """
    clump = Clumper.read_json("http://calmcode.io/datasets/pokemon.json")
    sampled_without_replacement = clump.sample(n, replace=False)
    assert (
        has_duplicate(sampled_without_replacement.collect()) is False
    ), "Found duplicate elements when sampling without replacement"


@pytest.mark.parametrize("n", [200, 300])
def test_basic_sample_with_replacement(n):
    """
    Make sure that there are at least one duplicate values when sampling with replacement
    """
    clump = Clumper.read_json("http://calmcode.io/datasets/pokemon.json")
    sampled_with_replacement = clump.sample(n, replace=True)

    assert (
        has_duplicate(sampled_with_replacement.collect()) is True
    ), "Didn't find duplicate elements when sampling with replacement"


@pytest.mark.parametrize(
    "replace, weights", itertools.product([True, False], ["hp", "attack"])
)
def test_weighted_sampling(replace, weights):
    """
    Make sure that weighted sampling has duplicates when sampling with replacement (and vice versa)
    """
    clumper = Clumper.read_jsonl("https://calmcode.io/datasets/pokemon.jsonl")
    sampled = clumper.sample(n=200, replace=replace, weights=weights)
    if replace:
        assert (
            has_duplicate(sampled.collect()) is True
        ), "Didn't find duplicate elements in weighted sampling with replacement"
    else:
        assert (
            has_duplicate(sampled.collect()) is False
        ), "Found duplicate elements in weighted sampling without replacement"
