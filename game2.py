#segunda tentativa de fazer esse bagulho dar certo




#imports
import pygame





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
    input_buffer()
    sair()
    screen.fill((0, 0, 0))

def sair():

    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:            
            pygame.quit()
            quit()
            exit()

def guia_de_cenas(cena):

    if cena == 0:
        if save_existe():
            with open('save', 'r') as f:
                data = f.readlines()
                if data[0] == '00':
                    f.close()
                    return 1
        else:
            return 1
    elif cena == 1:
        criar_save()
        return 2    

def criar_save():

    with open('save', 'w') as f:
        f.write('00')
        f.close

    text = ''
    while True:

        posicao_do_texto = (screen.get_width()/4, screen.get_height()/3)

        draw_text(texto[0], posicao_do_texto[0], posicao_do_texto[1])

        for event in input_buffer_get():
                if event.key in teclas_confirmar:
                    print('deu enter')
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
                
        draw_text(text, posicao_do_texto[0], posicao_do_texto[1] + fonte_padrao().get_height(), menos_um=False)
                    




        loop_geral()

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

def input_buffer():
    
    global in_buffer

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            in_buffer.append(event)

    return in_buffer

def input_buffer_get():

    global in_buffer

    retornar = input_buffer()

    in_buffer = list()

    return retornar
    




#agrupamentos de teclas
teclas_confirmar = (pygame.K_KP_ENTER, pygame.KSCAN_KP_ENTER, pygame.K_RETURN, pygame.KSCAN_RETURN)
teclas_cima = (pygame.K_UP, pygame.K_w)
teclas_baixo = (pygame.K_DOWN, pygame.K_s)





#inicialização do pygame 
pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((1600, 900), pygame.RESIZABLE)

texto = ('strings/strings-pt-br')
texto = (open(texto).readlines())


#umas variaveis globais
in_buffer = list()






#loop principal
cena = 0
while True:
    loop_geral()
    cena = guia_de_cenas(cena)
