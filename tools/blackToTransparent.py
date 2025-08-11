from PIL import Image

def substituir_preto_por_transparente(imagem_path, output_path):
     """
     Substitui a cor preta por transparente em uma imagem.

     :param imagem_path: Caminho para o arquivo de imagem de entrada.
     :param output_path: Caminho para salvar a imagem de saída com transparência.
     """
     try:
         # Abre a imagem e garante que ela esteja no modo RGBA (para ter canal alfa)
         img = Image.open(imagem_path).convert("RGBA")
         datas = img.getdata()

         nova_data = []
         for item in datas:
             # Verifica se o pixel é preto (RGB: 0, 0, 0)
             if item[:3] == (0, 0, 0):
                 # Se for preto, torna-o totalmente transparente (RGBA: 0, 0, 0, 0)
                 nova_data.append((0, 0, 0, 0))
             else:
                 # Caso contrário, mantém a cor original
                 nova_data.append(item)

         # Cria uma nova imagem com os dados modificados
         img.putdata(nova_data)

         # Salva a imagem no formato PNG (que suporta transparência)
         img.save(output_path, "PNG")

         print(f"✅ Cor preta substituída por transparente em '{imagem_path}' e salva em '{output_path}'.")

     except FileNotFoundError:
         print(f"❌ Erro: O arquivo '{imagem_path}' não foi encontrado.")
     except Exception as e:
         print(f"❌ Um erro inesperado ocorreu: {e}")

# --- Como usar ---
if __name__ == '__main__':
     input_image = 'output.png'  # Substitua pelo caminho da sua imagem
     output_image = 'transparente_output.png'

     substituir_preto_por_transparente(input_image, output_image)