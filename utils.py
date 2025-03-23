import cv2
import mediapipe as mp
import numpy as np
import time
import ctypes

from scipy.spatial.distance import euclidean
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

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