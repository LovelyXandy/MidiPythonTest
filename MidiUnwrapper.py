import mido
from mido import MidiFile

mid = MidiFile('LevanPolka.mid')

#Constants and simple lambda for getting the frequency of a note - note 69 is 440 / concert A - every octave doubles frequency
g = 2**(1/12)
f = lambda midi: 440*g**(midi-69)
#    freq = f(midi)

listTrackData = []
#convert note events to a list of dictionaries
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

#print(listTrackData)

noteList = []
rollDict = {}

for noteEvent in listTrackData:
    if(noteEvent["identifier"] == "note_on"):
        if(noteEvent["note"]+"on" in rollDict):
            rollDict[noteEvent["note"]+"on"].append = noteEvent.values()
        else:
            rollDict[noteEvent["note"]+"on"] = [noteEvent.values()]
    else:
        if(noteEvent["note"]+"off" in rollDict):
            rollDict[noteEvent["note"]+"off"].append = noteEvent.values()
        else:
            rollDict[noteEvent["note"]+"off"] = [noteEvent.values()]
    
