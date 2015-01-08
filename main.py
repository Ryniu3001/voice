#from __future__ import division
import scipy.io.wavfile
import struct
from pylab import *
from numpy import *
from scipy import *
from os import listdir
from os.path import isfile, join, splitext
from scikits.audiolab import wavread

def loadFiles(path):
    """reads wave files from path and returns dictionary with fields:
        - "name" - name of file
        - "nameGender" - a sex readed from filename
        - "signal" - numpy array with sound signal readed from file
        - "sampleRate" - sample rate of the file

        and dictionary that contains numbers of male and female voices
    """
    print "reading files..."

    files = [f for f in listdir(path) if isfile(join(path, f)) and splitext(f)[1] == ".wav"]

    samples = []
    maleCount = 0
    femaleCount = 0
    for f in files:
        p = path + '/' + f

        print "...", f
        data, rate, encoding = wavread(p)
        sig = [mean(d) for d in data]
        samples.append({'name': f, 'nameGender': f[-5:-4], 'signal': sig, 'sampleRate': rate})

        if f[-5:-4] == "M":
            maleCount += 1
        else:
            femaleCount += 1

    counters = {"maleCount": maleCount, "femaleCount": femaleCount}
    return samples, counters


def recognizeGender(sample):
    # This function recognizes the sex of person who is speaking

    # argument: single sample from dictionary that is returned by loadFiles

    # returns: string - 'M' i a man is speaking, 'K' if a woman is speaking
    t = 3
    w = sample['sampleRate']
    n = w * t  #t*w
    signal = sample['signal']
    nframe = len(signal)
    #if n > nframe:
    n = nframe
    frequency = linspace(0, w, n)
    spectrum = fft(signal)
    spectrum = abs(spectrum)
    amp, freq = [], []
    for i in range(len(frequency)):
        if 85 < frequency[i] < 255:
            freq.append(frequency[i])
            amp.append(spectrum[i])
    index = amp.index(max(amp))
    avg_freq = freq[index]
    if avg_freq < 173:
        return 'M', avg_freq
    else:
        return 'K', avg_freq


def launchAlgorithm(samples, counters):
    recognizedMale = 0
    recognizedFemale = 0
    wellRecognized = 0

    print "Launching algorithm..."
    for s in samples:
        gender, avf = recognizeGender(s)

        if gender == s['nameGender']:
            wellRecognized += 1

            if gender == "M":
                recognizedMale += 1
            elif gender == "K":
                recognizedFemale += 1
            else:
                print "...algorithm returned wrong value: ", s['name']

            print "...", s['name'], "...ok!", avf
        else:
            print "...", s['name'], "...not so good", avf

    samplesCount = counters['maleCount'] + counters['femaleCount']
    print "\nStatistics..."
    print "...Well recognized Male: ", recognizedMale, "/", counters['maleCount']
    print "...Well recognized Female: ", recognizedFemale, "/", counters['femaleCount']
    print "...Total: ", wellRecognized, "/", samplesCount, " (", wellRecognized / samplesCount * 100, "%)"


if __name__ == '__main__':
    samples, counters = loadFiles("train")
    # print samples
    print(counters)
    #makePlots(samples)
    launchAlgorithm(samples, counters)
