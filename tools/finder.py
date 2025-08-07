import pyautogui
from PIL import Image

# ==============================================================================
# ======================== CONFIGURAÇÃO DE VERIFICAÇÃO =======================
# ==============================================================================

# 1. Coloque a coordenada que você acredita estar correta.
PONTO_DE_ORIGEM_MAPA = (609, 383)

# 2. Coloque o nome da sua imagem gabarito para que o script saiba o tamanho da área.
CAMINHO_IMAGEM_A_PINTAR = 'sceptile.png'

# ==============================================================================

def verificar_area_desenho():
    """
    Desenha um retângulo na tela com o mouse para mostrar a área de pintura
    que o bot está usando, baseada nas suas configurações.
    """
    print(">>> INICIANDO VERIFICADOR DE ÁREA EM 3 SEGUNDOS <<<")
    print(">>>   DEIXE A JANELA DO JOGO VISÍVEL   <<<")
    time.sleep(3)

    try:
        imagem_gabarito = Image.open(CAMINHO_IMAGEM_A_PINTAR)
        largura, altura = imagem_gabarito.size
        print(f"Imagem gabarito '{CAMINHO_IMAGEM_A_PINTAR}' carregada. Dimensões: {largura}x{altura}.")
    except FileNotFoundError:
        print(f"❌ ERRO: Imagem '{CAMINHO_IMAGEM_A_PINTAR}' não encontrada.")
        return

    x_inicial, y_inicial = PONTO_DE_ORIGEM_MAPA
    
    # Calcula os 4 cantos do retângulo
    canto_superior_esquerdo = (x_inicial, y_inicial)
    canto_superior_direito = (x_inicial + largura, y_inicial)
    canto_inferior_direito = (x_inicial + largura, y_inicial + altura)
    canto_inferior_esquerdo = (x_inicial, y_inicial + altura)
    
    print("\nDesenhando o contorno da área de pintura com o mouse...")
    print(f"Canto superior esquerdo: {canto_superior_esquerdo}")
    
    # Desenha o retângulo lentamente
    pyautogui.moveTo(canto_superior_esquerdo[0], canto_superior_esquerdo[1], duration=0.5)
    pyautogui.moveTo(canto_superior_direito[0], canto_superior_direito[1], duration=0.5)
    pyautogui.moveTo(canto_inferior_direito[0], canto_inferior_direito[1], duration=0.5)
    pyautogui.moveTo(canto_inferior_esquerdo[0], canto_inferior_esquerdo[1], duration=0.5)
    pyautogui.moveTo(canto_superior_esquerdo[0], canto_superior_esquerdo[1], duration=0.5)
    
    print("\n✅ Verificação concluída. O contorno desenhado pelo mouse é a área que o bot usará.")
    print("Ajuste PONTO_DE_ORIGEM_MAPA até que o contorno se alinhe perfeitamente com a tela do jogo.")

if __name__ == "__main__":
    verificar_area_desenho()