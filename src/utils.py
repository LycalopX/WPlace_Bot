
import math
from src.config import *
import pyautogui
import time

# ==============================================================================
# =========================== FUNÇÕES AUXILIARES ===============================
# ==============================================================================

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
    print(f"Porcentagem percorrida: {porcentagem_percorrida:.2f}")
    cor = (dim_original - ESCALA_DE_PIXELS * dim_pixel_completa) * porcentagem_percorrida
    print(f"Cor corrigida: {cor:.2f}")

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
        time.sleep(10)

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