import mido
from mido import MidiFile

mid = MidiFile('LevanPolka.mid')

#Constants and simple lambda for getting the frequency of a note - note 69 is 440 / middle C - every octave doubles frequency
g = 2**(1/12)
f = lambda midi: 440*g**(midi-69)
#    freq = f(midi)

listTrackData = []
for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        data = str(msg).split(" ")
        dictAdd = {}
        dictAdd["identifier"] = data.pop(0)
        if("note" in dictAdd["identifier"]):
            for point in data:
                dp = point.split("=")
                dictAdd[dp[0]] = dp[1]
            listTrackData.append(dictAdd)

print(listTrackData)
