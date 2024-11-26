import cv2
import numpy as np

def detect_shape(contour):
    # Aproxima el contorno
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    x, y, w, h = cv2.boundingRect(approx)

    # Calcula el área y perímetro del contorno
    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)

    # Filtra figuras por tamaño mínimo
    if area < 500:  # Ajusta este valor según tu caso
        return None, (x, y, w, h)

    # Determina la forma basándose en los vértices y relaciones geométricas
    if len(approx) == 3:
        return 'Triangulo', (x, y, w, h)
    elif len(approx) == 4:
        aspect_ratio = float(w) / h
        if 0.8 <= aspect_ratio <= 1.2:
            return 'Cuadrado aproximado', (x, y, w, h)
        else:
            return 'Rectangulo aproximado', (x, y, w, h)
    elif 5 <= len(approx) <= 6:
        return 'Poligono (5-6 lados)', (x, y, w, h)
    elif len(approx) > 6:
        circularity = (4 * np.pi * area) / (perimeter ** 2)
        if 0.6 <= circularity <= 1.3:  # Tolerancia para formas circulares
            return 'Circulo aproximado', (x, y, w, h)
        else:
            return 'Elipse u otra forma redonda', (x, y, w, h)
    return 'Forma desconocida', (x, y, w, h)

# Inicia la captura de video desde la cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()  # Lee un fotograma de la cámara
    if not ret:
        print("Error: No se pudo capturar el video.")
        break

    # Suaviza la imagen para reducir el ruido
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

    # Aplica el detector de bordes Canny
    canny = cv2.Canny(gray, 50, 150)
    canny = cv2.dilate(canny, None, iterations=1)
    canny = cv2.erode(canny, None, iterations=1)

    # Encuentra contornos
    cnts, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Muestra el frame en tiempo real
    cv2.imshow('Presiona "Espacio" o "c"', frame)

    # Espera una tecla
    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):  # Detecta todas las figuras al presionar "c"
        for contour in cnts:
            shape, (x, y, w, h) = detect_shape(contour)
            if shape:
                cv2.putText(frame, shape, (x, y - 10), 1, 1, (0, 255, 0), 2)
                cv2.drawContours(frame, [contour], 0, (0, 255, 0), 2)
        cv2.imshow('Deteccion', frame)

    elif key == ord(' '):  # Detecta una figura a la vez al presionar la barra espaciadora
        if cnts:
            contour = cnts.pop(0)  # Saca el primer contorno de la lista
            shape, (x, y, w, h) = detect_shape(contour)
            if shape:
                cv2.putText(frame, shape, (x, y - 10), 1, 1, (0, 255, 0), 2)
                cv2.drawContours(frame, [contour], 0, (0, 255, 0), 2)
            cv2.imshow('Deteccion', frame)

    if key == ord('q'):  # Termina el programa al presionar "q"
        break

cap.release()
cv2.destroyAllWindows()