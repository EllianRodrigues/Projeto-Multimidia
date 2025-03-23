import cv2

from handDetector import handDetector
from utils import   draw_hud, normalize_landmarks, compare_positions, \
                    function_five, function_one, function_two, function_three, function_four

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    detector = handDetector()

    # Armazena os gestos registrados
    registered_gestures = {i: None for i in range(1, 6)}

    gesture_functions = {
        1: function_one,
        2: function_two,
        3: function_three,
        4: function_four,
        5: function_five
    }

    while True:
        success, img = cap.read()
        if not success:
            break

        img = detector.findHands(img)
        img = draw_hud(img)  # Aplica a HUD na imagem

        # Verifica se há mãos detectadas
        if detector.results.multi_hand_landmarks:
            for handNo, _ in enumerate(detector.results.multi_hand_landmarks):
                lmList = detector.findPosition(img, handNo)
                normalized_landmarks = normalize_landmarks(lmList)

                # Compara com os gestos registrados
                for gesture_id, gesture_position in registered_gestures.items():
                    if gesture_position and normalized_landmarks:
                        if compare_positions(gesture_position, normalized_landmarks):
                            cv2.putText(img, f"Gesto {gesture_id} Reconhecido!", 
                                        (50, 150 + 40 * gesture_id),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            gesture_functions[gesture_id]()

        cv2.imshow("Controle por Gestos", img)

        key = cv2.waitKey(1) & 0xFF
        if key in [ord(str(i)) for i in range(1, 6)]:
            gesture_id = int(chr(key))
            if normalized_landmarks:
                registered_gestures[gesture_id] = normalized_landmarks
                print(f"{gesture_id} registered !")

        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()