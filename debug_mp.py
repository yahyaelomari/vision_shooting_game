import mediapipe as mp
print(dir(mp))
try:
    print(mp.solutions)
    print("mp.solutions exists")
except AttributeError:
    print("mp.solutions does not exist")

import mediapipe.python.solutions as solutions
print("Imported mediapipe.python.solutions")
