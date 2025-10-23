# tools/teste.py

import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import pyautogui
from PIL import Image
import time

from configs.sceptile_config import PONTO_DE_ORIGEM_MAPA, CAMINHO_IMAGEM_A_PINTAR

# Para telas Retina de MacBook, o fator de escala de pixels físicos é 2.
ESCALA_TELA = 2

print("Iniciando teste de captura com a nova estratégia (tela inteira + recorte)...")
time.sleep(3)

try:
    caminho_completo_gabarito = os.path.join(project_root, CAMINHO_IMAGEM_A_PINTAR)
    imagem_gabarito = Image.open(caminho_completo_gabarito)
    w_logico, h_logico = imagem_gabarito.size
    x_logico, y_logico = PONTO_DE_ORIGEM_MAPA

    print(f"Dimensões lógicas do gabarito (w, h): ({w_logico}, {h_logico})")
    print(f"Ponto de origem lógico (x, y): ({x_logico}, {y_logico})")

    # --- PASSO 1: Capturar a tela INTEIRA ---
    print("\nCapturando a tela inteira...")
    screenshot_tela_inteira = pyautogui.screenshot()
    print(f"Dimensões da tela inteira (em pixels): {screenshot_tela_inteira.size}")

    # --- PASSO 2: Calcular a área de recorte em PIXELS FÍSICOS ---
    left = x_logico * ESCALA_TELA
    top = y_logico * ESCALA_TELA
    right = (left + w_logico)
    bottom = (top + h_logico)
    
    # ==============================================================================
    # CORREÇÃO DO ERRO DE DIGITAÇÃO ESTÁ AQUI:
    area_de_recorte = (left, top, right, bottom)
    # ==============================================================================
    
    print(f"Área de recorte calculada (em pixels): {area_de_recorte}")

    # --- PASSO 3: Recortar a imagem com o Pillow ---
    print("Recortando a região de interesse...")
    imagem_recortada = screenshot_tela_inteira.crop(area_de_recorte)
    
    w_real, h_real = imagem_recortada.size
    print(f"Dimensões REAIS da imagem recortada (w, h): ({w_real}, {h_real})")
    print(f"As dimensões reais devem ser ({w_logico * ESCALA_TELA}, {h_logico * ESCALA_TELA})")

    caminho_saida = os.path.join(os.path.dirname(__file__), 'captura_bruta_teste.png')
    imagem_recortada.save(caminho_saida)

    print(f"\nTeste concluído! A nova imagem foi salva como '{caminho_saida}'")
    print("Verifique se a imagem NÃO está mais achatada.")

except Exception as e:
    print(f"Ocorreu um erro durante o teste: {e}")