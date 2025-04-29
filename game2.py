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
    clock.tick()
    sair()
    event_buffer()
    screen.fill((0, 0, 0))

def sair():

    for event in event_buffer_get(hold=True):
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
        f.writelines(text,)
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

    chao_x = 300
    chao_y = 600

    eu_x = 400
    eu_y = 500
    mov_e = False
    mov_d = False


    while True:

        chao = ground(chao_x, chao_y)
        for repet in range(1, 15):
            ground((chao_x + repet * chao.rect.width), chao_y)

        eu = player(eu_x, eu_y)
        eu.movimento(mov_e, mov_d)
        eu.render()

        eu_x = eu.rect.x+32
        eu_y = eu.rect.y+32

        mov_e = eu.movimento_esquerda
        mov_d = eu.movimento_direita

        #print(eu.movimento_direita, eu.movimento_esquerda)

        loop_geral()



#classes (ainda não sei o que tô fazendo)
class ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.sprite = pygame.image.load('sprites/place-holder_chao_armored-armadillo.png')
        self.rect = self.sprite.get_rect()
        self.rect.center = (x, y)
        screen.blit(self.sprite, self.rect)
    
class player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.sprite = pygame.image.load('sprites/place-holder_Sara.png')
        self.rect = self.sprite.get_rect()
        self.rect.center = (x, y)
        
    def movimento(self, movimento_esquerda, movimento_direita):

        self.movimento_esquerda = movimento_esquerda
        self.movimento_direita = movimento_direita

        for event in event_buffer_get():
            if event.type == pygame.KEYDOWN:
                if event.key in teclas_esquerda:
                    self.movimento_esquerda = True
                if event.key in teclas_direita:
                    self.movimento_direita = True
            elif event.type == pygame.KEYUP:
                if event.key in teclas_esquerda:
                    self.movimento_esquerda = False
                if event.key in teclas_direita:
                    self.movimento_direita = False

        self.velocidade = 2

        delta_x = 0
        delta_y = 0

        if self.movimento_esquerda:
            delta_x = -self.velocidade 
        if self.movimento_direita:
            delta_x = self.velocidade 

        self.rect.x += delta_x
        self.rect.y += delta_y

    def render(self):
        screen.blit(self.sprite, self.rect)



#agrupamentos de teclas
teclas_confirmar = (pygame.K_KP_ENTER, pygame.KSCAN_KP_ENTER, pygame.K_RETURN, pygame.KSCAN_RETURN)
teclas_cima = (pygame.K_UP, pygame.K_w)
teclas_baixo = (pygame.K_DOWN, pygame.K_s)
teclas_esquerda = (pygame.K_LEFT, pygame.K_a)
teclas_direita = (pygame.K_RIGHT, pygame.K_d)






#inicialização do pygame 
pygame.init()
pygame.display.set_caption('Presente')
clock = pygame.time.Clock()

screen = pygame.display.set_mode((1600, 900), pygame.RESIZABLE)

texto = ('strings/strings-pt-br')
texto = (open(texto).readlines())


#umas variaveis globais
ev_buffer = list()






#loop principal
cena = 0
while True:
    loop_geral()
    cena = guia_de_cenas(cena)
