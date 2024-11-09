import re
import numpy
from ewoksorange.tests.utils import execute_task

from ewoksxrpd.tasks.ascii import SaveAsciiMultiPattern1D
from orangecontrib.ewoksxrpd.ascii import OWSaveAsciiPattern1D


def test_save_ascii_task(tmpdir, setup1):
    assert_save_ascii(tmpdir, setup1, None)


def test_save_ascii_widget(tmpdir, setup1, qtapp):
    assert_save_ascii(tmpdir, setup1, qtapp)


def assert_save_ascii(tmpdir, setup1, qtapp):
    inputs = {
        "filename": str(tmpdir / "result.dat"),
        "x": numpy.linspace(1, 60, 60),
        "y": numpy.random.random(60),
        "xunits": "2th_deg",
        "header": {
            "energy": 10.2,
            "detector": setup1.detector,
            "detector_config": setup1.detector_config,
            "geometry": setup1.geometry,
        },
        "metadata": {"name": "mysample"},
    }

    execute_task(
        OWSaveAsciiPattern1D.ewokstaskclass if qtapp is None else OWSaveAsciiPattern1D,
        inputs=inputs,
    )

    x, y = numpy.loadtxt(str(tmpdir / "result.dat")).T
    numpy.testing.assert_array_equal(x, inputs["x"])
    numpy.testing.assert_array_equal(y, inputs["y"])

    with open(tmpdir / "result.dat") as f:
        lines = list()
        for line in f:
            if not line.startswith("#"):
                break
            lines.append(line)
    lines = "".join(lines)

    for key in (
        "detector",
        "energy",
        "distance",
        "center dim0",
        "center dim1",
        "rot1",
        "rot2",
        "rot3",
        "xunits",
    ):
        assert f"{key} =" in lines
    assert "name = mysample" in lines
    m = re.findall("energy = (.+) keV", lines)
    assert len(m) == 1
    assert float(m[0]) == inputs["header"]["energy"]


def test_save_multi_ascii(tmpdir, setup1):
    inputs = {
        "filenames": [str(tmpdir / "result1.dat"), str(tmpdir / "result2.dat")],
        "x_list": [numpy.linspace(1, 60, 60), numpy.linspace(1, 60, 60)],
        "y_list": [numpy.random.random(60), numpy.random.random(60)],
        "yerror_list": [numpy.random.random(60), numpy.random.random(60)],
        "xunits_list": ["2th_deg", "2th_rad"],
        "header_list": [
            {
                "energy": 10.2,
                "detector": setup1.detector,
                "geometry": setup1.geometry,
            },
            {
                "energy": 9.8,
                "detector": setup1.detector,
                "geometry": setup1.geometry,
            },
        ],
        "metadata_list": [{"name": "mysample"}, {"name": "mysample"}],
    }

    execute_task(SaveAsciiMultiPattern1D, inputs=inputs)

    for (
        filename,
        input_x,
        input_y,
        input_yerror,
        input_header,
        input_metadata,
    ) in zip(
        inputs["filenames"],
        inputs["x_list"],
        inputs["y_list"],
        inputs["yerror_list"],
        inputs["header_list"],
        inputs["metadata_list"],
    ):
        x, y, yerror = numpy.loadtxt(filename).T
        numpy.testing.assert_array_equal(x, input_x)
        numpy.testing.assert_array_equal(y, input_y)
        numpy.testing.assert_array_equal(yerror, input_yerror)

        with open(filename) as f:
            lines = list()
            for line in f:
                if not line.startswith("#"):
                    break
                lines.append(line)
        lines = "".join(lines)

        for key in (
            "detector",
            "energy",
            "distance",
            "center dim0",
            "center dim1",
            "rot1",
            "rot2",
            "rot3",
            "xunits",
        ):
            assert f"{key} =" in lines
        for k, v in input_metadata.items():
            assert f"{k} = {v}" in lines
        matches = re.findall("energy = (.+) keV", lines)
        assert len(matches) == 1
        assert float(matches[0]) == input_header["energy"]
