import mido
from mido import MidiFile

mid = MidiFile('LevanPolka.mid')
outputFile = open("output.txt", mode="w")

#Constants and simple lambda for getting the frequency of a note - note 69 is 440 / concert A - every octave doubles frequency
g = 2**(1/12)
f = lambda midi: 440*g**(midi-69)
#    freq = f(midi)
toms = 5

listTrackData = []
position = 0
#convert note events to a list of dictionaries
for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    if (i == 1):
        for msg in track:
            data = str(msg).split(" ")
            dictAdd = {}
            dictAdd["identifier"] = data.pop(0)
            if("note" in dictAdd["identifier"]):
                for point in data:
                    dp = point.split("=")
                    dictAdd[dp[0]] = dp[1]
                position += int(dictAdd["time"])
                dictAdd["abs"] = position
                listTrackData.append(dictAdd)

#print(listTrackData)

noteList = []
rollDict = {}

for noteEvent in listTrackData:
    if(noteEvent["identifier"] == "note_on"):
        if(noteEvent["note"]+"on" in rollDict):
            rollDict[noteEvent["note"]+"on"].append(noteEvent)
        else:
            rollDict[noteEvent["note"]+"on"] = [noteEvent]
    else:
        if(noteEvent["note"]+"off" in rollDict):
            rollDict[noteEvent["note"]+"off"].append(noteEvent)
        else:
            rollDict[noteEvent["note"]+"off"] = [noteEvent]
    
#print(rollDict["42on"])
#print(rollDict["42off"])

    
for noteEvent in listTrackData:
    if(noteEvent["identifier"] == "note_on"):
        noteEvent["duration"] = rollDict[noteEvent["note"]+"off"].pop(0)["abs"]-rollDict[noteEvent["note"]+"on"].pop(0)["abs"]
        noteList.append(noteEvent)

for i, j in zip(noteList, noteList[1:]):
    outputFile.write("music.play_tone(" + str(int(f(int(i["note"])))) + ", " + str(int(i["duration"])*toms) + ")\n")
    outputFile.write("basic.pause("+str((j["abs"]-i["abs"])*toms)+")\n")
