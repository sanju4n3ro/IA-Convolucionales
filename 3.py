import cv2

# Corregir el nombre de la función VideoCapture
captura = cv2.VideoCapture(0)

ret, frame = captura.read()

if ret:
    cv2.imwrite('captura.jpg', frame)

# Corregir el nombre del método para liberar la captura
captura.release()
