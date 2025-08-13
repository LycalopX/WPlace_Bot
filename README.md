Esse bot é feito para funcionar sob circunstancias extremamente específicas e não configuráveis naturalmente. 

## Para qualquer imagem:
1. Escolha uma imagem com um determinado número de pixels, e mantenha esse valor em mente
2. Faça essa imagem ficar o menor possível, com cada bloco sendo um determinado pixel nela. Um exemplo disso pode ser visto na pasta Imagens, para o conjunto sceptile ou mew, em que, a imagem com os pixels afiados é "resized", e a de tamanho normal deve ser aproximadamente 16 * 1.024 maior. Para satisfazer essas condições, use o programa "resize.py" em Wplace/tools.

> Comando:
python resize.py <nome> <proporção>

3. A parte mais difícil já foi feita. Agora, (essa parte é opcional), você pode tirar uma print da tela completa do seu PC, e escolher onde quer que a imagem "comece", mantendo em mente que pixels transparentes contam como parte da imagem no cálculo de coordenadas.
4. Vá na pasta configs, e crie sua nova config, mantendo em mente que os valores selecionados do template são os mais adequados, e que a forma como você calibra o bot dependerá de você.
5. Vá em Wplace/src/config.py, e mude sua config para o nome do arquivo que escolheu, na linha 7, `from configs.lucky_star import *` sendo um exemplo.
6. Escolha suas configurações adequadas em config.py, como número de contas, ou cooldown entre contas trocadas, mantendo em mente que a única coisa que o programa faz é mudar de janela.

## Para visualizar como vai ficar no jogo:
1. Escolha sua imagem, coloque na pasta tools, e rode cV.py com o nome do arquivo que quer visualizar.

> Comando:
python cV.py <nome>

## Para calibrar a posição das cores:
1. Tire uma print da sua tela completa, e apenas deixe as cores avulsas, como é possível ver em colors.png.
2. Rode findColor.py, ele vai te fornecer uma array das cores analizadas.
3. Substitua a array em findcolorpallete.py, ele vai te fornecer um objeto com as cores e suas respectivas posições na tela.
4. Coloque seu novo objeto em config.py! E agora o programa vai saber onde ficam as cores.

## Para calibrar a posição dos botões:
1. No Mac, use cmd + shift + 4, para abrir a captura de tela. Ela te fornece a posição de onde está mirando.

## Configurações de Múltiplas contas:
1. Abra em uma guia anonima do Chrome, ou em um perfil alternado uma outra conta no Wplace, e deixe no modo janela.
2. Quando iniciar o programa, a janela inicial deve estar no fullscreen.