from enum import Enum


class SignalFilterType(str, Enum):
    LOWPASS = 'lowpass'
    HIGHPASS = 'highpass'
    BANDPASS = 'bandpass'
    BANDSTOP = 'bandstop'

class SignalFilterName(str, Enum):
    CHEBYSHEV_I = 'cheby1'
    CHEBYSHEV_II = 'cheby2'
    BUTTERWORTH = 'butterworth'
