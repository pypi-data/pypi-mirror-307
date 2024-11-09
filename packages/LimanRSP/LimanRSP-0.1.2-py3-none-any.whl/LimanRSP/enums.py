from enum import Enum


class SignalFilterType(Enum, str):
    LOWPASS = 'lowpass'
    HIGHPASS = 'highpass'
    BANDPASS = 'bandpass'
    BANDSTOP = 'bandstop'

class SignalFilterName(Enum, str):
    CHEBYSHEV_I = 'cheby1'
    CHEBYSHEV_II = 'cheby2'
    BUTTERWORTH = 'butterworth'
