#segunda tentativa de fazer esse bagulho dar certo
#IDEIAS
# - placa com panda desenhado
# - janela com vista de uma cutia com passaros
# - entregar uma pedra com um laço



#imports
import pygame
import time
import os





#funções
def save_existe():

    try:
        with open('save', 'r') as f:
            tem_save = True
            f.close()
    except:
            tem_save = False

    return tem_save

def loop_geral():
    
    clock.tick(fps_cap)
    event_buffer()
    sair()
    tela.blit(screen, screen_cords)
    pygame.display.flip()
    #print(int(clock.get_fps()))
    
def sair():

    sair_com_esc()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:            
            pygame.quit()
            quit()
            exit()

def guia_de_cenas(cena):

    if cena == 0:
        if save_existe():
            with open('save', 'r') as f:
                data = f.readlines()
                if data[0] == '00' or data[0] == '':
                    f.close()
                    return 1
                elif data[1] == '00':
                    return 2
        else:
            return 1
    elif cena == 1:
        criar_save()
        return 2    
    elif cena == 2:
        level_001()
        return 2

def criar_save():

    with open('save', 'w') as f:
        f.write('00')
        f.close()

    text = ''
    linha_digitação = True
    start = time.perf_counter()
    quebra = False
    while True:

        fonte_tamanho = fonte_padrao().get_height()

        posicao_do_texto = (screen.get_width()/4, screen.get_height()/3)

        draw_text(texto[0], posicao_do_texto[0], posicao_do_texto[1])

        for event in event_buffer_get():
            if event.type == pygame.TEXTINPUT:
                text += event.text
                linha_digitação = True
                start = time.perf_counter()
            elif event.type == pygame.KEYDOWN:
                if event.key in teclas_confirmar:
                    if text != '':
                        print('enter')
                        quebra = True
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                
        text_2 = text

        if linha_digitação: text_2 += '|'

        draw_text(text_2, posicao_do_texto[0], posicao_do_texto[1] + fonte_tamanho, menos_um=False)



        if time.perf_counter() - start >= 1.0:
            linha_digitação = not linha_digitação
            start = time.perf_counter()


        loop_geral()

        if quebra: break

    with open('save', 'w') as f:
        f.writelines([text, '\n00'])
        f.close()

def draw_text(texto, x, y, fonte = None, cor_do_texto = None, menos_um = None):

    if fonte == None: fonte = fonte_padrao()
    if cor_do_texto == None: cor_do_texto = (255, 255, 255)
    if menos_um != False: texto = texto [:-1]

    img = fonte.render(texto, True, cor_do_texto)
    screen.blit(img, (x, y))

def fonte_padrao():

    font_size = int(screen.get_height() / 25)
    font_file = 'font/Vipnagorgialla Rg.otf'
    fonte = pygame.font.Font(font_file, font_size)
    
    return fonte

def event_buffer():
    
    global ev_buffer

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP or event.type == pygame.TEXTINPUT:
            ev_buffer.append(event)
            #print(event)


    return ev_buffer

def event_buffer_get(hold = None):

    global ev_buffer

    retornar = event_buffer()

    if hold != True:
        ev_buffer = list()

    return retornar
    
def level_001():

    # um monte de variavel da tela

    global screen_cords
    global screen

    scr_scroll = 0
    screen = pygame.Surface((3200, scr_h))
    screen_cords = (scr_scroll, 0)

    # variaveis do plano de fundo

    bg_paralax = (4, 2, 0)
    bg_y_list = (0, 0, 0, 0, 0)
    bg = background('sprites/bg/oak_forest', 4, bg_y_list)
    bg.load(96)

    # varias colisoes

    colid_lista = list()
    colid_lista += limite(top=False, bot=False)

    chao_colid = plataforma(0, screen.get_width(), screen.get_height()-96, screen.get_height())
    colid_lista.append(chao_colid)
    
    # tu

    eu = player(400, 400)

    # assets

    chao = assetona(0, 0, 'sprites/chao/oak_forest.png')
    chao.bot()

    assets_pre = list()
    assets_pre.append(chao)
    assets_pos = list()
    assets_pos.append(assetona(-50, 784, 'sprites/assets/grama_amarela.png'))

    while True:

        eu.movimento()
        for item in colid_lista:
            eu.check_colid(item.rect)
        eu.scroll()
        bg.render(bg_paralax)

        for asset in assets_pre:
            asset.render()

        eu.sprite_process()
        eu.render()
        
        for asset in assets_pos:
            asset.render()



        loop_geral()

def sair_com_esc():

    global saindo

    if saindo == False:
        for event in event_buffer_get(hold=True):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    saindo = time.perf_counter()
    else:
        print(str(time.perf_counter() - saindo)[:4])
        if (time.perf_counter() - saindo) > 2.0: quit()
        for event in event_buffer_get(hold=True):
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    saindo = False
                    print('cancelado')

def limite(top = None, bot = None, l = None, r = None):

    barreiras = list()

    topo = plataforma(0, screen.get_width(), 0, 1)
    fundo = plataforma(0, screen.get_width(), screen.get_height(), screen.get_height()+1)
    esquerda = plataforma(0, 1, 0, screen.get_height())
    direita = plataforma(screen.get_width(), screen.get_width()+1, 0, screen.get_height())

    if top != False: barreiras.append(topo)
    if bot != False: barreiras.append(fundo)
    if l != False: barreiras.append(esquerda)
    if r != False: barreiras.append(direita)

    return barreiras

    


#classes (agora sei mais ou menos o que tô fazendo)
class plataforma(pygame.sprite.Sprite):
    def __init__(self, x0, xf, y0, yf):
        self.x0 = x0
        self.xf = xf
        self.y0 = y0
        self.yf = yf
        self.rect = pygame.Rect(x0, y0, (xf - x0), (yf - y0))
        #print(self.rect)

    def linha_vermelha(self):
        cor = (255, 0 ,0)
        pygame.draw.rect(screen, cor, pygame.Rect(self.rect.left, self.rect.top, self.rect.width, 1))
        pygame.draw.rect(screen, cor, pygame.Rect(self.rect.left, self.rect.bottom, self.rect.width, 1))
        pygame.draw.rect(screen, cor, pygame.Rect(self.rect.left, self.rect.top, 1, self.rect.height))
        pygame.draw.rect(screen, cor, pygame.Rect(self.rect.right, self.rect.top, 1, self.rect.height))
  
class player():
    def __init__(self, x, y):

        self.escala = escala_geral
        self.scr_scroll = 0
        self.scr_w = screen.get_width()
        self.flip = False
        self.vel_y = 0
        self.vel_x = 4
        self.movimento_esquerda = False
        self.movimento_direita = False
        self.pulando = True
        self.vel_terminal = 15

        self.sprite = pygame.image.load('sprites/player.png')
        self.sprite = pygame.transform.scale(self.sprite, (int(self.sprite.get_width() * self.escala), int(self.sprite.get_height() * self.escala)))
        self.rect = self.sprite.get_rect()
        self.rect.center = (x, y)
        
    def movimento(self, hab_pulo = None):

        if hab_pulo != True: self.pulando = True

        delta_x = 0
        delta_y = 0

        if self.vel_y > 0: self.pulando = True

        for event in event_buffer_get(hold=True):
            if event.type == pygame.KEYDOWN:
                if event.key in teclas_esquerda:
                    self.movimento_esquerda = time.perf_counter()
                if event.key in teclas_direita:
                    self.movimento_direita = time.perf_counter()
                if event.unicode == 'z' and self.pulando == False:
                    self.pulando = time.perf_counter()
            elif event.type == pygame.KEYUP:
                if event.key in teclas_esquerda:
                    self.movimento_esquerda = False
                    if self.movimento_direita != False:
                        self.movimento_direita = time.perf_counter()
                if event.key in teclas_direita:
                    self.movimento_direita = False

        if self.movimento_esquerda != False:
            delta_x = ((time.perf_counter() - self.movimento_esquerda) * self.vel_x *-1)*100
            self.movimento_esquerda = time.perf_counter()
            self.flip = True
            #delta_x -= self.vel_x
        elif self.movimento_direita != False:
            delta_x = ((time.perf_counter() - self.movimento_direita) * self.vel_x)*100
            self.movimento_direita = time.perf_counter()
        if int(delta_x) != 0:
            delta_x = self.vel_x * round(delta_x / self.vel_x)
            #print(delta_x)
            #delta_x = self.vel_x

        if self.pulando != False:

            if time.perf_counter() - self.pulando < 2:
                self.vel_y = -5

                for event in event_buffer_get():
                    if event.type == pygame.KEYUP:
                        if event.unicode == 'z':
                            self.pulando = True
                            print('parei de pular')

        event_buffer_get()

        self.vel_y += 0.3
        if self.vel_y > self.vel_terminal: self.vel_y = self.vel_terminal

        delta_y = self.vel_y

        self.rect.x += delta_x
        self.rect.y += delta_y

        #print(self.rect.x)

        self.delta_x = delta_x
        self.delta_y = delta_y

    def sprite_process(self):

        if self.movimento_esquerda:
            self.flip = True
        elif self.movimento_direita:
            self.flip = False

    def render(self):
        screen.blit(pygame.transform.flip(self.sprite, self.flip, False), self.rect)

    def check_colid(self, chao_rect):
        after_left = False
        before_right = False
        below_top = False
        above_bottom = False

        mesmo_x = False
        mesmo_y = False

        x_dif = 0
        y_dif= 0

        variacao = int(self.rect.width/3.5)

        if self.rect.right - variacao > chao_rect.left: after_left = True
        if self.rect.left + variacao < chao_rect.right: before_right = True
        if self.rect.bottom > chao_rect.top: below_top = True
        if self.rect.top < chao_rect.bottom: above_bottom = True

        if before_right and after_left: mesmo_y = True
        elif not before_right and not after_left: mesmo_y = True
        if below_top and above_bottom: mesmo_x = True
        elif not below_top and not above_bottom: mesmo_x = True

        if mesmo_x and mesmo_y:
            if chao_rect.bottom - self.rect.top < self.rect.bottom - chao_rect.top:
                y_dif = chao_rect.bottom - self.rect.top 
            else: y_dif = (self.rect.bottom - chao_rect.top)*-1
            
            if self.rect.right - chao_rect.left < chao_rect.right - self.rect.left:
                x_dif = self.rect.right - chao_rect.left - variacao
            else: x_dif = (chao_rect.right - self.rect.left)*-1 + variacao

            temp_y_dif = y_dif
            temp_x_dif = x_dif

            if y_dif < 0: temp_y_dif = y_dif*-1
            if x_dif < 0: temp_x_dif = x_dif*-1

            if temp_y_dif < temp_x_dif -4: 
                self.rect.y += y_dif
                self.vel_y = 0
                if y_dif < 0: self.pulando = False
                x_dif = 0
            else: 
                self.rect.x += (x_dif)*-1
                y_dif = 0
        
        self.x_dif = x_dif
        self.y_dif = y_dif

    def scroll(self):
        
        global screen_cords
        

        threshold = 650

        if self.rect.x > screen_cords[0] + threshold and self.rect.x < self.scr_w - (1600 - threshold):
            self.scr_scroll = -(self.rect.x - threshold)
            screen_cords = (self.scr_scroll, 0)
        #print(self.scr_scroll)

class background(pygame.sprite.Sprite):
    def __init__(self, folder, repts, y_list):

        self.folder = folder
        self.layers = list()
        self.repts = repts
        self.y_list = y_list

        for n in range (0, len(os.listdir(folder))):
            self.layers.append(f'{folder}/{n+1}.png')

    def load(self, chao):

        lista = list()

        for n in range(0, len(self.layers)):
            sprite = pygame.image.load(self.layers[n]).convert_alpha()

            correcao = 1
            img_h = sprite.get_height()

            if self.y_list[n] == 0 and img_h != 900:
                correcao = (900 - chao)/(img_h*escala_geral)
                #print(correcao)
                

            sprite = pygame.transform.scale(sprite, (int(img_h * escala_geral * correcao), int(sprite.get_height() * escala_geral * correcao)))
            lista.append(sprite)

        self.layers_2 = lista

    def render(self, paralax):

        for nr in range(0, self.repts):
            for n in range(0, len(self.layers_2)):

                if self.y_list[n] == 0: y = 0
                else: y = scr_h - self.layers_2[n].get_height()
                #print(n)
                screen.blit(self.layers_2[n], (self.layers_2[n].get_width()*nr - (paralax[n]/5 * screen_cords[0]), y))

class assetona():
    def __init__(self, x, y, sprite):

        self.x = x
        self.y = y

        sprite = pygame.image.load(sprite)
        self.sprite = pygame.transform.scale(sprite, (int(sprite.get_width() * escala_geral), int(sprite.get_height() * escala_geral)))

    def bot(self):

        self.y = screen.get_height() - self.sprite.get_height()

    def render(self):
        screen.blit(self.sprite, (self.x, self.y))



#agrupamentos de teclas
teclas_confirmar = (pygame.K_KP_ENTER, pygame.KSCAN_KP_ENTER, pygame.K_RETURN, pygame.KSCAN_RETURN)
teclas_cima = (pygame.K_UP,)
teclas_baixo = (pygame.K_DOWN,)
teclas_esquerda = (pygame.K_LEFT,)
teclas_direita = (pygame.K_RIGHT,)






#inicialização do pygame 
pygame.init()
pygame.display.set_caption('Presente')
clock = pygame.time.Clock()

fps_cap = 90

scr_w = 1600
scr_h = 900

tela = pygame.display.set_mode((scr_w, scr_h))
screen = pygame.Surface((scr_w, scr_h))
screen_cords = (0,0)

texto = ('strings/strings-pt-br')
texto = (open(texto).readlines())


#umas variaveis globais
ev_buffer = list()
saindo = False
escala_geral = 4





#loop principal
cena = 0
while True:
    loop_geral()
    cena = guia_de_cenas(cena)
