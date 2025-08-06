import pytest

from pymeasure.instruments.thorlabs.thorlabspm100usb import ThorlabsPM100USB
from pymeasure.test import expected_protocol

POWER_SENSOR_IDN = b"TestSensor,SerialNum,29-APR-2025,1,0,289"
ENERGY_SENSOR_IDN = b"TestSensor,SerialNum,29-APR-2025,0,0,290"


def test_init():
    with expected_protocol(
        ThorlabsPM100USB,
        [(b"SYST:SENSOR:IDN?", POWER_SENSOR_IDN)],
    ):
        pass  # Verify the expected communication.


def test_zero():
    with expected_protocol(
        ThorlabsPM100USB,
        [(b"SYST:SENSOR:IDN?", POWER_SENSOR_IDN), (b"SENS:CORR:COLL:ZERO", None)],
    ) as inst:
        inst.zero()


def test_wavelength_min():
    with expected_protocol(
        ThorlabsPM100USB,
        [(b"SYST:SENSOR:IDN?", POWER_SENSOR_IDN), (b"SENS:CORR:WAV? MIN", 1000)],
    ) as inst:
        assert inst.wavelength_min == 1000


def test_wavelength_max():
    with expected_protocol(
        ThorlabsPM100USB,
        [(b"SYST:SENSOR:IDN?", POWER_SENSOR_IDN), (b"SENS:CORR:WAV? MAX", 2000)],
    ) as inst:
        assert inst.wavelength_max == 2000


def test_wavelength_getter():
    with expected_protocol(
        ThorlabsPM100USB,
        [(b"SYST:SENSOR:IDN?", POWER_SENSOR_IDN), (b"SENS:CORR:WAV?", b"1500")],
    ) as inst:
        assert inst.wavelength == 1500


def test_wavelength_setter():
    with expected_protocol(
        ThorlabsPM100USB,
        [
            (b"SYST:SENSOR:IDN?", POWER_SENSOR_IDN),
            ("SENS:CORR:WAV? MIN", b"1000"),
            ("SENS:CORR:WAV? MAX", b"2000"),
            (b"SENS:CORR:WAV 1500", None),
        ],
    ) as inst:
        inst.wavelength = 1500


def test_power():
    with expected_protocol(
        ThorlabsPM100USB,
        [(b"SYST:SENSOR:IDN?", POWER_SENSOR_IDN), (b"MEAS:POW?", b"0.1")],
    ) as inst:
        assert inst.power == 0.1


def test_power_range_getter():
    with expected_protocol(
        ThorlabsPM100USB,
        [(b"SYST:SENSOR:IDN?", POWER_SENSOR_IDN), (b"SENS:POW:RANG?", b"0.2")],
    ) as inst:
        assert inst.power_range == 0.2


def test_power_range_setter():
    with expected_protocol(
        ThorlabsPM100USB,
        [
            (b"SYST:SENSOR:IDN?", POWER_SENSOR_IDN),
            (b"SENS:POW:RANG 0.2", None),
            (b"SYST:ERR?", b"0,No error\n"),
        ],
    ) as inst:
        inst.power_range = 0.2


def test_power_auto_range_getter():
    with expected_protocol(
        ThorlabsPM100USB,
        [(b"SYST:SENSOR:IDN?", POWER_SENSOR_IDN), (b"SENS:POW:RANG:AUTO?", b"1")],
    ) as inst:
        assert inst.power_auto_range is True


def test_power_auto_range_setter():
    with expected_protocol(
        ThorlabsPM100USB,
        [(b"SYST:SENSOR:IDN?", POWER_SENSOR_IDN), (b"SENS:POW:RANG:AUTO 0", None)],
    ) as inst:
        inst.power_auto_range = False


def test_energy():
    with expected_protocol(
        ThorlabsPM100USB,
        [(b"SYST:SENSOR:IDN?", ENERGY_SENSOR_IDN), (b"MEAS:ENER?", b"1")],
    ) as inst:
        assert inst.energy == 1


def test_energy_range_getter():
    with expected_protocol(
        ThorlabsPM100USB,
        [(b"SYST:SENSOR:IDN?", ENERGY_SENSOR_IDN), (b"SENS:ENER:RANG?", b"0.2")],
    ) as inst:
        assert inst.energy_range == 0.2


def test_energy_range_setter():
    with expected_protocol(
        ThorlabsPM100USB,
        [
            (b"SYST:SENSOR:IDN?", ENERGY_SENSOR_IDN),
            (b"SENS:ENER:RANG 0.2", None),
            (b"SYST:ERR?", "0,No error\n"),
        ],
    ) as inst:
        inst.energy_range = 0.2


def test_energy_with_power_sensor():
    with pytest.raises(AttributeError):
        with expected_protocol(
            ThorlabsPM100USB,
            [(b"SYST:SENSOR:IDN?", POWER_SENSOR_IDN), (b"MEAS:ENER?", b"1")],
        ) as inst:
            _ = inst.energy


def test_power_with_energy_sensor():
    with pytest.raises(AttributeError):
        with expected_protocol(
            ThorlabsPM100USB,
            [(b"SYST:SENSOR:IDN?", ENERGY_SENSOR_IDN), (b"MEAS:POW?", b"1")],
        ) as inst:
            _ = inst.power
