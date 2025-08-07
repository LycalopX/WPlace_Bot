import pyautogui
import time
from PIL import Image
import math
import subprocess

# ==============================================================================
# ======================== CONFIGURAÇÃO PRINCIPAL DO BOT =======================
# ==============================================================================

# --- Configurações do Alvo ---
CAMINHO_IMAGEM_A_PINTAR = 'sceptile.png'
CAMINHO_IMAGEM_A_PINTAR_REDIMENSIONADA = 'resized_gabarito.png'
PONTO_DE_ORIGEM_MAPA = (609, 384) # Ponto (X, Y) do pixel do canto superior esquerdo da sua arte no mapa.

# --- Configurações do Jogo ---
PALETA_DE_CORES = {
    (0, 0, 0): (38, 749), (58, 127, 111): (1088, 734), (60, 60, 60): (68, 735),
    (120, 120, 120): (112, 735), (170, 170, 170): (156, 735), (210, 210, 210): (201, 735),
    (87, 13, 26): (290, 735), (151, 35, 37): (334, 735), (218, 56, 50): (378, 735),
    (234, 135, 119): (423, 735), (212, 101, 49): (467, 735), (239, 134, 64): (511, 735),
    (235, 173, 61): (556, 735), (244, 222, 93): (600, 735), (254, 250, 195): (645, 735),
    (152, 133, 63): (689, 735), (193, 174, 74): (733, 735), (229, 213, 113): (778, 735),
    (81, 106, 63): (822, 735), (103, 147, 83): (866, 735), (146, 195, 124): (911, 735),
    (85, 182, 112): (955, 735), (107, 227, 134): (1000, 735), (165, 252, 117): (1044, 735),
    (80, 171, 165): (1133, 735), (104, 222, 191): (1177, 735), (55, 119, 155): (1221, 735),
    (140, 244, 241): (1266, 735), (200, 248, 242): (1310, 735), (50, 79, 153): (1355, 735),
    (86, 145, 222): (1399, 735), (100, 113, 134): (182, 763), (254, 255, 255): (12, 765),
    (254, 254, 255): (13, 766), (110, 117, 139): (1307, 778), (142, 197, 250): (23, 779),
    (73, 50, 177): (68, 779), (103, 81, 237): (112, 779), (158, 176, 245): (156, 779),
    (73, 66, 128): (201, 779), (120, 113, 190): (245, 779), (180, 174, 236): (290, 779),
    (110, 25, 147): (334, 779), (157, 64, 179): (378, 779), (214, 162, 243): (423, 779),
    (186, 38, 120): (467, 779), (217, 57, 127): (511, 779), (229, 146, 169): (556, 779),
    (145, 86, 76): (600, 779), (198, 132, 123): (645, 779), (240, 185, 167): (689, 779),
    (99, 71, 55): (733, 779), (142, 106, 53): (778, 779), (211, 166, 109): (822, 779),
    (119, 100, 84): (866, 779), (152, 133, 110): (911, 779), (209, 182, 152): (955, 779),
    (198, 132, 90): (1000, 779), (238, 181, 128): (1044, 779), (246, 199, 170): (1088, 779),
    (107, 100, 68): (1133, 779), (204, 197, 162): (1221, 779), (52, 57, 64): (1266, 779),
}
BOTAO_ABRIR_PALETA_POS = (722, 845) # Coordenada fornecida na descrição

# --- Configurações do Bot ---
COOLDOWN_ENTRE_ACOES = 0.5
ESCALA_TELA = 2  # 2 para telas Retina de MacBook, 1 para telas normais.
ESCALA_DE_PIXELS = 16
TOLERANCIA_COR = 20 # Quão diferentes as cores podem ser para ainda serem consideradas "iguais".

# ==============================================================================
# =========================== FUNÇÕES AUXILIARES ===============================
# ==============================================================================

def cores_sao_proximas(cor1, cor2, tolerancia):
    """Verifica se duas cores RGB são suficientemente próximas com base na tolerância."""
    if cor1 is None or cor2 is None: return False
    distancia = math.sqrt(sum([(a - b) ** 2 for a, b in zip(cor1, cor2)]))
    return distancia < tolerancia

def encontrar_cor_mais_proxima(cor_alvo, paleta):
    """Encontra a cor mais próxima disponível na paleta do jogo."""
    return min(paleta.keys(), key=lambda cor: math.sqrt(sum([(a - b) ** 2 for a, b in zip(cor_alvo, cor)])))

def mecanismo_de_correção_de_pixels(dim_original, dim_pixel, dim_pixel_completa):
    """Calcula correção de pixels da imagem original para a imagem redimensionada."""

    porcentagem_percorrida = dim_pixel / dim_pixel_completa
    print(f"Porcentagem percorrida: {porcentagem_percorrida:.2f}")
    cor = (dim_original - 16 * dim_pixel_completa) * porcentagem_percorrida
    print(f"Cor corrigida: {cor:.2f}")

    return cor


# Lógica do bot

def encontrar_proximo_alvo(imagem_gabarito, imagem_gabarito_redimensionada, origem_mapa):
    
    x, y = origem_mapa
    w, h = imagem_gabarito.width // ESCALA_TELA, imagem_gabarito.height // ESCALA_TELA
    caminho_temp = "temp_screenshot.png"
    
    try:
        print(f"Capturando área de {w}x{h} pontos começando em ({x}, {y})...")
        subprocess.run(['screencapture', '-x', '-R', f'{x},{y},{w},{h}', caminho_temp], check=True)

    except Exception as e:
        print(f"❌ Erro ao usar 'screencapture': {e}")
        return None
    
    w = w // ESCALA_DE_PIXELS * ESCALA_TELA
    h = h // ESCALA_DE_PIXELS * ESCALA_TELA

    screenshot_jogo = Image.open(caminho_temp).convert('RGBA')
    screenshot_jogo_redimensionada = screenshot_jogo.resize((screenshot_jogo.width // ESCALA_DE_PIXELS, screenshot_jogo.height // ESCALA_DE_PIXELS), Image.Resampling.NEAREST)
    screenshot_jogo_redimensionada.save('screenshot_jogo_redimensionada.png')

    for y_rel in range(h):
        for x_rel in range(w):

            cor_gabarito_rgba = imagem_gabarito_redimensionada.getpixel((x_rel, y_rel))

            if cor_gabarito_rgba[3] < 255:
                continue
            
            cor_gabarito_rgb = cor_gabarito_rgba[:3]
            
            cor_ideal_na_paleta = encontrar_cor_mais_proxima(cor_gabarito_rgb, PALETA_DE_CORES)
            cor_atual_jogo_rgb = screenshot_jogo_redimensionada.getpixel((x_rel, y_rel))[:3]

            # 3. Compara a cor da tela com a cor ideal DA PALETA, não do gabarito.
            if not cores_sao_proximas(cor_ideal_na_paleta, cor_atual_jogo_rgb, TOLERANCIA_COR):
                print(f"🎯 Alvo encontrado em ({x_rel}, {y_rel}). Cor Gabarito: {cor_gabarito_rgb}, Cor na Tela: {cor_atual_jogo_rgb}")

                x_cor = mecanismo_de_correção_de_pixels(screenshot_jogo.width, x_rel, w)
                y_cor = mecanismo_de_correção_de_pixels(screenshot_jogo.height, y_rel, h)
                x_cor = x_cor - (x_cor % 1)
                y_cor = y_cor - (y_cor % 1)

                x_OG = (x_rel * ESCALA_DE_PIXELS + ESCALA_DE_PIXELS / 2) / 2 + x_cor
                y_OG = (y_rel * ESCALA_DE_PIXELS + ESCALA_DE_PIXELS / 2) / 2 + y_cor

                print(f"Coordenada corrigida: ({x_OG}, {y_OG})")
                print(f"Coordenada redimensionada: ({x_rel}, {y_rel})")

                return {'coord_arte': (x_OG, y_OG), 'cor_alvo': cor_gabarito_rgb}

    return None

def pintar_pixel(coord_arte, cor_alvo):
    """
    Encontra a cor na paleta e usa cliques humanizados para pintar o pixel no mapa,
    COM A LÓGICA DE COORDENADAS CORRIGIDA para telas Retina e gabaritos 2x.
    """
    cor_na_paleta = encontrar_cor_mais_proxima(cor_alvo, PALETA_DE_CORES)
    if not cor_na_paleta or cor_na_paleta not in PALETA_DE_CORES:
        return

    pos_cor_na_tela = PALETA_DE_CORES[cor_na_paleta]

    # ================== A CORREÇÃO FINAL ESTÁ AQUI ==================
    # Para garantir que o clique aconteça no CENTRO do pixel do jogo e não na borda,
    # adicionamos um pequeno deslocamento de meio "ponto".

    pos_mapa_na_tela = (
        PONTO_DE_ORIGEM_MAPA[0] + coord_arte[0],
        PONTO_DE_ORIGEM_MAPA[1] + coord_arte[1]
    )
    # =================================================================

    print(f"Corrigindo pixel em {pos_mapa_na_tela} para a cor {cor_alvo}...")
    try:
        # A sequência de cliques humanizados continua a mesma.
        pyautogui.click(BOTAO_ABRIR_PALETA_POS[0], BOTAO_ABRIR_PALETA_POS[1])
        time.sleep(0.2)

        pyautogui.click(pos_cor_na_tela[0], pos_cor_na_tela[1])
        time.sleep(0.2)

        pyautogui.click(pos_mapa_na_tela[0], pos_mapa_na_tela[1])
        time.sleep(0.2)

        pyautogui.click(BOTAO_ABRIR_PALETA_POS[0], BOTAO_ABRIR_PALETA_POS[1])
    except Exception as e:
        print(f"❌ Ocorreu um erro ao tentar pintar: {e}")

# ==============================================================================
# ============================ EXECUÇÃO DO BOT =================================
# ==============================================================================

if __name__ == "__main__":
    
    print("Carregando imagem gabarito...")
    try:
        imagem_gabarito = Image.open(CAMINHO_IMAGEM_A_PINTAR).convert('RGBA')
        imagem_gabarito_redimensionada = Image.open(CAMINHO_IMAGEM_A_PINTAR_REDIMENSIONADA).convert('RGBA')

    except FileNotFoundError:
        print(f"❌ ERRO FATAL: Imagem gabarito '{CAMINHO_IMAGEM_A_PINTAR}'/'{CAMINHO_IMAGEM_A_PINTAR_REDIMENSIONADA}' não encontrada.")
        exit()
        
    print(f"Gabarito '{CAMINHO_IMAGEM_A_PINTAR}' carregado ({imagem_gabarito.width}x{imagem_gabarito.height}).")
    print(">>> INICIANDO BOT CORRETOR EM 5 SEGUNDOS <<<")
    time.sleep(5)
    
    while True:        

        alvo = encontrar_proximo_alvo(imagem_gabarito, imagem_gabarito_redimensionada, PONTO_DE_ORIGEM_MAPA)
        if alvo is None:
            print("\n✅🎉====== DESENHO CONCLUÍDO E VERIFICADO! ======🎉✅")
            print("Aguardando 180 segundos antes de verificar novamente...")
            time.sleep(180)
            continue
        
        pintar_pixel(alvo['coord_arte'], alvo['cor_alvo'])
        
        print(f"Aguardando cooldown de {COOLDOWN_ENTRE_ACOES} segundos...")
        time.sleep(COOLDOWN_ENTRE_ACOES)