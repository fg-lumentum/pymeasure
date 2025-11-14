#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2025 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import pytest

from pymeasure.instruments import SCPIKeyword, SCPIKeywordEnum
from pymeasure.instruments.validators import strict_discrete_set

from test_common_base import CommonBase, FakeBase


# === SCPIKeyword ===


@pytest.mark.parametrize(
    "value, shortform",
    (
        ("ALPHa", "ALPH"),
        ("ALPH", "ALPH"),
        ("ALPHa1", "ALPH1"),
        (SCPIKeyword("ALPHa"), "ALPH"),
    ),
)
def test_scpi_keyword_init_valid(value, shortform):
    assert SCPIKeyword(value).shortform == shortform


@pytest.mark.parametrize("value", [1234])
def test_scpi_keyword_init_type_error(value):
    with pytest.raises(TypeError):
        SCPIKeyword(value)


@pytest.mark.parametrize("value", ("ALPHa-1", "alpha", "alPHa", "A1PHa"))
def test_scpi_keyword_init_value_error(value):
    with pytest.raises(ValueError):
        SCPIKeyword(value)


def test_scpi_keyword_repr():
    assert repr(SCPIKeyword("ALPHa")) == "SCPIKeyword('ALPHa')"


def test_scpi_keyword_str():
    assert ("%s" % SCPIKeyword("ALPHa")) == "ALPH"


@pytest.mark.parametrize(
    "value, valid",
    [
        ("Alph", True),
        ("Alpha", True),
        (SCPIKeyword("ALPHa"), True),
        ("ALP", False),
        (SCPIKeyword("ALPH"), False),
    ],
)
def test_scpi_keyword_matches(value, valid):
    assert SCPIKeyword("ALPHa").matches(value) is valid


@pytest.mark.parametrize("value, valid", [("ALPH", True), ("ALPHa", False)])
def test_scpi_keyword_hash(value, valid):
    assert (hash(SCPIKeyword("ALPHa")) == hash(value)) is valid


@pytest.mark.parametrize("value", ["ALPH", SCPIKeyword("ALPHa")])
def test_scpi_keyword_strict_discrete_set_valid(value):
    strict_discrete_set(value, {SCPIKeyword("ALPHa")})


@pytest.mark.parametrize("value", ["ALP", SCPIKeyword("ALPH"), False])
def test_scpi_keyword_strict_discrete_set_value_error(value):
    with pytest.raises(ValueError):
        strict_discrete_set(value, {SCPIKeyword("ALPHa")})


@pytest.mark.parametrize("dynamic", [False, True])
def test_scpi_keyword_control(dynamic):
    class Fake(FakeBase):
        x = CommonBase.control(
            "",
            "%s",
            "",
            validator=strict_discrete_set,
            values={SCPIKeyword("ALPHa")},
            dynamic=dynamic,
        )

    fake = Fake()
    fake.x = "Alpha"
    assert fake.read() == "ALPHa"
    fake.x = "alph"
    assert fake.x == "ALPHa"
    fake.x = "ALPHA"
    assert type(fake.x) is SCPIKeyword


# === SCPIKeywordEnum ===


class AlphaKeywordEnum(SCPIKeywordEnum):
    ALPHA = "ALPHa"
    BRAVO = SCPIKeyword("BRAVo")


@pytest.mark.parametrize("entry", [AlphaKeywordEnum.ALPHA, AlphaKeywordEnum.BRAVO])
def test_scpi_keyword_enum_str(entry):
    assert str(entry) == str(entry.value)


@pytest.mark.parametrize(
    "entry, value, valid",
    [
        (AlphaKeywordEnum.ALPHA, SCPIKeyword("ALPHa"), True),
        (AlphaKeywordEnum.ALPHA, "Alpha", True),
        (AlphaKeywordEnum.ALPHA, "alph", True),
        (AlphaKeywordEnum.ALPHA, "ALP", False),
        (AlphaKeywordEnum.BRAVO, SCPIKeyword("BRAVo"), True),
        (AlphaKeywordEnum.BRAVO, "Bravo", True),
        (AlphaKeywordEnum.BRAVO, "brav", True),
    ],
)
def test_scpi_keyword_enum_eq(entry, value, valid):
    assert (entry.value == value) is valid


@pytest.mark.parametrize(
    "entry, value",
    [
        (AlphaKeywordEnum.ALPHA, SCPIKeyword("ALPHa")),
        (AlphaKeywordEnum.ALPHA, "Alpha"),
        (AlphaKeywordEnum.ALPHA, "alph"),
        (AlphaKeywordEnum.BRAVO, SCPIKeyword("BRAVo")),
        (AlphaKeywordEnum.BRAVO, "Bravo"),
        (AlphaKeywordEnum.BRAVO, "brav"),
    ],
)
def test_scpi_keyword_enum_lookup_valid(entry, value):
    assert AlphaKeywordEnum(value) is entry


@pytest.mark.parametrize("input_value", ["Charlie", "", None])
def test_scpi_keyword_enum_lookup_value_error(input_value):
    with pytest.raises(ValueError):
        AlphaKeywordEnum(input_value)
