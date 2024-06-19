from camera import App

if __name__ == '__main__':
    # Set your config here
    virtualMidiOutputPortName = "loopMIDI Port 1" # check your ports using mido.get_output_names()
    scale = "eMajor2Octave" # check the available scales in midi.py
    
    app = App(virtualMidiOutputPortName, scale)
    app.startApp()