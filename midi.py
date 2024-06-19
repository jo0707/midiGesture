import mido
from mido import Message

scales = {
            "chromatic": [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71],
            "cMajor": [72, 74, 76, 77, 79, 81, 83, 84],
            "dMajor": [74, 76, 78, 79, 81, 83, 85, 86],
            "eMajor": [76, 78, 80, 81, 83, 85, 87, 88],
            "fMajor": [77, 79, 81, 82, 84, 86, 88, 89],
            "gMajor": [79, 81, 83, 84, 86, 88, 90, 91],
            "aMajor": [81, 83, 85, 86, 88, 90, 92, 93],
            "bMajor": [83, 85, 87, 88, 90, 92, 94, 95],
            "cMinor": [72, 74, 75, 77, 79, 80, 82, 84],
            "dMinor": [74, 76, 77, 79, 81, 82, 84, 86],
            "eMinor": [76, 78, 79, 81, 83, 84, 86, 88],
            "fMinor": [77, 79, 80, 82, 84, 85, 87, 89],
            "gMinor": [79, 81, 82, 84, 86, 87, 89, 91],
            "aMinor": [81, 83, 84, 86, 88, 89, 91, 93],
            "bMinor": [83, 85, 86, 88, 90, 91, 93, 95],
            "cMajor2Octave": [72, 74, 76, 77, 79, 81, 83, 84, 86, 88, 90, 91, 93, 95, 96],
            "dMajor2Octave": [74, 76, 78, 79, 81, 83, 85, 86, 88, 90, 92, 93, 95, 97, 98],
            "eMajor2Octave": [76, 78, 80, 81, 83, 85, 87, 88, 90, 92, 93, 95, 97, 99, 100],
            "fMajor2Octave": [77, 79, 81, 82, 84, 86, 88, 89, 91, 93, 95, 96, 98, 100, 101],
            "gMajor2Octave": [79, 81, 83, 84, 86, 88, 90, 91, 93, 95, 97, 98, 100, 102, 103],
            "aMajor2Octave": [81, 83, 85, 86, 88, 90, 92, 93, 95, 97, 99, 100, 102, 104, 105],
            "bMajor2Octave": [83, 85, 87, 88, 90, 92, 94, 95, 97, 99, 101, 102, 104, 106, 107],
            "cMinor2Octave": [72, 74, 75, 77, 79, 80, 82, 84, 86, 87, 89, 91, 92, 94, 96],
            "dMinor2Octave": [74, 76, 77, 79, 81, 82, 84, 86, 88, 89, 91, 93, 94, 96, 98],
            "eMinor2Octave": [76, 78, 79, 81, 83, 84, 86, 88, 90, 91, 93, 95, 96, 98, 100],
            "fMinor2Octave": [77, 79, 80, 82, 84, 85, 87, 89, 91, 92, 94, 96, 97, 99, 101],
            "gMinor2Octave": [79, 81, 82, 84, 86, 87, 89, 91, 93, 94, 96, 98, 99, 101, 103],
            "aMinor2Octave": [81, 83, 84, 86, 88, 89, 91, 93, 95, 96, 98, 100, 101, 103, 105],
            "bMinor2Octave": [83, 85, 86, 88, 90, 91, 93, 95, 97, 98, 100, 102, 103, 105, 107],
}

class MidiController:
    def __init__(self, midiOutputName="loopMIDI Port 1", scale="cMajor"):
        try:
            self.outPort = mido.open_output(midiOutputName)
            print(f"Connected to MIDI output port {midiOutputName}")
        except:
            print(f"MIDI output port with name {midiOutputName} not found, check your ports using mido.get_output_names()")
            exit()
        
        self.scalePositionDict = {}
        self.isNoteOn = False
        self.stateChanged = False
        self.currentNote = None
        self.modulation = None
        self.previousNote = None
        self.initializeScales(scale)

    def closeMidi(self):
        self.outPort.send(Message('note_off', note=self.currentNote, velocity=100))
        self.outPort.send(Message('note_off', note=self.previousNote, velocity=100))
        self.outPort.close()

    def initializeScales(self, scale="cMajor"):
        currentScale = scales.get(scale, None)
        if currentScale == None:
            print(f"Scale {scale} not found, check the available scales in midi.py")
            currentScale = scales["cMajor"]
        else:
            print(f"Using scale {scale}")
        
        widthPerNote = 1 / len(currentScale)
        self.scalePositionDict = {i * widthPerNote: note for i, note in enumerate(currentScale)}

    def setNote(self, x: float):
        note = None
        for xStart in reversed(self.scalePositionDict.keys()):
            if x >= xStart:
                note = self.scalePositionDict[xStart]
                break

        if note == None or (self.isNoteOn and note == self.currentNote):
            return

        self.isNoteOn = True
        self.currentNote = note
        self.stateChanged = True
        
    def setModulation(self, modulation: float):
        if modulation < 0 or modulation == self.modulation:
            return
        
        self.modulation = round(modulation * 127)
        self.stateChanged = True

    def stopNote(self):
        if not self.isNoteOn:
            return
        
        self.isNoteOn = False
        self.stateChanged = True

    def processMidi(self):
        if not self.stateChanged or self.currentNote == None:
            return

        if not self.isNoteOn:
            self.outPort.send(Message('note_off', note=self.currentNote, velocity=100))
            self.outPort.send(Message('note_off', note=self.previousNote, velocity=100))
            print("Note off")
            return

        if self.currentNote != None and self.currentNote != self.previousNote and self.isNoteOn:
            self.outPort.send(Message('note_on', note=self.currentNote, velocity=100))
            
            if self.previousNote != None:
                self.outPort.send(Message('note_off', note=self.previousNote, velocity=100))
            
            self.previousNote = self.currentNote
            print(f"Playing note on {self.currentNote}")

        if self.modulation != None:
            self.outPort.send(Message('control_change', control=1, value=self.modulation))
            print(f"Modulation set to {self.modulation}")

        self.stateChanged = False