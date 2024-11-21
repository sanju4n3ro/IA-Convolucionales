import cv2
import numpy as np
import matplotlib.pyplot as plt

# Corregir el nombre de la función
captura = cv2.VideoCapture(0)

while True:
    ret, frame = captura.read()
    
    if not ret:
        break
    
    cv2.imshow('Video en vivo', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Corregir el nombre del método para liberar la captura
captura.release()
cv2.destroyAllWindows()
