import cv2
import mediapipe as mp
from coordinates import proximity_score
from midi import MidiController

class App:
    def __init__(self, midiOutputName="loopMIDI Port 1", scale="bMajor"):
        self.mediaPipeHands = mp.solutions.hands
        self.mediapipeDraw = mp.solutions.drawing_utils
        self.hands = self.mediaPipeHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.camera = cv2.VideoCapture(0)
        self.midiController = MidiController(midiOutputName, scale)
        print("App initialized")
        print("Press 'q' on camera window to quit")

    def controlMidi(self, landmarks):
        thumbIndexProximity = proximity_score(0.25, landmarks.landmark[4], landmarks.landmark[8])
        indexProximity = proximity_score(0.1, landmarks.landmark[6], landmarks.landmark[7], landmarks.landmark[8])
        indexProximity = max(0.0, indexProximity - 0.2)
                
        if thumbIndexProximity < 0.8:
            self.midiController.setNote(landmarks.landmark[8].x)
        else:
            self.midiController.stopNote()
        
        self.midiController.setModulation(indexProximity)
        self.midiController.processMidi()

    def captureAndProcessImage(self):
        _, frame = self.camera.read()
        y, x, _ = frame.shape
        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(framergb)

        landmarks = []
        if result.multi_hand_landmarks:
            for handslms in result.multi_hand_landmarks:
                self.controlMidi(handslms)

                for lm in handslms.landmark:
                    lmx = int(lm.x * x)
                    lmy = int(lm.y * y)
                    landmarks.append([lmx, lmy])
                    
                self.mediapipeDraw.draw_landmarks(frame, handslms, self.mediaPipeHands.HAND_CONNECTIONS)
                
        for xStart in self.midiController.scalePositionDict.keys():
            xx = int(xStart * x)
            cv2.line(frame, (xx, 0), (xx, y), (255, 128, 0), 1)
        
        cv2.imshow("Camera", frame)

    def startApp(self):
        while True: 
            self.captureAndProcessImage()
            if cv2.waitKey(1) == ord('q'):
                break
        self.closeApp()

    def closeApp(self):
        self.midiController.closeMidi()
        self.camera.release()
        cv2.destroyAllWindows()