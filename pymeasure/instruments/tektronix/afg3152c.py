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
from math import sqrt, log10
from pymeasure.instruments import Instrument, Channel, SCPIUnknownMixin
from pymeasure.instruments.validators import strict_range, strict_discrete_set


class AFG3152CChannel(Channel):
    SHAPES = {
        "sinusoidal": "SIN",
        "square": "SQU",
        "pulse": "PULS",
        "ramp": "RAMP",
        "prnoise": "PRN",
        "dc": "DC",
        "sinc": "SINC",
        "gaussian": "GAUS",
        "lorentz": "LOR",
        "erise": "ERIS",
        "edecay": "EDEC",
        "haversine": "HAV",
    }
    FREQ_LIMIT = [1e-6, 150e6]  # Frequency limit for sinusoidal function
    DUTY_LIMIT = [0.001, 99.999]
    AMPLITUDE_LIMIT = {
        "VPP": [20e-3, 10],
        "VRMS": list(map(lambda x: round(x / 2 / sqrt(2), 3), [20e-3, 10])),
        "DBM": list(
            map(lambda x: round(20 * log10(x / 2 / sqrt(0.1)), 2), [20e-3, 10])
        ),
    }  # Vpp, Vrms and dBm limits
    UNIT_LIMIT = ["VPP", "VRMS", "DBM"]
    IMP_LIMIT = [1, 1e4]

    shape = Instrument.control(
        "function:shape?",
        "function:shape %s",
        """ Control the shape of the output. (str)""",
        validator=strict_discrete_set,
        values=SHAPES,
        map_values=True,
    )

    unit = Instrument.control(
        "voltage:unit?",
        "voltage:unit %s",
        """ Control the amplitude unit. (str)""",
        validator=strict_discrete_set,
        values=UNIT_LIMIT,
    )

    amp_vpp = Instrument.control(
        "voltage:amplitude?",
        "voltage:amplitude %eVPP",
        """Control the output amplitude in Vpp. (float)""",
        validator=strict_range,
        values=AMPLITUDE_LIMIT["VPP"],
    )

    amp_dbm = Instrument.control(
        "voltage:amplitude?",
        "voltage:amplitude %eDBM",
        """ Control the output amplitude in dBm. (float)""",
        validator=strict_range,
        values=AMPLITUDE_LIMIT["DBM"],
    )

    amp_vrms = Instrument.control(
        "voltage:amplitude?",
        "voltage:amplitude %eVRMS",
        """ Control the output amplitude in Vrms. (float)""",
        validator=strict_range,
        values=AMPLITUDE_LIMIT["VRMS"],
    )

    offset = Instrument.control(
        "voltage:offset?",
        "voltage:offset %e",
        """ Control the amplitude offset. It is always in Volt. (float)""",
    )

    frequency = Instrument.control(
        "frequency:fixed?",
        "frequency:fixed %e",
        """ Control the frequency. (float)""",
        validator=strict_range,
        values=FREQ_LIMIT,
    )

    duty = Instrument.control(
        "pulse:dcycle?",
        "pulse:dcycle %.3f",
        """ Control the duty cycle of pulse. (float))""",
        validator=strict_range,
        values=DUTY_LIMIT,
    )

    impedance = Instrument.control(
        "output:impedance?",
        "output:impedance %d",
        """ Control the output impedance of the channel. Be careful with this.""",
        validator=strict_range,
        values=IMP_LIMIT,
        cast=int,
    )

    def insert_id(self, command):
        """Prepend the channel id for most writes."""
        return f'source{self.id}:{command}'

    def enable(self):
        self.parent.write("output%d:state on" % self.number)

    def disable(self):
        self.parent.write("output%d:state off" % self.number)

    def waveform(
        self, shape="SIN", frequency=1e6, units="VPP", amplitude=1, offset=0
    ):
        """General setting method for a complete wavefunction"""
        self.write("function:shape %s" % shape)
        self.write("frequency:fixed %e" % frequency)
        self.write("voltage:unit %s" % units)
        self.write("voltage:amplitude %e%s" % (amplitude, units))
        self.write("voltage:offset %eV" % offset)


class AFG3152C(SCPIUnknownMixin, Instrument):
    """Represents the Tektronix AFG 3000 series (one or two channels)
    arbitrary function generator and provides a high-level for
    interacting with the instrument.

    .. code-block:: python

        afg=AFG3152C("GPIB::1")        # AFG on GPIB 1
        afg.reset()                    # Reset to default
        afg.ch1.shape='sinusoidal'     # Sinusoidal shape
        afg.ch1.unit='VPP'             # Sets CH1 unit to VPP
        afg.ch1.amp_vpp=1              # Sets the CH1 level to 1 VPP
        afg.ch1.frequency=1e3          # Sets the CH1 frequency to 1KHz
        afg.ch1.enable()               # Enables the output from CH1
    """

    def __init__(self, adapter, name="Tektronix AFG3152C arbitrary function generator", **kwargs):
        super().__init__(
            adapter,
            name,
            **kwargs
        )
        self.ch1 = AFG3152CChannel(self, 1)
        self.ch2 = AFG3152CChannel(self, 2)

    def beep(self):
        self.write("system:beep")

    def opc(self):
        return int(self.ask("*OPC?"))
