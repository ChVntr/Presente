#segunda tentativa de fazer esse bagulho dar certo




#imports
import pygame
import time





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
    
    pygame.display.update()
    clock.tick(90)
    event_buffer()
    sair()
    screen.fill((0, 0, 0))
    
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
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
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

    eu_x = 400
    eu_y = 400
    mov_e = False
    mov_d = False
    vel_x = 4
    vel_y = 0
    flip_player_sprite = False
    pulando = False

    while True:

        chao_lista = list()

        chao = plataforma(200, 1000, 600, 650)
        chao_lista.append(chao)
        chao.linha_vermelha()

        eu = player(eu_x, eu_y)
        eu.movimento(mov_e, mov_d, vel_x, vel_y, pulando)
        for chao in chao_lista:
            eu.check_colid_chao(chao.rect)

        eu.sprite_process(flip_player_sprite)
        flip_player_sprite = eu.flip
        eu.render()






        eu_x = eu.rect.x+(32*eu.escala)
        eu_y = eu.rect.y+(32*eu.escala)
        vel_y = eu.vel_y
        mov_e = eu.movimento_esquerda
        mov_d = eu.movimento_direita
        pulando = eu.jump

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

    


#classes (ainda não sei o que tô fazendo)
class plataforma(pygame.sprite.Sprite):
    def __init__(self, x0, xf, y0, yf):
        pygame.sprite.Sprite.__init__(self)
        self.x0 = x0
        self.xf = xf
        self.y0 = y0
        self.yf = yf
        self.rect = pygame.Rect(x0, y0, (xf - x0), (yf - y0))

    def linha_vermelha(self):
        cor = (255, 0 ,0)
        pygame.draw.rect(screen, cor, pygame.Rect(self.rect.left, self.rect.top, self.rect.width, 1))
        pygame.draw.rect(screen, cor, pygame.Rect(self.rect.left, self.rect.bottom, self.rect.width, 1))
        pygame.draw.rect(screen, cor, pygame.Rect(self.rect.left, self.rect.top, 1, self.rect.height))
        pygame.draw.rect(screen, cor, pygame.Rect(self.rect.right, self.rect.top, 1, self.rect.height))
  
class player(pygame.sprite.Sprite):
    def __init__(self, x, y):

        self.escala = 2

        pygame.sprite.Sprite.__init__(self)
        self.sprite = pygame.image.load('sprites/player.png')
        self.sprite = pygame.transform.scale(self.sprite, (int(self.sprite.get_width() * self.escala), int(self.sprite.get_height() * self.escala)))
        self.rect = self.sprite.get_rect()
        self.rect.center = (x, y)
        
    def movimento(self, movimento_esquerda, movimento_direita, vel_x, vel_y, pulando):

        self.movimento_esquerda = movimento_esquerda
        self.movimento_direita = movimento_direita

        self.vel_x = vel_x
        self.vel_y = vel_y
        self.vel_terminal = 15
        self.jump = pulando

        delta_x = 0
        delta_y = 0

        for event in event_buffer_get(hold=True):
            if event.type == pygame.KEYDOWN:
                if event.key in teclas_esquerda:
                    self.movimento_esquerda = True
                if event.key in teclas_direita:
                    self.movimento_direita = True
                if event.unicode == 'z' and self.jump == False:
                    self.jump = time.perf_counter()
            elif event.type == pygame.KEYUP:
                if event.key in teclas_esquerda:
                    self.movimento_esquerda = False
                if event.key in teclas_direita:
                    self.movimento_direita = False

        if self.movimento_esquerda:
            delta_x = -self.vel_x 
            self.flip = True
        elif self.movimento_direita:
            delta_x = self.vel_x 

        if self.jump != False:

            if time.perf_counter() - self.jump < 0.3:
                self.vel_y = -6

                for event in event_buffer_get():
                    if event.type == pygame.KEYUP:
                        if event.unicode == 'z':
                            self.jump = True
                            print('parei de pular')

        event_buffer_get()

        self.vel_y += 0.4
        if self.vel_y > self.vel_terminal: self.vel_y = self.vel_terminal

        delta_y = self.vel_y

        self.rect.x += delta_x
        self.rect.y += delta_y

        #print(self.rect.x)

    def sprite_process(self, flip):

        if self.movimento_esquerda:
            self.flip = True
        elif self.movimento_direita:
            self.flip = False
        else:
            self.flip = flip

    def render(self):
        screen.blit(pygame.transform.flip(self.sprite, self.flip, False), self.rect)

    def check_colid_chao(self, chao_rect):
        after_left = False
        before_right = False
        below_top = False
        above_bottom = False

        mesmo_x = False
        mesmo_y = False

        variacao = int(self.rect.width/3)

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
                if y_dif < 0: self.jump = False
            else: 
                self.rect.x += (x_dif)*-1
        
            
                



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

screen = pygame.display.set_mode((1600, 900), pygame.RESIZABLE)

texto = ('strings/strings-pt-br')
texto = (open(texto).readlines())


#umas variaveis globais
ev_buffer = list()
saindo = False






#loop principal
cena = 0
while True:
    loop_geral()
    cena = guia_de_cenas(cena)
