from clumper import Clumper

d = [
    {
        "download_count": 661467185,
        "project": "pyyaml",
        "url": "https://libraries.io/pypi/pyyaml",
        "data": [
            {"sourcerank": 25},
            {"dependents": 5280},
            {"versions": 24},
            {"stargazers": 1220},
            {"network": 281},
            {"watchers": 50},
            {"contributors": 31},
        ],
    },
    {
        "download_count": 640176111,
        "project": "docutils",
        "url": "https://libraries.io/pypi/docutils",
        "data": [{"sourcerank": 15}, {"dependents": 460}, {"versions": 26}],
    },
]


def test_unpack_dict():
    """Make sure that we can properly unnest the data property"""
    assert len(Clumper(d).unpack("data")) == 10
