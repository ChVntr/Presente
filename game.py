# espera... é tudo função?
# sempre foi...





def constfont(valor):
    
    global font
    global valdafonte

    fontsize = int(screen_h / 25)
    font = pygame.font.Font(fonte, fontsize)

def select_ud(select, limite):

    global hold_ud

    key = pygame.key.get_pressed()

    

    if hold_ud == 0:
        for tecla in teclas_cima:
            if key[tecla]:
                select = select -1
                hold_ud=1
                break
        for tecla in teclas_baixo:
            if key[tecla]:
                select = select +1
                hold_ud=1
                break
    else:
        for tecla in teclas_cima + teclas_baixo:
            if key[tecla]:
                hold_ud=1
                break
            hold_ud=0


    if select < 0:
        select = limite-1
    elif select == limite:
        select = 0


    #print(select)
    return select

def select_lr(select, limite):

    global hold_lr

    key = pygame.key.get_pressed()

    

    if hold_lr == 0:
        if key[pygame.K_RIGHT] == True or key[pygame.K_d] ==True:
            select = select +1
            hold_lr=1
        elif key[pygame.K_LEFT] == True or key[pygame.K_a] ==True:
            select = select -1
            hold_lr=1
    else:
        if key[pygame.K_RIGHT] != True and key[pygame.K_LEFT] != True and key[pygame.K_a] != True and key[pygame.K_d] != True:
            hold_lr=0


    if select < 0:
        select = 0
    elif select == limite:
        select = limite-1


    
    return select

def check_sl(esseaqui, tanesse):
    
    if esseaqui == tanesse:
        text_col = (255, 255, 255)
    else:
        text_col = (125, 125, 125)

    return(text_col)

def menu1():

    select = 0
    menu = 1

    while menu==1:

        if not tem_save:
            save_variavel = 1
        else:
            save_variavel = 0

        limite=5-save_variavel
        select = select_ud(select, limite)

        for opt in range(0, limite-1):
            draw_text(istringi[opt+save_variavel], font, check_sl(select, opt), sw, sh+(fontsize*opt*1.4))
        draw_text(istringi[limite-1+save_variavel], font, check_sl(select, limite-1), sw, sh+((fontsize*limite)+(3*fontsize)))


        key = pygame.key.get_pressed()
        for tecla in teclas_confirmar:
            if key[tecla]:
                if select == limite-3:
                    menu=2
                elif select == limite-1:
                    pygame.quit()
                elif select == limite-4:
                    return 1

        limite = limite + save_variavel
        loopgeral()

    select=0
    while menu ==2:

        global vol_music
        
        liststart = limite+1
        limite2=1
        in_opt=False

        select = select_ud(select, limite2+1)
        print(select)

        # eu não sei como isso tá funcionando mas 
        # PELO AMOR DE DEUS NÃO MEXE
        for opt in range(0, limite2):
            draw_text(istringi[opt+liststart], font, check_sl(select, opt), sw, sh+(fontsize*opt*1.40))
            if opt == 0:
                barra_pos_h = sh+(fontsize*opt)+(fontsize*0.3)
                barra_pos_w = (screen.get_width() / 2)
                barra_multiplicador = 0.005
                pygame.draw.rect(screen, check_sl(select, opt), (barra_pos_w, barra_pos_h, fontsize*vol_music/2, fontsize/2))
                pygame.draw.rect(screen, check_sl(select, opt), (barra_pos_w-(barra_pos_w*barra_multiplicador), barra_pos_h-(barra_pos_h*barra_multiplicador*2.5), 2, fontsize/1.5))
                pygame.draw.rect(screen, check_sl(select, opt), (barra_pos_w+(barra_pos_w*barra_multiplicador)+(fontsize*10), barra_pos_h-(barra_pos_h*barra_multiplicador*2.5), 2, fontsize/1.5))
            #print(fontsize*vol_music/2, fontsize*10, fontsize, vol_music)

        draw_text(istringi[liststart+limite2], font, check_sl(select, limite2), sw, sh+((fontsize*limite2)+(3*fontsize)))

        if select == 0:

            vol_music = select_lr(vol_music, volume_multiplier+1)
            pygame.mixer.music.set_volume(float(vol_music/volume_multiplier))
            




        key = pygame.key.get_pressed()
        for tecla in teclas_confirmar:
            if key[tecla]:
                if select == limite2:
                    menu=1
                    
                    
                    

                


        return 0
  
def draw_text(text, font, text_col, x, y):
    img = font.render(text[:-1], True, text_col)
    screen.blit(img, (x, y))

    #pygame.draw.rect(screen, (255, 0, 0), (0, y, screen.get_width(), 2))
    #print(text_col)

def sair():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:            
            pygame.quit()
            quit()
            exit()

def mvmdir(obj):

    pygame.draw.rect(screen, (255, 0, 0), obj)

    key = pygame.key.get_pressed()

    if key[pygame.K_UP] == True:
        obj.move_ip(0, -1)

    if key[pygame.K_DOWN] == True:
        obj.move_ip(0, +1)

    if key[pygame.K_LEFT] == True:
        obj.move_ip(-1, 0)

    if key[pygame.K_RIGHT] == True:
        obj.move_ip(+1, 0)

def praondeagora(simbora):
    
    if simbora == 0:
        pygame.mixer.music.play(0)
        pygame.mixer.music.set_volume(float(vol_music/volume_multiplier))
        while simbora == 0:
            result = menu1()
            if result != 0: break
        return result
    elif simbora == 1:
        print('agora faz oq kkkkkk')
        pygame.quit()

def loopgeral():

    global sw
    global sh
    global resfluid
    global font
    global fontsize
    

    if resfluid==True:
        sw = (screen.get_width() / 15)
        sh = (screen.get_height() / 4)

        fontsize = int(screen.get_height() / 25)
        font = pygame.font.Font(fonte, fontsize)
    

    #print(pygame.mixer.music.get_volume())

    
    sair()
    pygame.display.update()
    #clock.tick(), print(clock.get_fps())
    screen.fill((0, 0, 0))

def hora_do_pau():
    ''



# unica importação sem imposto
import pygame





# inicialização do pygame 
pygame.init()
clock = pygame.time.Clock()




# cacetada de variavel

screen_w=1600
screen_h=900

fontsize = int(screen_h / 25)
fonte = 'font/Vipnagorgialla Rg.otf'
font = pygame.font.Font(fonte, fontsize)

screen = pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)
sw = (screen.get_width() / 15)
sh = (screen.get_height() / 4)
resfluid=True

andamento=0

hold_lr=0
hold_ud=0

idioma=('strings/strings-pt-br')
istringi=(open(idioma).readlines())

msc_mainmenu = pygame.mixer_music.load('soundtrack/atelier.mp3')
vol_music=0
volume_multiplier=20

filename = 'save'

try:
    with open(filename, 'r') as f:
        tem_save = True
        f.close()
except:
        tem_save = False

teclas_confirmar = (pygame.K_KP_ENTER, pygame.KSCAN_KP_ENTER, pygame.K_SPACE, pygame.K_RETURN, pygame.KSCAN_RETURN)
teclas_cima = (pygame.K_UP, pygame.K_w)
teclas_baixo = (pygame.K_DOWN, pygame.K_s)





# loop principal do jogo
while True:
    andamento = praondeagora(andamento)
    loopgeral()

