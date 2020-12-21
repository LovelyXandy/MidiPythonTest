import mido
from mido import MidiFile

mid = MidiFile('levPolkXand.mid')
outputFile = open("output.txt", mode="w")

#Constants and simple lambda for getting the frequency of a note - note 69 is 440 / concert A - every octave doubles frequency
g = 2**(1/12)
f = lambda midi: 440*g**(midi-69)
#    freq = f(midi)
toms = 2
defDuration = 100
minNote = 0
minPause = 0

listTrackData = []
position = 0
#convert note events to a list of dictionaries
for i, track in enumerate(mid.tracks):
    print('Track {}: {} {}'.format(i, track.name, len(track)))
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

print(listTrackData[0:10])

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
#print(rollDict["78off"])

    
for noteEvent in listTrackData:
    if(noteEvent["identifier"] == "note_on"):
        try:
            noteEvent["duration"] = rollDict[noteEvent["note"]+"off"].pop(0)["abs"]-rollDict[noteEvent["note"]+"on"].pop(0)["abs"]
            noteList.append(noteEvent)
        except:
            #print("No matching off ", str(noteEvent["note"]))
            noteEvent["duration"] = defDuration
            noteList.append(noteEvent)

print(len(noteList))

for i, j in zip(noteList, noteList[1:]):
    if(int(i["note"]) >= minNote):
        outputFile.write("music.play_tone(" + str(int(f(int(i["note"])))) + ", " + str(int(i["duration"])*toms) + ")\n")

    if(minPause <= ((j["abs"]-i["abs"])*toms)):
        outputFile.write("basic.pause("+str((j["abs"]-i["abs"])*toms)+")\n")

outputFile.close()
