
import math
from src.config import *
import pyautogui
import time
import cv2
import numpy as np
import pytesseract
from playsound import playsound
from PIL import ImageOps

# ==============================================================================
# =========================== FUNÇÕES AUXILIARES ===============================
# ==============================================================================
# Em utils.py

# Em src/utils.py
# Em utils.py

# Em src/utils.py

def find_and_read_pixel_count():
    """
    Busca o ícone âncora na tela inteira, valida o candidato correto
    verificando o texto adjacente com OCR e retorna os pixels disponíveis.
    Este método é totalmente automático e lida com telas de alta resolução (Retina).
    """
    try:
        screenshot_cv = np.array(pyautogui.screenshot())
        screenshot_gray = cv2.cvtColor(screenshot_cv, cv2.COLOR_RGB2GRAY)
        
        template = cv2.imread(CAMINHO_IMAGEM_ANCORA, 0)
        if template is None:
            raise FileNotFoundError(f"Imagem âncora não encontrada em {CAMINHO_IMAGEM_ANCORA}")

        template_h, template_w = template.shape

        res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(res >= 0.85)
        
        rects = []
        for pt in zip(*locations[::-1]):
            rects.append([int(pt[0]), int(pt[1]), template_w, template_h])

        rects, weights = cv2.groupRectangles(rects, 1, 0.2)
        
        if len(rects) == 0:
            return 0
        
        for (raw_x, raw_y, raw_w, raw_h) in rects:
            # Traduz as coordenadas físicas da captura para as lógicas da tela
            anchor_x = raw_x // ESCALA_TELA
            anchor_y = raw_y // ESCALA_TELA
            w = raw_w // ESCALA_TELA
            h = raw_h // ESCALA_TELA

            search_left = anchor_x + w
            search_top = anchor_y
            search_width = 300
            search_height = h
            
            screen_w, screen_h = pyautogui.size()
            if search_left >= screen_w or search_top >= screen_h:
                continue
            if search_left + search_width > screen_w:
                search_width = screen_w - search_left
            if search_width <= 10:
                continue

            search_area_img = pyautogui.screenshot(region=(search_left, search_top, search_width, search_height))
            
            ocr_img = search_area_img.convert('L')
            ocr_img = ocr_img.point(lambda p: 255 if p > 200 else 0)
            ocr_img = ImageOps.invert(ocr_img)

            ocr_text = pytesseract.image_to_string(ocr_img, config='--psm 7')

            for word in ocr_text.split():
                if '/' in word and word.replace('/', '').isdigit():
                    primeira_parte = word.split('/')[0]
                    numero_pixels = int("".join(filter(str.isdigit, primeira_parte)))
                    return numero_pixels
        
        return 0

    except Exception as e:
        print(f"❌ Erro no processo de encontrar e ler pixels: {e}")
        return 0
    
def cores_sao_proximas(cor1, cor2, tolerancia):
    """Verifica se duas cores RGB são suficientemente próximas com base na tolerância."""
    
    if cor1 is None or cor2 is None or cor2 == (249, 245, 241) or cor2 == (248, 244, 240) or cor2 == (248, 245, 241): return False
    distancia = math.sqrt(sum([(a - b) ** 2 for a, b in zip(cor1, cor2)]))
    return distancia < tolerancia

def encontrar_cor_mais_proxima(cor_alvo, paleta):
    """Encontra a cor mais próxima sem calcular a raiz quadrada, para maior eficiência."""
    return min(paleta.keys(), key=lambda cor: sum((a - b) ** 2 for a, b in zip(cor_alvo, cor)))

def mecanismo_de_correção_de_pixels(dim_original, dim_pixel, dim_pixel_completa):
    """Calcula correção de pixels da imagem original para a imagem redimensionada."""

    porcentagem_percorrida = dim_pixel / dim_pixel_completa
    cor = (dim_original - ESCALA_DE_PIXELS * dim_pixel_completa) * porcentagem_percorrida

    return cor

def execute_tabs_cycle(j):

    # Para focar na janela, e ter certeza que nenhum pixel está clicado
    time.sleep(0.5)
    pyautogui.moveTo(214, 423)
    time.sleep(0.5)
    pyautogui.click(214, 423)
    time.sleep(1)
    print("⌨️ Pressionando a tecla ESC...")
    pyautogui.press('esc')
    time.sleep(1)

    k = 0

    if (j == 0):
        return

    if (j % (NUMERO_DE_CONTAS * 2) > (NUMERO_DE_CONTAS - 1)):
        k = 1

    if (j % NUMERO_DE_CONTAS == 0):
        print(f"Terminamos ciclo n˚{j // NUMERO_DE_CONTAS}")
        playWinSound()
        time.sleep(20)

    """Executa o ciclo de troca de abas."""
    print("Pressionando Ctrl + Command + F")
    pyautogui.hotkey('ctrl', 'command', 'f')
    pyautogui.hotkey('ctrl', 'command', 'f')

    time.sleep(2)
    for z in range(abs(j % NUMERO_DE_CONTAS - k * NUMERO_DE_CONTAS)):
        print("Pressionando Command + `")
        pyautogui.hotkey('command', '`')
        time.sleep(0.5)

    print("Pressionando Ctrl + Command + F")
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'command', 'f')
    pyautogui.hotkey('ctrl', 'command', 'f')
    time.sleep(2)


def playWinSound():
    # The sound will play and the script will block until it is finished
    playsound('sounds/winmusic.mp3')