from __future__ import division
from scipy import *
from os.path import isfile
from scikits.audiolab import wavread
import sys

def loadFile(file):
    '''
    :param file: plik do wczytania
    :return: czestotliwosc probkowania [Hz] i dane(sygnal)
    '''

    if not isfile(file):
        print "Podany argument nie jest plikiem"
        sys.exit("Brak pliku")

    data, rate, encoding = wavread(file)
    sig = [mean(d) for d in data]           # usrednianie z dwoch kanalow przy plikach stereo

    return rate, sig


def gender(rate, sig):

    w = rate
    signal = sig
    n = len(signal)
    frequency = linspace(0, w, n)
    spectrum = fft(signal)
    spectrum = abs(spectrum)
    amp, freq = [], []
    for i in range(len(frequency)):
        if 85 < frequency[i] < 255:
            freq.append(frequency[i])   # czestotliwosci ludzkiego glosu
            amp.append(spectrum[i])     # amplitudy
    index = amp.index(max(amp))         # index maksymalnej amplitudy
    most_freq = freq[index]             # czestotliwosc najczesciej wystepujaca
    if most_freq < 173:                 # decydowanie na podstawie czestotliwsoci o plci
        print 'M'
    else:
        print 'K'

if __name__ == '__main__':
    rate, signal = loadFile(sys.argv[1])
    gender(rate, signal)
