__author__ = 'Felipe'
#**********************************#
###           CLASSES            ###
#**********************************#
from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from random import *
from PPlay.collision import *
from time import time

#**********************************#
### FUNÇÕES(em ordem alfabética) ###
#**********************************#
def arrasta_peca(peca,click,mouse):
    """Função que arrasta a peça até a posição desejada"""
    # Guarda as coordenadas(x,y) do mouse no formato de vetor, posicao_mouse = [x,y]
    posicao_mouse = mouse.get_position()
    # Parar de arrastar a peça no cursor
    if mouse.is_button_pressed(2) and posicao_mouse[1]<600:
        click[0] = False
    # Para atualizar a peça junto ao cursor do mouse
    if click[0] == True:
        posx = posicao_mouse[0] - peca.width/2
        posy = posicao_mouse[1] - peca.height/2
        peca.x = posx
        peca.y = posy
        peca.draw()

def check_win_or_lose(barra_movel,barra,waves,conta_win,tempo_wave):
    """checa quando ocorre vitória ou derrota"""
    global GAME_STATE
    win = False
    lose = False
    # Quando o tempo de jogo acabar, se tiver peça parada por colisão dupla na borda, mova a peça
    if barra_movel.x+barra_movel.width >= barra.x+barra.width:
        barra_movel.x = barra.x+barra.width
        for linha in range(len(waves)):
            for pos in range(len(waves[linha])):
                if waves[linha][pos]!=0 and waves[linha][pos].x>=janela.width:
                    # .check_colision = checa se a peça está colidindo ( 0 = OFF , 1 = ON)
                    waves[linha][pos].check_colision = 0

        # Cria todas as waves restantes quando acaba o tempo
        for i in range(len(tempo_wave)):
            tempo_wave[i] = 0

        # Checa se algum monstro ainda está vivo quando acaba o tempo, e muda a win condition
        for num_wave in range(len(waves)):
            win = True
            for pos in range(len(waves[num_wave])):
                if waves[num_wave][pos] != 0:
                    win = False

    # Se algum monstro passar da barreira o player perde
    for num_wave in range(len(waves)):
            for pos in range(len(waves[num_wave])):
                if waves[num_wave][pos]!=0:
                    if waves[num_wave][pos].x + waves[num_wave][pos].width  < 0:
                        lose = True
    # O número de waves  - número de vitórias(conta_win) = número de waves inicial(linha 5
    if numero_waves - conta_win[0] == 2:
        # Se todos os monstros forem destruídos o player vence
        for num_wave in range(len(waves)):
            win = True
            for pos in range(len(waves[num_wave])):
                if waves[num_wave][pos] != 0:
                    win = False
    # Muda o estado do jogo
    if lose == True:
        #GAME OVER
        GAME_STATE = 3
        conta_win[0] = 0
    elif win == True:
        #FASE SEGUINTE
        GAME_STATE = 2
        conta_win[0] += 1

def colide_Bala_Monster(bala,matrizmonstro,Score):
    """Realiza a colisão entre os tiros do player e o Monstro"""
    if (len(matrizmonstro)) > 0:
        for wave in range(len(matrizmonstro)):
            for linha in range (len(matrizmonstro[wave])):
                for posicaonalinha in range(len(bala[0])):

                    if matrizmonstro[wave][linha] != 0 and bala[linha][posicaonalinha] !=0:
                        # Checa a colisão e tira a vida do monstro
                        if Collision.collided_perfect(matrizmonstro[wave][linha],bala[linha][posicaonalinha]):
                            matrizmonstro[wave][linha].vida = matrizmonstro[wave][linha].vida - bala[linha][posicaonalinha].dano
                            bala[linha][posicaonalinha] = 0
                            # Destrói o monstro e aumenta o score do player
                            if matrizmonstro[wave][linha].vida < 0:
                                matrizmonstro[wave][linha] = 0
                                Score[0] += 20

def colide_PxM(matrizplayer,matrizmonstro,Score):
    """Realiza a colisão da peça do player com o monstro criado na matrizmonstro"""
    if (len(matrizmonstro)) > 0:
        for wave in range(len(matrizmonstro)):
            for linha in range (len(matrizmonstro[wave])):
                for posicaonalinha in range(len(matrizplayer[0])):
                    if matrizmonstro[wave][linha] != 0 and matrizplayer[linha][posicaonalinha] !=0:
                        # Checa a colisão e tira vida do player e do monstro(caso a peça da colisão tenha ataque a curta distância)
                        if Collision.collided_perfect(matrizmonstro[wave][linha],matrizplayer[linha][posicaonalinha]):
                            if matrizmonstro[wave][linha].x > matrizplayer[linha][posicaonalinha].x+Sprite("Soldier1.png").width/3:
                                matrizmonstro[wave][linha].vida -=  matrizplayer[linha][posicaonalinha].dano
                                matrizplayer[linha][posicaonalinha].vida -=  matrizmonstro[wave][linha].dano
                                matrizmonstro[wave][linha].check_colision = 1
                                #Checa se o monstro morreu
                                if matrizmonstro[wave][linha].vida <= 0:
                                    matrizmonstro[wave][linha] = 0
                                    Score[0] += 20
                                #Checa se a peça do player foi destruída
                                if matrizplayer[linha][posicaonalinha].vida <= 0:
                                    matrizplayer[linha][posicaonalinha] = 0
                                    matrizmonstro[wave][linha].check_colision = 0
                                    #Quando ocorre colisão dula chamamos a função move_parado para não dar bug
                                    move_parado(matrizmonstro)

def colide_MvsWall(monstro,wall):
    """Colisão do Monstro com a barreira quadrada"""
    if len(monstro) > 0:
        for linha in range(len(monstro)):
            for wave in range(len(monstro[0])):
                for colun in range(5):
                    if monstro[linha][wave]!=0 and wall[colun]!=0:
                        if Collision.collided_perfect(monstro[linha][wave],wall[colun]):
                            if monstro[linha][wave].x <= 120:
                                wall[colun].vida -= monstro[linha][wave].dano
                                monstro[linha][wave].x = 120
                            # Checa se a barreira foi destruída
                            if wall[colun].vida <= 0:
                                wall[colun] = 0
                                # Ao ser destruída a barreira mata o monstro que a destruiu
                                monstro[linha][wave] = 0


def controlador_tiro(controlatiro,Mbullets):
    """Controla a frequência de tiro do player"""
    for i in range (len(Mbullets)):
        for j in range(len(controlatiro[i])):
            if Mbullets[i][j] !=0 or controlatiro[i][j]>0:
                aux = controlatiro[i][j]
                controlatiro[i][j] = aux + janela.delta_time()
                if controlatiro[i][j] >= 3:
                    controlatiro[i][j] = 0

def cria_player(mouse,matriz,peca_click,contaclick,custo_peca):
    """Cria a peça do jogador no mapa"""
    global recurso
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            # Ativado quando o mouse clica na peça do menu
            if mouse.is_over_object(peca1) and mouse.is_button_pressed(1):
                #Se peça do menu for clickada esse parêmentro recebe TRUE
                peca_click[0] = True
            # Para não ficar clickando infinitamente e contar apenas 1 click
            if peca_click[0] == True and not mouse.is_button_pressed(1):
                contaclick[0] = 1
            # Guarda o vetor posição do mouse
            pos_mouse = mouse.get_position()
            # Quando clica no quadrado vazio, cria a peça
            if mouse.is_button_pressed(1) and peca_click[0] == True and pos_mouse[1]<600 and contaclick[0]==1 and recurso >= custo_peca:
                pos = mouse.get_position()
                posx = pos[0]
                posy = pos[1]
                # a e b recebem a coordenada do quadrado(Dimensão do quadrado 120x120);Ex.:quadrado (a=0,b=0), é o primeiro quadrado
                a = posx//120
                b = posy//120
                # Se o quadrado estiver vazio criamos a peça e resetamos as variáveis que controlam o click do mouse
                if matriz[b][a] == 0:
                    contaclick[0] = 0
                    peca_click[0] = False
                    peca = Sprite("Soldier111.png")
                    # Posição da peça no tabuleiro
                    peca.x =  a * 120
                    peca.y =  b * 120
                    # Atributo que controla quanto de dano a peça pode levar
                    peca.vida = 1500
                    # Dano que a peça causa
                    peca.dano = 0
                    # custo da peça
                    peca.custo = custo_peca
                    matriz[b][a] = peca
                    # Diminui o custo da peça dos recursos do jogador
                    recurso = recurso - custo_peca
            # Comando para destruir a peça
            if mouse.is_button_pressed(3) and pos_mouse[1]<600:
                contaclick[0] = 0
                pos = mouse.get_position()
                posx = pos[0]
                posy = pos[1]
                a = posx//120
                b = posy//120
                # Se destruir a peça o jogador recebe parte do recurso gasto de volta
                if matriz[b][a] !=0:
                    recurso = recurso + int(custo_peca/4)
                    matriz[b][a] = 0

def cria_tiro_player(Mbullet, Matrizplayer,controlatiro):
    """Cria os tiros do jogador"""
    for linha in range(len(Matrizplayer)):
        for poslinha in range(len(Matrizplayer[linha])):
            # A criação de tiro depende da matrizplayer e do controlador de tempo de tiro
            if Matrizplayer[linha][poslinha] != 0 and Mbullet[linha][poslinha] == 0 and (controlatiro[linha][poslinha]==0 or controlatiro[linha][poslinha] > 3):
                bala = Sprite("bala.png")
                bala.x = Matrizplayer[linha][poslinha].x + Matrizplayer[linha][poslinha].width - bala.width #Posição e largura do Sprite
                bala.y = Matrizplayer[linha][poslinha].y + Matrizplayer[linha][poslinha].height/3 - bala.height
                #Quantidade de vida que a bala tira ao colidir
                bala.dano = 80
                Mbullet[linha][poslinha] = bala
                # Reseta o controlador de tempo do tiro
                if controlatiro[linha][poslinha] > 3:
                    controlatiro[linha][poslinha] = 0

def cria_wall(wall):
    """cria as barreiras"""
    for i in range(5):
            npc = Sprite("barreira quadrada.png")
            npc.x = 0
            npc.y = 120 * i
            npc.vida = 2000
            npc.dano = 0
            wall.append(npc)

def delay_entre_waves(tempo,numerowaves):
    """Controla a criação dos monstros até o fim da barra de tempo"""
    timer = 0
    for i in range(numerowaves):
        if len(tempo)<numerowaves:
            timer += randint(10,20)
            if (len(tempo)) == 0:
                timer = 0
            tempo.append(timer)

def desenha_player(matriz):
    """desenha as peças do player contidas no parâmeto matriz"""
    for i in range(len(matriz)):
        for j in range (len(matriz[i])):
            if matriz[i][j]!=0:
                matriz[i][j].draw()

def desenha_tiro(Tiro):
    """desenha os tiros da peça do player"""
    if len(Tiro) > 0:
        for i in range(len(Tiro)):
            for j in range(len(Tiro[i])):
                if Tiro[i][j]!= 0 :
                    Tiro[i][j].draw()

def desenha_wall(wall):
    """desenha as barreiras"""
    for i in range(5):
        if wall[i]!=0:
            if wall[i].vida < 1000:
                aux = Sprite("barreira com dano.png")
                aux.x = wall[i].x
                aux.y = wall[i].y
                aux.vida = wall[i].vida
                wall[i] = aux
            wall[i].draw()

def desenha_wave(wave):
    """desenha os monstros"""
    if len(wave) > 0:
        for i in range(len(wave)):
            # O limite é a altura da coluna de quadrados (5)
            for j in range(5):
                if wave[i][j] != 0:
                    wave[i][j].draw()
                    wave[i][j].update()

def enemy_spawn(wave,linha,tempo_entre_waves,contador_tempo,jacriouwave,numerowaves,life_monster):
  """Cria os Inimigos"""
  for k in range(numerowaves):
    # Aguarda o controlador de tempo para criar as waves
    if contador_tempo[0] >= tempo_entre_waves[k] and jacriouwave[k] == False:
        # controla quais posições da coluna poderão ter monstro criado
        aux = linha[k]
        enemy_matrix = []
        for i in range(5):
            enemy = Sprite("Alien1.png")
            enemy.set_total_duration(1000)  # duração em milissegundos
            enemy.x = janela.width + randint(10*i,10*i**2)
            enemy.y = 120 * i
            enemy.vida = life_monster
            enemy.dano = 5
            enemy.check_colision = 0 # 0 para Desligado == 1 para Ligado ( Checa se esta colidando ou não)
            # somente cria o monstro se a linha[i] for == 1, se for diferente recebe 0 e não cria nada
            if aux[i] == 1:
                enemy_matrix.append(enemy)
            else:
                enemy_matrix.append(aux[i])
        wave.append(enemy_matrix)
        # Controlamos a criação das ondas de monstros para não ficarem ondas duplicadas
        jacriouwave[k] = True

def move_bala(Mbullet,Matrizplayer):
    """movimenta os tiros do jogador"""
    if len(Mbullet)>0:
        for i in range (len(Mbullet)):
            for j in range(len(Mbullet[i])):
                if Mbullet[i][j]!=0:
                    Mbullet[i][j].move_x(5 * GAME_SPEED * janela.delta_time())
                    if Mbullet[i][j].x > janela.width:
                        Mbullet[i][j] = 0

def monster_por_wave(quantidade_inicial,numero_waves):
    """Define o fomato das waves e guarda em linha = []"""
    aux = []
    aumenta_monstros = 1
    coluna_de_monstros = 0
    formato_wave = []
    # Para variar quantos monstros serão criados por vez
    for monstro_por_linha in range(numero_waves):
        aumenta_monstros += 1
        if aumenta_monstros >= (5):
            aumenta_monstros = randint(1,5)

        coluna_de_monstros = aumenta_monstros * quantidade_inicial
        # Limita o número máximo de monstros a 5
        if coluna_de_monstros > 5:
            coluna_de_monstros = 5
        # append 1 para criar o monstro e 0 para espaço vazio
        for linha in range(coluna_de_monstros):
            aux.append(1)
        # Se o vetor auxiliar ficar menor que 5 preencha com espaço vazio (0)
        while len(aux) < 5:
            aux.append(0)
        random_aux = []

        # Embaralha o vetor aux = [xxxxxx], para não ficar sempre na mesma ordem o formato das ondas de monstro
        for i in range(5):
            pega_random = randint(0,len(aux)-1)
            random_aux.append(aux[pega_random])
            aux.pop(pega_random)
        formato_wave.append(random_aux)
    return formato_wave

def move_barra(tempo,movebarra,geradorrecurso,tempo_execucao):
    """Movimenta a barra móvel(barrinha vermelha) da barra de tempo"""
    global recurso
    if tempo_execucao[0] <= tempo[0]:
        # Controla a velocidade com que a barra se movimenta
        movebarra[0] += 0.25
        barramovel.x = timebar.x - barramovel.width + movebarra[0]
        # Congela a barra quando ela chega ao fim
        if barramovel.x + barramovel.width >= timebar.x+timebar.width:
            barramovel.x = timebar.x + timebar.width - barramovel.width
        # Aumenta o recurso do jogador ao passar o tempo ( ~a cada 5 segundos)
        if tempo[0] == geradorrecurso[0]:
            recurso += 25
            geradorrecurso[0] += 5

def move_parado(matriz_monstro):
    """Quando ocorre colisão com mais de 1 objeto"""
    if len(matriz_monstro) > 1:
        for l in range(len(matriz_monstro)):
            for pos in range(len(matriz_monstro[l])):
                if matriz_monstro[l][pos] !=0:
                    if matriz_monstro[l][pos].check_colision == 1:
                        matriz_monstro[l][pos].check_colision = 0

def move_enemy_wave(wave):
    """Movimenta os inimigos"""
    if len(wave) > 0:
        for i in range(len(wave)):
            for j in range(len(wave[i])):
                if wave[i][j] != 0 and wave[i][j].check_colision == 0:
                    wave[i][j].move_x(-0.5 * GAME_SPEED * janela.delta_time())

def restart(conta_win):
    """Reseta todas as váriáveis iniciais do jogo para mudança de fase"""
    global GAME_STATE
    global qtd_inicial_monstros
    global numero_waves
    global matriz_peca1
    global tempo
    global jacriouwave
    global monstros_fase1
    global bala_peca1
    global limitador_tiro
    global contador_tempo
    global contaclick
    global click_peca1
    global movebarra
    global qtd_inicial_monstros
    global recurso
    global tempo_wave_monstro
    global linha
    global geradorrecurso
    global tempo_execucao
    global wall
    global life_inicial
    life_inicial += 10
    tempo_execucao = [2]
    linha = []
    tempo_wave_monstro = []
    numero_waves += 1
    monstros_fase1 = []
    jacriouwave = [False] * numero_waves
    tempo = []
    matriz_peca1 = [[0 for x in range(16)] for x in range(8)]
    bala_peca1 = [[0 for x in range(16)] for x in range(8)]
    limitador_tiro = [[0 for y in range(16)] for y in range(8)]
    wall = []
    contador_tempo = [0]
    geradorrecurso = [7]
    contaclick = [0]
    click_peca1 = [False]
    barramovel.set_position(timebar.x - barramovel.width,timebar.y)
    recurso = 100
    movebarra = [0]

    qtd_inicial_monstros += conta_win[0]
    if qtd_inicial_monstros >= 3:
        qtd_inicial_monstros = randint(1,3)
    # Fase Seguinte
    if GAME_STATE !=3:
        GAME_STATE = 1
        janela.set_background_color([0,0,0])
        janela.draw_text("VICTORY !!!!",janela.width/2 - 50,janela.height/2,36,(255,255,255),"Calibri", True)
        janela.update()
        janela.delay(1000)
        janela.set_background_color([0,0,0])
        janela.update()
        janela.draw_text("Fase "+str(conta_win[0]+1),janela.width/2 - 50,janela.height/2 ,36,(255,255,255),"Calibri", True)
        janela.update()
        janela.delay(1000)
    # GAME OVER
    else:
       janela.set_background_color([0,0,0])
       janela.update()
       nome = 0
       nome = str(input("Nome do Jogador: "))
       janela.delay(5000)
       if nome == 0:
           janela.delay(5000)
       if nome == 0:
           janela.delay(5000)
       numero_waves = 5
       janela.set_background_color([0,0,0])
       janela.draw_text("GAME OVER",janela.width/2-50,janela.height/2+50,36,(255,255,255),"Calibri", True)
       janela.draw_text("Final Score ="+str(score)+" <> "+nome,peca1.x+3*peca1.width,janela.height - peca1.width/2,24,(255,255,255),"Calibri", True)
       arq = open("Score.txt","a")
       arq.write(nome)
       arq.write(" - ")
       arq.write(str(score[0]))
       arq.write("\n")
       arq.close()
       janela.update()
       janela.delay(3000)
       GAME_STATE = 0
       numero_waves = randint(1,3)

def tela_inicial(conta_win):
        """Cria a tela inicial do jogo"""
        global GAME_STATE
        tela = True
        telainicial.draw()
        janela.draw_text("@ Jorge Chagas &  Lucas Santana",janela.width-250,janela.height-50,16,(255,255,255),"Calibri", True)
        janela.update()
        if teclado.key_pressed("enter"):
            tela = False
        janela.update()
        janela.delay(10)

        if tela == False:
            fica_no_tutorial = True
            while fica_no_tutorial == True:
                tutorial.draw()
                janela.update()
                if teclado.key_pressed("esc"):
                    fica_no_tutorial = False

            janela.set_background_color([0,0,0])
            janela.draw_text(" FASE "+str(conta_win[0] + 1),janela.width/2-50,janela.height/2,36,(255,255,255),"Calibri", True)
            janela.update()
            janela.delay(2000)
            GAME_STATE = 1

def timer(contador_tempo,tempo_execucao):
    """Conta o tempo de jogo"""
    if tempo_execucao[0] > contador_tempo[0]:
        contador_tempo[0] += 1

def tiro_colide(Mbullet,wave):
    """Colisão  do tiro com o monstro"""
    if len(Mbullet) > 0 and len(wave) > 0:
        for linha in range(len(Mbullet)):
            for poslinha in range(len(Mbullet)):
                for num_wave in range(len(wave)):
                    for linhawave in range(len(wave[num_wave])):
                        if Mbullet[linha][poslinha]!=0 and wave[num_wave][linhawave] !=0:
                            #Quando a bala colide ela causa dano no monstro
                            if Mbullet[linha][poslinha].collided(wave[num_wave][linhawave]):
                                wave[num_wave][linhawave].vida = wave[num_wave][linhawave].vida - Mbullet[linha][poslinha].dano
                                Mbullet[linha][poslinha] = 0 #(Destrói a bala)
                                # Destrói o monstro
                                if wave[num_wave][linhawave].vida <= 0:
                                    wave[num_wave][linhawave] = 0

#**********************************#
###      VARIAVEIS DO JOGO       ###
#**********************************#

##---- CONTROLADORES DO JOGO ----##
#---------------------------------#
#conta quantos segundos se passaram aproximadamente
contador_tempo = [0]
tempo_execucao = [2]

# acumulador que aumenta a quantidade de recursos do player
geradorrecurso = [7]

# Controla em qual o estado o jogo se encontra ( WIN, LOSE, FASE )
GAME_STATE = 0

# Controla a velociade do Jogo
GAME_SPEED = 50

# Conta o número de vitórias seguidas do player
conta_win = [0]

#Pontuação
score = [0]

##---- CRIA JANELA ----##
#-----------------------#
largura_janela = 960
altura_janela = 720
janela = Window(largura_janela,altura_janela)
title = "Alien Invaders"
janela.set_title(title)

##---- ELEMENTOS DA INTERFACE ----##
#----------------------------------#
#Teclado
teclado = Window.get_keyboard()
# Cursor que aparece na tela e executa as ações do player
mouse = Window.get_mouse()
# Responsável por contar quando um click for realizado numa peça do menu
contaclick = [0]
# Responsável por informar quando o click na peça do menu for ativado
click_peca1 = [False]
#====> As variáveis click_peca e contaclick estão responsáveis por contar somente 1 click, pois com o comando para checar
# se o botão do mouse foi clicado pegar somente 1 click, sem esse controle vários clicks são registrados

# Peça que fica no menu inferior esquerdo da tela
peca1 = Sprite("Soldier1.png")
peca1.set_position(0,janela.height - peca1.height)
# Sprite da peça que fica junto ao cursos
peca1_no_cursor = Sprite("Soldier1.png")

# Quantidade de recurso que o player começa, fica no menu inferior
recurso = 100

# Barra que controla o tempo restante do jogo
timebar = GameImage("Timebar.png")
timebar.set_position(janela.width - timebar.width - 3, janela.height - timebar.height - 3)
barramovel = Sprite("barramovel.png") # Barra vermelha que percorre a timebar
barramovel.set_position(timebar.x - barramovel.width,timebar.y)
# Contador responsável por mudar a posição x da barra de tempo
movebarra = [0]

#===================#
#-- MAPAS E TELAS --#

# Define a fase que será chamada, default fase1
mapa = GameImage("Mapa1.png")

# A tela inicial do jogo
telainicial = GameImage("tela_inicial.jpg")

# Tela Tuturial
tutorial = GameImage("Tutorial.jpg")

##---- INIMIGO ----##
#-------------------#
#define o número de waves na fase
numero_waves = 2
#matriz(es) que vão receber os monstros da respectiva fase
monstros_fase1 = []
# Informa se a wave já foi criada, para não gerar mancha no mapa
jacriouwave = [False] * numero_waves
# Matriz que guardará o  tempo entre cada wave de monstros
tempo_wave_monstro = []
#Define como será a compsição de cada wave, e a linha receberá [0] = vazio [1] = crir monstro
qtd_inicial_monstros = 1
life_inicial = 200

##---- JOGADOR ----##
#-------------------#

# Matriz(es) que recebe(m) as peças
matriz_peca1 = [[0 for x in range(16)] for x in range(8)]
# Matriz responsável pelo tiro e a matriz que controla o tiro
bala_peca1 = [[0 for x in range(16)] for x in range(8)]
limitador_tiro = [[0 for y in range(16)] for y in range(8)]
peca1_custo = 40
arrastando = [False]

# Salva o nome do Jogador
nome_do_jogador = [0]
#Matriz da Barreira Final
wall = []

#**********************************#
###=========== O JOGO ===========###
#**********************************#

while True :
    #-- Define o formato das waves --#
    linha = monster_por_wave(qtd_inicial_monstros,numero_waves)
    #-- Controla o tempo em que os monstros serão criados --##
    delay_entre_waves(tempo_wave_monstro,numero_waves)

    #------------------------#
    ##---- TELA INICIAL ----##
    #------------------------#
    if GAME_STATE == 0:
        while GAME_STATE ==0:
            tela_inicial(conta_win)

    #------------------------#
    ##---- INICIA O JOGO ----#
    #------------------------#
    elif GAME_STATE == 1:
        while GAME_STATE == 1:

            ##---- LÓGICA DO JOGO ----##
            #--------------------------#

            #-- Atualizar o tempo do jogo --#
            tempo_execucao[0] += janela.delta_time()
            timer(contador_tempo,tempo_execucao)

            #-- Mover a barra de tempo --#
            move_barra(contador_tempo,movebarra,geradorrecurso,tempo_execucao)

            #-- Criar os inimigos --#
            enemy_spawn(monstros_fase1,linha,tempo_wave_monstro,contador_tempo,jacriouwave,numero_waves,life_inicial)

            #-- Criar as peças do player --#
            # Peça
            cria_player(mouse,matriz_peca1,click_peca1,contaclick,peca1_custo)
            # Tiro da Peça(Quando houver)
            cria_tiro_player(bala_peca1,matriz_peca1,limitador_tiro)
            #Cria as barreiras
            cria_wall(wall)

            ##-- Movimento dos Objetos --##
            move_enemy_wave(monstros_fase1)
            move_bala(bala_peca1,matriz_peca1)
            # controla a cadência das balas
            controlador_tiro(limitador_tiro,bala_peca1)

            ##-- Colisões dos Objetos --##
            colide_PxM(matriz_peca1,monstros_fase1,score)

            colide_Bala_Monster(bala_peca1,monstros_fase1,score)

            colide_MvsWall(monstros_fase1,wall)

            ##-- Checha se ocorreu vitória ou derrota
            check_win_or_lose(barramovel,timebar,monstros_fase1,conta_win,tempo_wave_monstro)

            #-- RENDER --#
            #------------#
            # Desenha o mapa da fase
            mapa.draw()

            # Desenha os monstros
            desenha_wave(monstros_fase1)
            #Desenha as barreiras
            desenha_wall(wall)
            # Desenha a(s) peça(s) do menu no cursor quando clicada(s)
            arrasta_peca(peca1_no_cursor,click_peca1,mouse)
            # Desenha a(s) peça(s) do Menu
            peca1.draw()

            # Desenha o player e o tiro
            desenha_player(matriz_peca1)
            desenha_tiro(bala_peca1)


            # Desenha a barra e a barrinha móvel que anda na barra de tempo
            timebar.draw()
            barramovel.draw()

            # Informa o custo da peça e a quantidade de recurso do jogador na tela
            janela.draw_text("  Minério[$"+str(recurso)+"]",peca1.x+peca1.width,janela.height - peca1.width/2,26,(255,255,255),"Calibri", True)
            janela.draw_text("SOLDIER [$40]",peca1.x,peca1.y-18,18,(255,255,255),"Calibri", True)
            janela.draw_text("Score"+str(score),peca1.x+5*peca1.width,janela.height - peca1.width/2,24,(255,255,255),"Calibri", True)
            #Atualiza a janela >>>
            janela.update()

    elif GAME_STATE == 2:
        restart(conta_win)

    elif GAME_STATE == 3:
        restart(conta_win)









