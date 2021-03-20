from clumper.clump import Clumper
import pytest
import itertools


def test_oversampling(base_clumper):
    with pytest.raises(ValueError):
        base_clumper.sample(n=len(base_clumper) + 1, replace=False)


def test_non_existent_weight(base_clumper):
    with pytest.raises(ValueError):
        base_clumper.sample(n=len(base_clumper) + 1, replace=False, weights="my-key")


@pytest.mark.parametrize("n,expected", [(0, 0), (1, 1), (5, 5), (10, 10), (26, 26)])
def test_sample_size(base_clumper, n, expected):
    """
    Check for sampling n items's size
    """
    assert len(base_clumper.sample(n, replace=False)) == expected


def check_for_duplicates(sampled_clumper):
    for i in range(len(sampled_clumper)):
        source_clump = sampled_clumper[i]
        for j in range(len(sampled_clumper)):
            if i != j:
                assert sampled_clumper[j] != source_clump, "Found duplicates"


@pytest.mark.parametrize("n", [0, 10, 5, 26])
def test_basic_sample_without_replacement(n):
    """
    Check that there are no duplicate values
    """
    clump = Clumper.read_json("http://calmcode.io/datasets/pokemon.json")
    sampled_without_replacement = clump.sample(n, replace=False)
    assert len(sampled_without_replacement) == n
    check_for_duplicates(sampled_without_replacement.collect())


@pytest.mark.parametrize("n", [200, 300])
def test_basic_sample_with_replacement(n):
    """
    Check that there is at least one duplicate value
    """
    clump = Clumper.read_json("http://calmcode.io/datasets/pokemon.json")
    sampled_without_replacement = clump.sample(n, replace=True)
    assert len(sampled_without_replacement) == n
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


@pytest.mark.parametrize(
    "replace, weights", itertools.product([True, False], ["hp", "attack"])
)
def test_weighted_sampling(replace, weights):
    clumper = Clumper.read_jsonl("https://calmcode.io/datasets/pokemon.jsonl")
    sampled = clumper.sample(n=10, replace=replace, weights=weights)
    assert len(sampled) == 10
    check_for_duplicates(sampled.collect())
