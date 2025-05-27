#segunda tentativa de fazer esse bagulho dar certo
#IDEIAS
# - placa com panda desenhado
# - janela com vista de uma cutia com passaros
# - entregar uma pedra com um laço



#imports
import pygame
import time
import os
import random




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
    screen_update()
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

    #print(ev_buffer)

    return ev_buffer

def event_buffer_get(hold = None):

    global ev_buffer

    retornar = ev_buffer

    if hold != True:
        ev_buffer = list()

    return retornar
    
def level_001():

    # um monte de variavel da tela

    global screen_cords
    global screen

    scr_scroll = 0
    screen = pygame.Surface((1600*2.5, scr_h))
    screen_cords = (scr_scroll, 0)

    # variaveis do plano de fundo

    bg_paralax = (4, 2, 0)
    bg_y_list = (0, 0, 0, 0, 0)
    bg = background('sprites/bg/oak_forest', bg_y_list, bg_paralax, 96)

    # varias colisoes

    colid_lista = list()
    colid_lista += limite(top=False, bot=False, l=False)

    chao_colid = plataforma(-200, screen.get_width(), screen.get_height()-96, screen.get_height())
    colid_lista.append(chao_colid)
    
    # tu

    eu = player(-100, 784-130, 'sprites/dragao/vermelho', 0.1)

    # assets e renderização

    render_list = list()

    render_list.append(bg)

    chao = assetona(0, 0, 'sprites/chao/oak_forest.png', -1)
    chao.bot()
    render_list.append(chao)

    render_list.append( assetona(2000-20, 550, 'sprites/assets/panda_sign.png') )

    casa_x = 3400
    casa = assetona(casa_x, 316, 'sprites/assets/casa/casa.png')
    porta = assetona(casa_x + 140, 572, 'sprites/assets/casa/porta/1.png', anim_speed=0.03, anim_folder='sprites/assets/casa/porta')

    grama_min = 20
    grama_max = 100
    preda_min = 100
    preda_max = 700
    xf = screen.get_width()

    render_list.append(rndm_asset(0, casa_x, 804, 'sprites/assets/grama_amarela', grama_min, grama_max))
    render_list.append(rndm_asset(0, casa_x, 804, 'sprites/assets/preda', preda_min, preda_max))
    render_list.append(rndm_asset(0, casa_x, 804, 'sprites/assets/grama_amarela', grama_min, grama_max))
    render_list.append(casa)
    render_list.append(porta)
    
    render_list.append(eu)

    render_list.append(rndm_asset(0, xf, 804, 'sprites/assets/grama_amarela', grama_min, grama_max))
    render_list.append(rndm_asset(0, casa_x, 812, 'sprites/assets/preda', preda_min, preda_max))
    render_list.append(rndm_asset(0, xf, 812, 'sprites/assets/grama_amarela', grama_min, grama_max))
    

    f_in = time.perf_counter()
    cutscene = True
    while cutscene:
            
        for obj in render_list:
            obj.render()
        
        cutscene = fade_in(f_in, 2)
        loop_geral()

    cutscene = True
    eu.movimento_direita = time.perf_counter() 
    while eu.rect.center[0] < 400:

        eu.movimento(block_input=True)
        for item in colid_lista:
            eu.check_colid(item.rect)
        eu.scroll()
        eu.animate()
        eu.sprite_process()
        
            
        for obj in render_list:
            obj.render()
        
        loop_geral()
        
    eu.movimento_direita = False
    colid_lista += limite(top=False, bot=False, r=False)

    max_dif = 200
    porta_rev = True
    porta.sprite_atual = 10
    while True:

        eu.movimento()
        for item in colid_lista:
            eu.check_colid(item.rect)
        eu.scroll()
        eu.animate()
        eu.sprite_process()
        
        porta_dif = eu.rect.x - porta.x + 72
        if porta_dif < max_dif and porta_dif > max_dif*-1:
            if porta_rev:
                if porta.sprite_atual == 10: porta.sprite_atual = 0
                porta_rev = False
        else: 
            if not porta_rev:
                if porta.sprite_atual == 10: porta.sprite_atual = 0
                porta_rev = True
        porta.animate(reverse=porta_rev)

        for obj in render_list:
            obj.render()
        interact(porta, eu, 'vai se fuder')
        

        loop_geral()

def sair_com_esc():

    global saindo

    if saindo == False:
        for event in ev_buffer:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    saindo = time.perf_counter()
    else:
        print(str(time.perf_counter() - saindo)[:4])
        if (time.perf_counter() - saindo) > 2.0: quit()
        for event in ev_buffer:
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

def screen_update():
    tela.blit(screen, screen_cords)
    pygame.display.flip()
    screen.fill((0, 0, 0))
    
def fade_in(tempo, segundos):

    tempo = time.perf_counter() - tempo

    surface_fade = pygame.Surface((scr_w, scr_h), pygame.SRCALPHA)

    alpha = int(255 - (tempo/segundos * 255))

    if alpha < 0: alpha = 0

    surface_fade.fill((0, 0, 0, alpha))
    screen.blit(surface_fade, (0, 0))


    if tempo >= segundos:
        return False
    else: return True

def escala(n):

    return (escala_geral * round(n/escala_geral))




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
    def __init__(self, x, y, sprite_folder, anim_speed):

        self.scr_scroll = 0
        self.scr_w = screen.get_width()
        self.flip = False
        self.vel_y = 0
        self.vel_x = 4
        self.movimento_esquerda = False
        self.movimento_direita = False
        self.pulando = True
        self.vel_terminal = 15
        self.anim_speed = anim_speed

        sprite_list = list()
        for n in range (0, len(os.listdir(sprite_folder))):
            sprite = (f'{sprite_folder}/{n+1}.png')
            sprite = pygame.image.load(sprite)
            sprite = pygame.transform.scale(sprite, (int(sprite.get_width() * escala_geral), int(sprite.get_height() * escala_geral)))
            sprite_list.append(sprite)
        
        self.rect = sprite.get_rect()
        self.rect.center = (x, y)

        self.sprite_list = sprite_list
        self.anim_progress = False
        self.sprite_atual = 0
        self.sprite = sprite
        
    def movimento(self, hab_pulo = None, block_input = None):

        if hab_pulo != True: self.pulando = True

        delta_x = 0
        delta_y = 0

        if self.vel_y > 0: self.pulando = True

        if block_input != True:
            for event in ev_buffer:
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

        if self.pulando != False:

            if time.perf_counter() - self.pulando < 2:
                self.vel_y = -5

                if block_input != True:
                    for event in event_buffer_get():
                        if event.type == pygame.KEYUP:
                            if event.unicode == 'z':
                                self.pulando = True
                                print('parei de pular')

        if block_input != True: event_buffer_get()

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

        #self.vel_y += 0.3
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
            if self.scr_scroll > 0: self.scr_scroll = 0
            screen_cords = (self.scr_scroll, 0)
        #print(self.scr_scroll)

    def animate(self):

        if self.sprite_atual >= len(self.sprite_list): self.sprite_atual = 0

        if self.anim_progress == False:
            self.anim_progress = time.perf_counter()

        if time.perf_counter() - self.anim_progress > self.anim_speed:
            self.sprite = self.sprite_list[self.sprite_atual]
            self.sprite_atual += 1
            self.anim_progress = time.perf_counter()

class background(pygame.sprite.Sprite):
    def __init__(self, folder, y_list, paralax, chao):

        self.folder = folder
        self.layers = list()
        self.y_list = y_list
        self.paralax = paralax

        self.scr_h = screen.get_height()
        self.scr_w = screen.get_width()

        for n in range (0, len(os.listdir(folder))):
            self.layers.append(f'{folder}/{n+1}.png')

        lista = list()

        for n in range(0, len(self.layers)):
            sprite = pygame.image.load(self.layers[n]).convert_alpha()

            correcao = 1
            if self.y_list[n] == 0 and sprite.get_height() != 900:
                correcao = ((900 - chao)/(sprite.get_height() * escala_geral))
                #print(correcao)

            w = sprite.get_width() * escala_geral * correcao
            h = sprite.get_height() * escala_geral * correcao

            w = escala(w)
            h = escala(h)

            sprite = pygame.transform.scale(sprite, (w, h))
            lista.append(sprite)

        self.layers_2 = lista
        self.sprites_w = list()

        for item in self.layers_2:

            self.sprites_w.append(item.get_width())

    def render(self):

        last_x = list((0, 0, 0))

        for n in range(0, len(self.layers_2)):

            img_w = self.sprites_w[n]

            while True:

                prlx = self.paralax[n]/5 * screen_cords[0]

                x = last_x[n] - prlx 

                if x > screen_cords[0]*-1 + 1600: break
                last_x[n] = x + img_w + prlx

                if x > screen_cords[0]*-1 - img_w: 
                    if self.y_list[n] == 0: y = 0
                    else: y = self.scr_h - self.layers_2[n].get_height()
                    screen.blit(self.layers_2[n], (x, y))

class assetona():
    def __init__(self, x, y, sprite, repets = None, anim_folder = None, anim_speed = None):

        self.x = escala(x)
        self.y = escala(y)

        if repets == None: repets = 1
        self.repets = repets

        self.anim_folder = anim_folder
        self.anim_speed = anim_speed
        self.anim_progress = False

        sprite = pygame.image.load(sprite)
        self.sprite = pygame.transform.scale(sprite, (int(sprite.get_width() * escala_geral), int(sprite.get_height() * escala_geral)))

        self.img_w = self.sprite.get_width()

        anim_sprites = list()
        if self.anim_folder != None:

            for n in range (0, len(os.listdir(anim_folder))):
                sprite = (f'{anim_folder}/{n+1}.png')
                sprite = pygame.image.load(sprite)
                sprite = pygame.transform.scale(sprite, (int(sprite.get_width() * escala_geral), int(sprite.get_height() * escala_geral)))

                anim_sprites.append(sprite)

        self.anim_sprites = anim_sprites
        self.sprite_atual = 0

    def bot(self):

        self.y = screen.get_height() - self.sprite.get_height()

    def animate(self, reverse = None, loop = None, boomerang = None, random = None):
        
        if self.sprite_atual >= len(self.anim_sprites):
            if loop == True: self.sprite_atual = 0
            else: return
        
        if self.anim_progress == False:
            self.anim_progress = time.perf_counter()

        if reverse != True:
            if time.perf_counter() - self.anim_progress > self.anim_speed:
                self.sprite = self.anim_sprites[self.sprite_atual]
                self.sprite_atual += 1
                self.anim_progress = time.perf_counter()
        else:
            if time.perf_counter() - self.anim_progress > self.anim_speed:
                self.sprite = self.anim_sprites[len(self.anim_sprites) - self.sprite_atual -1]
                self.sprite_atual += 1
                self.anim_progress = time.perf_counter()

    def render(self):

        if self.repets == -1: inf = True
        else: inf = False
        
        if not inf: 
            for n in range(0, self.repets):
                x = self.x + self.img_w * n
                if x > screen_cords[0]*-1 + 1600: return
                if x > screen_cords[0]*-1 - self.img_w:
                    screen.blit(self.sprite, (x, self.y))           
        else:
            x = self.x * screen_cords[0] / self.img_w
            while True:
                if x > screen_cords[0]*-1 + 1600: return
                if x > screen_cords[0]*-1 - self.img_w:
                    screen.blit(self.sprite, (x, self.y))
                x += self.img_w

class rndm_asset():

    def __init__(self, x, xf, y, folder, int_min = None, int_max = None):

        self.y = y

        if int_min == None: int_min = 0
        if int_max == None: int_max = 0

        sprite_list = list()
        sprite_list2 = list()
        self.sprite_x_list = list()
        self.sprite_order = list()

        for n in range (0, len(os.listdir(folder))):
            sprite_list.append(f'{folder}/{n+1}.png')

        #print(sprite_list)

        for sprite in sprite_list:
            sprite = pygame.image.load(sprite)
            sprite = pygame.transform.scale(sprite, (int(sprite.get_width() * escala_geral), int(sprite.get_height() * escala_geral)))

            sprite_list2.append(sprite)
        sprite_list = sprite_list2

        n=0
        p_x = 0
        while True:

            self.sprite_order.append(sprite_list[random.randrange(0, len(sprite_list))])
            
            if len(self.sprite_x_list) == 0: self.sprite_x_list.append(0)
            else: 
                x = p_x + self.sprite_order[n].get_width() + random.randrange(int_min, int_max)
                x = escala(x)

                if x > xf: 
                    break

                self.sprite_x_list.append(x)
                p_x = x

            n += 1

    def render(self):

        for n in range(0, len(self.sprite_x_list)):
            
            x = self.sprite_x_list[n]
            
            if x > screen_cords[0]*-1 + 1600: 
                return
            
            if x > screen_cords[0]*-1 - self.sprite_order[n].get_width():
                screen.blit(self.sprite_order[n], (x, self.y - self.sprite_order[n].get_height()))

class interact():
    def __init__(self, obj, player, texto):
            
            perto = False
            longe = True

            dif = player.rect.x - obj.x + 52
            max_dif = 200

            if dif < max_dif and dif > max_dif*-1:
                print(texto)

    def fade_in():
        ''

    def fade_out():
        ''
                


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
