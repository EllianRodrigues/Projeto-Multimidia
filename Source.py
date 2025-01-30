import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial.distance import euclidean
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from comtypes import CLSCTX_ALL
import time
import ctypes

class handDetector:
    def __init__(self, mode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            self.mode, self.maxHands, self.modelComplex, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0):
        lmlist = []
        if self.results.multi_hand_landmarks:
            if handNo < len(self.results.multi_hand_landmarks):
                myHand = self.results.multi_hand_landmarks[handNo]

                for id, lm in enumerate(myHand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmlist.append((cx, cy))

        return lmlist


def normalize_landmarks(landmarks):
    """
    Normaliza os pontos da mão para torná-los independentes da posição e do tamanho.
    """
    if not landmarks:
        return []

    # Usa o ponto 0 (palma da mão) como referência
    base_x, base_y = landmarks[0]
    normalized = [(x - base_x, y - base_y) for x, y in landmarks]

    # Escala os pontos para normalizar o tamanho
    max_distance = max(np.linalg.norm([x, y]) for x, y in normalized)
    if max_distance > 0:
        normalized = [(x / max_distance, y / max_distance) for x, y in normalized]

    return normalized


def compare_positions(position1, position2, threshold=0.2):
    """
    Compara duas posições normalizadas para verificar similaridade.
    Retorna True se forem semelhantes.
    """
    if len(position1) != len(position2):
        return False

    distances = [euclidean(p1, p2) for p1, p2 in zip(position1, position2)]
    avg_distance = np.mean(distances)
    return avg_distance < threshold


def function_one():
    sessions = AudioUtilities.GetAllSessions()

    spotify_found = False
    for session in sessions:
        if session.Process and session.Process.name() == "Spotify.exe":
            spotify_found = True
            try:
                volume_interface = session._ctl.QueryInterface(ISimpleAudioVolume)
                current_volume = volume_interface.GetMasterVolume() * 100
                current_volume = current_volume + 2 if current_volume < 100 else 100
                if current_volume == 100:
                    return
                volume_interface.SetMasterVolume(current_volume/ 100, None)
                return
            except Exception as e:
                print(f"Erro ao aumentar o volume: {e}")
                return

    if not spotify_found:
        print("Spotify não encontrado em execução.")

def function_two():
    sessions = AudioUtilities.GetAllSessions()

    spotify_found = False
    for session in sessions:
        if session.Process and session.Process.name() == "Spotify.exe":
            spotify_found = True
            try:
                volume_interface = session._ctl.QueryInterface(ISimpleAudioVolume)
                current_volume = volume_interface.GetMasterVolume() * 100
                current_volume = current_volume - 2 if current_volume >= 2 else 0
                if current_volume == 0:
                    return
                volume_interface.SetMasterVolume(current_volume / 100, None)
                return
            except Exception as e:
                print(f"Erro ao diminuir o volume: {e}")
                return

    if not spotify_found:
        print("Spotify não encontrado em execução.")


def function_three():
    # Código da tecla multimídia "Próxima Faixa"
    VK_MEDIA_NEXT_TRACK = 0xB0
    
    # Simular o pressionamento da tecla
    ctypes.windll.user32.keybd_event(VK_MEDIA_NEXT_TRACK, 0, 0, 0)  # Pressionar a tecla
    time.sleep(0.8)  # Pequena pausa para garantir que o sistema registre
    ctypes.windll.user32.keybd_event(VK_MEDIA_NEXT_TRACK, 0, 2, 0)  # Soltar a tecla
    print("Comando enviado: Próxima música!")

def function_four():
    # Código da tecla multimídia "Próxima Faixa"
    VK_MEDIA_PREV_TRACK = 0xB1
    
    # Simular o pressionamento da tecla
    ctypes.windll.user32.keybd_event(VK_MEDIA_PREV_TRACK, 0, 0, 0)  # Pressionar a tecla
    time.sleep(0.8)  # Pequena pausa para garantir que o sistema registre
    ctypes.windll.user32.keybd_event(VK_MEDIA_PREV_TRACK, 0, 2, 0)  # Soltar a tecla
    print("Comando enviado: Próxima música!")


def function_five():   
    # Código da tecla multimídia "Próxima Faixa"
    VK_MEDIA_PLAY_PAUSE = 0xB3
    
    # Simular o pressionamento da tecla
    ctypes.windll.user32.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, 0, 0)  # Pressionar a tecla
    time.sleep(0.8)  # Pequena pausa para garantir que o sistema registre
    ctypes.windll.user32.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, 2, 0)  # Soltar a tecla
    print("Comando enviado: Próxima música!")


def draw_hud(img):
    overlay = img.copy()
    height, width, _ = img.shape

    # Criar HUD semi-transparente
    cv2.rectangle(overlay, (0, 0), (width, 100), (0, 0, 0), -1)  # Barra preta superior
    alpha = 0.5  # Transparência
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

    text_color = (255, 255, 255)  # Branco
    shadow_color = (0, 0, 0)  # Preto (sombra)

    def draw_text(text, x, y, size=0.5):
        cv2.putText(img, text, (x + 1, y + 1), cv2.FONT_HERSHEY_SIMPLEX, size, shadow_color, 2)
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, size, text_color, 1)

    draw_text("Commands:", 10, 30, 0.8)
    draw_text("1 - Volume Up | 2 - Volume Down | 3 - Next Song", 10, 55)
    draw_text("4 - Previous Song | 5 - Play/Pause | Q - Quit", 10, 75)

    return img

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
            for handNo, handLms in enumerate(detector.results.multi_hand_landmarks):
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
