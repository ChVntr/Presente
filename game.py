import pygame

pygame.init()





clock = pygame.time.Clock()

run = True

screen_w=1600
screen_h=900

#as fontes que funcinam são -227 -223 -194 -171 -139 -134 -87 -84 -68 14 18 47 70 94 102 107 154 157 173
#as que lidam bem com pontuação 94
valdafonte=94
fontsize = int(screen_h / 25)
font = pygame.font.SysFont(pygame.font.get_fonts()[valdafonte], fontsize)

screen = pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)
sw = (screen.get_width() / 15)
sh = (screen.get_height() / 4)
resfluid=True

andamento=0

hold_lr=0
hold_ud=0

idioma=('jogo/strings/strings-pt-br')
istringi=(open(idioma).readlines())

msc_mainmenu = pygame.mixer_music.load('jogo/st/atelier')
vol_music=15
volume_multiplier=20




def constfont(valor):
    
    global font
    global valdafonte

    fontsize = int(screen_h / 25)


    #as fontes que funcinam são 14 18 47 70 94 102 107
    valdafonte = valdafonte + valor
    
    font = pygame.font.SysFont(pygame.font.get_fonts()[valdafonte], fontsize)

def select_ud(select, limite):

    global hold_ud

    key = pygame.key.get_pressed()

    

    if hold_ud == 0:
        if key[pygame.K_UP] == True or key[pygame.K_w] ==True:
            select = select -1
            hold_ud=1
        elif key[pygame.K_DOWN] == True or key[pygame.K_s] ==True:
            select = select +1
            hold_ud=1
    else:
        if key[pygame.K_UP] != True and key[pygame.K_DOWN] != True and key[pygame.K_s] != True and key[pygame.K_w] != True:
            hold_ud=0


    if select < 0:
        select = limite-1
    elif select == limite:
        select = 0


    
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

    global andamento

    select = 0
    menu = 1

    while menu==1:


        limite=5
        select = select_ud(select, limite)

        for opt in range(0,limite-1):
            draw_text(istringi[opt], font, check_sl(select, opt), sw, sh+(fontsize*opt*1.4))
        draw_text(istringi[limite-1], font, check_sl(select, limite-1), sw, sh+((fontsize*limite)+(3*fontsize)))


        key = pygame.key.get_pressed()
        
        if key[pygame.K_KP_ENTER] or key[pygame.KSCAN_KP_ENTER] or key[pygame.K_SPACE] or key[pygame.K_RETURN] or key[pygame.KSCAN_RETURN] == True:
            if select == 2:
                menu=2
            elif select == limite-1:
                pygame.quit()
                quit()

        loopgeral()

    global vol_music
    select=0

    while menu ==2:

        liststart = limite+1
        limite2=2
        in_opt=False

        select = select_ud(select, limite2+1)

        # eu não sei como isso tá funcionando mas 
        # PELO AMOR DE DEUS NÃO MEXE
        for opt in range(0, limite2):
            draw_text(istringi[opt+liststart], font, check_sl(select, opt), sw, sh+(fontsize*opt*1.40))
        draw_text(istringi[liststart+limite2], font, check_sl(select, limite2), sw, sh+((fontsize*limite2)+(3*fontsize)))

        if select == 1:

            vol_music = select_lr(vol_music, volume_multiplier)
            pygame.mixer.music.set_volume(float(vol_music/volume_multiplier))



        key = pygame.key.get_pressed()
        if key[pygame.K_KP_ENTER] or key[pygame.KSCAN_KP_ENTER] or key[pygame.K_SPACE] or key[pygame.K_RETURN] or key[pygame.KSCAN_RETURN] == True:
            if select == limite2:
                menu=1
                    
                    
                    

                


        loopgeral()
  
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

def sair():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:            
            pygame.quit()
            quit()

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
            menu1()

def loopgeral():

    global sw
    global sh
    global resfluid
    global font

    if resfluid==True:
        sw = (screen.get_width() / 15)
        sh = (screen.get_height() / 4)

        fontsize = int(screen.get_height() / 25)
        font = pygame.font.SysFont(pygame.font.get_fonts()[valdafonte], fontsize)
    

    print(pygame.mixer.music.get_volume())

    
    sair()
    pygame.display.update()
    clock.tick(30)
    screen.fill((0, 0, 0))






while run:
    praondeagora(andamento)
    loopgeral()

